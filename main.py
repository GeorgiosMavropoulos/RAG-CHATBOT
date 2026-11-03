"""Main entry point. Main method allows users to add documents to the chromaDB and query the LLM to retrive information from the document"""

from chroma_db.chroma import ChromaDocumentManager
from prompts.prompt_templates import Prompts
prompt_temps = Prompts()
chrom = ChromaDocumentManager(
    collection_name="fake_story_collection"
)

from llm.llm_client import LLM
client_llm = LLM()

file = './mock_story.txt'

def add_file(file):
    """Add file to chromadb"""
    chrom.load_and_index_txt(
    file_path=file,
    

    
)

def invoke_llm(user_question):
    """
       Calls the LLM and passes a prompt template
    """   
    
    #call the llm
    response = client_llm.get_llm(user_question)
    return response


     
   

def query_vector_database(question):
    results = chrom.query_documents(
        query_text=question,
        n_results=1
    )
    return results

def main():
    """Parse any document to chroma db and call the LLM to question it"""

    #add file
   # add_file(file)
    
    user_question = "Where is the village of Veyrath?"

    result_t = query_vector_database(user_question)
    final_prompt = prompt_temps.QA_RAG_TEMPLATE.format(
        question=user_question, 
        context=result_t
    )
    response_llm = invoke_llm(final_prompt)
    print(response_llm)

main()


