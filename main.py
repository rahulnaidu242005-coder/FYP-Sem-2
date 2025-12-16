from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
 
model = OllamaLLM(model="ALIENTELLIGENCE/cybersecuritythreatanalysisv2")
NETWITNESS_URI = "https://uvo1tpfzak7r2s03nhe.env.cloudshare.com/"

def main():
    template = """
    You are a plain text to link converter specialized in cybersecurity threat analysis using NetWitness. 
    Your task is to convert the analyst's natural language question into a direct link that can be used in NetWitness to find relevant data.
    Your knowledge base context is: {context}
    The netwitness instance is hosted at {NETWITNESS_URI}, replace the placeholder with the actual URI when needed.
    placeholders are enclosed in <>.
    If unable to find a relevant link, respond with: NO LINK FOUND
    Ensure your response is concise and only contains the link or the NO LINK FOUND message, no other text is to be output.
    Here is the analyst's question to answer: {question}
    Only output the final answer which should be formatted a link only. Do not output any other text.
    format your answer as follows:
    <NETWITNESS_URI>/path/to/resource?query=params
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    while True:
        print("\n\n----------------------------------------")
        question = input("Ask your question (q to quit): ")
        print("\n\n")
        if question == "q":
            break
    
        context = retriever.invoke(question)
        result = chain.invoke({"NETWITNESS_URI": NETWITNESS_URI, "context": context, "question": question})
        print(result)


if __name__ == "__main__":
    main()