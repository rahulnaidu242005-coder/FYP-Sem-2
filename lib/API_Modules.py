from datetime import datetime
import httpx, logging, re, time, json
from pydantic import HttpUrl
from lib.Config import AUTHENTICATION_URI, ROOT_URI, EARLIEST_DATE, get_current_timestamp
from lib.Models import APIRequestModel


class JsonlFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            # ISO 8601 Timestamp
            "timestamp": f"{datetime.fromtimestamp(record.created).isoformat()}Z",
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        # Include exception info if it exists
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)

logger = logging.getLogger(__name__)

class RedactingFilter(logging.Filter):
    """Intercepts and redacts sensitive information from all log records."""

    # 1. We define patterns to catch:
    # - password= in URLs (handles encoded characters)
    # - NetWitness-Token in headers
    # - accessToken in JSON responses
    SENSITIVE_PATTERNS = {
        # Catches username=admin OR 'username': 'admin'
        r"(username[=\s':]+)[^&\s'\"]+": r"\1********",
        r"(password[=\s':]+)[^&\s'\"]+": r"\1********",
        r"(NetWitness-Token[=\s':]+)[^&\s'\"]+": r"\1********",
        r"(accessToken[=\s':]+)[^&\s'\"]+": r"\1********",
        rf"{ROOT_URI}\/": ".../",
    }

    def filter(self, record):
        # Get the original log message
        msg = record.getMessage()

        for pattern, replacement in self.SENSITIVE_PATTERNS.items():
            # Check if the pattern exists in the message to avoid unnecessary work
            if re.search(pattern, msg):
                msg = re.sub(pattern, replacement, msg)

        # Overwrite the record message with the scrubbed version
        record.msg = msg
        record.args = None  # Crucial: prevents re-interpolation of original data
        return True

class NetWitnessClient:
    def __init__(self):
        self.timeout = httpx.Timeout(20.0, connect=30.0)
        # Using a Client session is more efficient for multiple calls
        self.client = httpx.Client(timeout=self.timeout, verify=False)
        # Log client initialization (don't log any secrets)
        logger.info("NetWitnessClient initialized", extra={"timeout": str(self.timeout)})

    def call_api(self, components: APIRequestModel) -> dict:
        logger.info(f"Calling {components.method} with {components.uri}")
        start_time = time.perf_counter()
        response = self.client.request(
            method=components.method,
            url=str(components.uri),
            params=components.query_params,
            headers=components.headers,
            json=components.body
        )
        end_time = time.perf_counter()
        duration = end_time - start_time

        # Log the duration (rounded to 2 decimal places)
        logger.info(f"API Response received in {duration:.2f} seconds")

        # Log status and approximate response size (do not log full body)
        logger.info(f"API response status={response.status_code}")

        if response.status_code == 405 and str(components.uri) == AUTHENTICATION_URI:
            logger.info("Server contactable (Health Check)")
        elif response.status_code != 200:
            logger.error(f"Failed: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()

    def get_token(self, username, password) -> str:
        # Log attempt but mask username for safety
        masked_user = (username[0] + "***") if (username and len(username) > 0) else "***"
        logger.info(f"Requesting token for user={masked_user}")
        req = APIRequestModel(
            method="POST",
            uri=HttpUrl(url=AUTHENTICATION_URI),
            query_params={"username": username, "password": password}
        )
        token = self.call_api(req).get("accessToken", "dummystr")
        # Log token retrieval without exposing the token (log length only)
        try:
            token_len = len(token) if isinstance(token, str) else 0
        except Exception:
            token_len = 0
        logger.info(f"accessToken={token} retrieved with length={token_len}")
        return token

    def get_incidents(self, token, since=EARLIEST_DATE, until=get_current_timestamp(), page=0, size=100) -> dict:
        logger.info(f"Fetching incidents since={since} until={until} page={page} size={size}")
        req = APIRequestModel(
            method="GET",
            uri=HttpUrl(url=f"{ROOT_URI}/incidents"),
            query_params={"since": since, "until": until, "pageNumber": page, "pageSize": size},
            headers={"NetWitness-Token": token}
        )
        resp = self.call_api(req)
        # Summarize response: try to log incident count if present
        count = None
        if isinstance(resp, dict):
            if "incidents" in resp and isinstance(resp["incidents"], list):
                count = len(resp["incidents"])
            elif "data" in resp and isinstance(resp["data"], list):
                count = len(resp["data"])
        if count is not None:
            logger.info(f"Retrieved incidents count={count}")
        else:
            # Fallback: log top-level keys to help debugging without dumping sensitive data
            try:
                keys = list(resp.keys()) if isinstance(resp, dict) else []
            except Exception:
                keys = []
            logger.info(f"Retrieved incidents response keys={keys}")
        return resp

class LoggerCustom:
    def __init__(self, file_name):
        self.log_file_name = file_name

    def setup_logging(self):
        """Configure root logging for the application.

        - File handler writes JSONL lines to app.log with redaction.
        - Console handler writes the same JSONL lines to stderr (useful during development).
        """
        file_handler = logging.FileHandler(self.log_file_name)
        file_handler.addFilter(RedactingFilter())
        file_handler.setFormatter(JsonlFormatter())

        # 3. Configure Root Logger
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler]
        )