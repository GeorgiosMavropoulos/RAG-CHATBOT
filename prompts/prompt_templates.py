"""
Prompts Module
Containing the following prompt templates:
QA_RAG_TEMPLATE: Prompting the LLM with hallucation guardrails so as it won't response with text that it's not available on the retrieved text
"""
class Prompts:
    def __init__(self):
        pass



    QA_RAG_TEMPLATE = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 

    If the context does not contain the answer, say "I cannot find the answer in the provided documents." 
    Do not use outside knowledge. Keep the answer concise (maximum three sentences).

    Context:
    {context}

    Question: {question}

    Answer:
    """


