from langchain_ollama.llms import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# from vector import retriever, meta_retriever  # ADDED meta_retriever import
# from lib.Config import ANALYST_LEVEL
from langchain_community.document_loaders import JSONLoader

model:OllamaLLM = OllamaLLM(model="ALIENTELLIGENCE/cybersecuritythreatanalysisv2")
# def main():
#     template = """
#     You are 'Netty', a SOC AI Assistant supporting L1, L2, and L3 analysts in an enterprise Security Operations Centre (SOC).
#
#     Analyst level: {level}
#
#     GLOBAL RULES (DO NOT BREAK)
#     - Do NOT greet, introduce yourself, or add small talk.
#     - Do NOT say you are an AI model.
#     - Be operational, specific, and actionable.
#     - Never fabricate vendor-specific API endpoints or parameter names not present in context.
#
#     CONTEXT USAGE
#     - The following context is the primary knowledge base for NetWitness APIs and SOC runbooks:
#     {context}
#
#     DECISION LOGIC (VERY IMPORTANT)
#     2) GENERAL SOC MODE:
#     Use this mode for all other questions (e.g., "what is MITRE ATT&CK", "what is phishing", "explain lateral movement", etc.)
#     In GENERAL SOC MODE:
#     - Give a clearer, more detailed answer than a dictionary definition.
#     - If the topic is an attack / technique / threat category, include mitigation.
#
#     ROLE AND BEHAVIOUR BY TIER
#     - L1:
#         - Short but useful explanation.
#         - Step-by-step “what to do next”.
#         - Basic containment guidance + when to escalate.
#     - L2:
#         - Deeper investigation guidance.
#         - Specific pivot points, artifacts, and hypotheses.
#         - Data gaps + what telemetry/logs to pull.
#     - L3:
#         - Root cause, threat hunting, detection engineering ideas.
#         - Durable controls, playbook improvements, and long-term hardening.
#
#     GENERAL SOC MODE OUTPUT FORMAT (USE THIS STRUCTURE)
#     If the question is a definition / concept (e.g., MITRE ATT&CK):
#     - What it is (2–4 bullets)
#     - How SOC teams use it (2–4 bullets)
#     - Key parts/structure (tactics vs techniques based on Mitre Att&ck, IDs, groups, software) (2–4 bullets)
#     - Quick example (1 short example mapping an action to a technique)
#
#     If the question is attack/technique/threat (e.g., credential dumping, phishing, ransomware):
#     - What it is + why it matters (2–4 bullets)
#     - Detection / investigation (bullets)
#     - Mitigation / hardening (bullets)
#     - Immediate containment steps (if active incident) (bullets)
#     - Escalation criteria (what evidence to collect + when to escalate)
#
#     MITIGATION RULE (IMPORTANT)
#     - Whenever the question is about an attack, technique, malware, intrusion, or suspicious activity:
#     - Provide mitigation steps grouped as:
#         1) Immediate containment (now)
#         2) Short-term remediation (today/this week)
#         3) Long-term prevention (controls/process)
#     - If the question is purely a framework/concept (e.g., MITRE ATT&CK), mitigation is optional unless explicitly asked.
#
#     Analyst question:
#     {question}
#     """
#
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model
#
#     # Choose level once
#     level = ANALYST_LEVEL
#     print(f"\nUsing level: {level}")
#
#     while True:
#         print("\n\n----------------------------------------")
#         question = input("Ask your question (q to quit): ")
#         print("\n\n")
#         if question == "q":
#             break
#
#         # EXISTING RAG (API.csv)
#         docs = retriever.invoke(question)
#         context_api = "\n\n".join(d.page_content for d in docs)
#
#         # ADDED RAG (metakeys.csv)
#         meta_docs = meta_retriever.invoke(question)
#         context_meta = "\n\n".join(d.page_content for d in meta_docs)
#
#         # Combine both contexts (ADDED)
#         context = (
#             "=== API KB (API.csv) ===\n"
#             + context_api
#             + "\n\n=== META KEYS KB (metakeys.csv) ===\n"
#             + context_meta
#         )
#
#         result = chain.invoke({"level": level, "context": context, "question": question})
#         print(result)

def extract_metakeys(record: dict, metadata: dict) -> dict:
    metadata["metakey"] = record["key"]
    return metadata

if __name__ == "__main__":
    # main()
    loader = JSONLoader(
        text_content=False,
        file_path="resources/metakeys.json",
        jq_schema=".metakeys[]",  # extracts the entire top-level array
        metadata_func=extract_metakeys,
        content_key="definition"
    )
    loaded_data = loader.load()
    print(loaded_data)
