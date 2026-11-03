"""
Prompts Module
Containing the following prompt templates:
QA_RAG_TEMPLATE: Prompting the LLM with hallucation guardrails so as it won't response with text that it's not available on the retrieved text
"""
class Prompts:
    def __init__(self):
        pass



    QA_RAG_TEMPLATE = """

You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you `I can't help you sir`. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:


"""