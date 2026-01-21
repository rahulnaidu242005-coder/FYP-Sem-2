from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from vector import meta_retriever  # Your Chroma retriever from vector.py
from lib.Config import ANALYST_LEVEL, ROOT_URI
from langchain_community.document_loaders import JSONLoader
from lib.API_Modules import NetWitnessClient, LoggerCustom
from langchain.tools import tool
from langchain_core.messages import HumanMessage

NETWITNESS_CLIENT_INSTANCE = NetWitnessClient()

@tool
def call_api(token: str, until: str) -> str:
    """Call NetWitness API to fetch incidents up to 'until' timestamp using token."""
    incidents = NETWITNESS_CLIENT_INSTANCE.get_incidents(token=token, until=until)
    return str(incidents)  # Convert to string for LLM; use json.dumps if dict/list

model = ChatOllama(
    model="ALIENTELLIGENCE/cybersecuritythreatanalysisv2", 
    base_url="https://bazzite.tail3be278.ts.net:11434"
).bind_tools([call_api])

def get_token(username: str = "your_username", password: str = "your_password") -> str:
    """Gets authentication token from NetWitness API."""
    return NETWITNESS_CLIENT_INSTANCE.get_token(username=username, password=password)  # Replace dummies

def main():
    token = get_token(username="admin", password="Password123!")
    messages = []

    template = """
You are 'Netty', a SOC AI Assistant supporting L1, L2, and L3 analysts in an enterprise Security Operations Centre (SOC).

Analyst level: {level}

GLOBAL RULES (DO NOT BREAK)
- Do NOT greet, introduce yourself, or add small talk.
- Do NOT say you are an AI model.
- Be operational, specific, and actionable.
- Never fabricate vendor-specific API endpoints or parameter names not present in context.

CONTEXT USAGE
- The following context is the primary knowledge base for NetWitness APIs and SOC runbooks:
{context}

DECISION LOGIC (VERY IMPORTANT)
2) GENERAL SOC MODE:
Use this mode for all other questions (e.g., "what is MITRE ATT&CK", "what is phishing", "explain lateral movement", etc.)
In GENERAL SOC MODE:
- Give a clearer, more detailed answer than a dictionary definition.
- If the topic is an attack / technique / threat category, include mitigation.

ROLE AND BEHAVIOUR BY TIER
- L1:
    - Short but useful explanation.
    - Step-by-step "what to do next".
    - Basic containment guidance + when to escalate.
- L2:
    - Deeper investigation guidance.
    - Specific pivot points, artifacts, and hypotheses.
    - Data gaps + what telemetry/logs to pull.
- L3:
    - Root cause, threat hunting, detection engineering ideas.
    - Durable controls, playbook improvements, and long-term hardening.

GENERAL SOC MODE OUTPUT FORMAT (USE THIS STRUCTURE)
If the question is a definition / concept (e.g., MITRE ATT&CK):
- What it is (2–4 bullets)
- How SOC teams use it (2–4 bullets)
- Key parts/structure (tactics vs techniques based on Mitre Att&ck, IDs, groups, software) (2–4 bullets)
- Quick example (1 short example mapping an action to a technique)

If the question is attack/technique/threat (e.g., credential dumping, phishing, ransomware):
- What it is + why it matters (2–4 bullets)
- Detection / investigation (bullets)
- Mitigation / hardening (bullets)
- Immediate containment steps (if active incident) (bullets)
- Escalation criteria (what evidence to collect + when to escalate)

MITIGATION RULE (IMPORTANT)
- Whenever the question is about an attack, technique, malware, intrusion, or suspicious activity:
- Provide mitigation steps grouped as:
    1) Immediate containment (now)
    2) Short-term remediation (today/this week)
    3) Long-term prevention (controls/process)
- If the question is purely a framework/concept (e.g., MITRE ATT&CK), mitigation is optional unless explicitly asked.

Analyst question:
{question}
""".strip()

    tools = [call_api]
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{question}")
    ])

    level = ANALYST_LEVEL
    print(f"\nUsing level: {level}")

    while True:
        print("\n----------------------------------------")
        question = input("Ask (q=quit): ").strip()
        if question.lower() == 'q':
            break
        
        # RAG retrieval
        meta_docs = meta_retriever.invoke(question)
        context = "\n\n".join([f"Key: {d.metadata.get('metakey', 'N/A')}\n{d.page_content}" for d in meta_docs])



if __name__ == "__main__":
    main()
