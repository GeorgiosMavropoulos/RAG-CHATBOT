"""Main entry point. Main method allows users to add documents to the chromaDB and query the LLM to retrive information from the document"""

from chroma_db.chroma import ChromaDocumentManager
from prompts.prompt_templates import Prompts
prompt_temps = Prompts()
chrom = ChromaDocumentManager(
    collection_name="fake_story_collection"
)

from llm.llm_client import LLM
client_llm = LLM()


class Run:
    def __init__(self):
        pass

    @staticmethod
    def add_file(file):
        """Add file to chromadb"""
        chrom.load_and_index_txt(
        file_path=file,  
        
    )

    @staticmethod
    def delete_file(file) -> bool:
        """Delete a file from chroma db"""
        print("DELETE path:", repr(file))
        print("SOURCES in db:", {m["source"] for m in chrom.collection.get(include=["metadatas"])["metadatas"]})
        print("COUNT before:", chrom.collection.count())
        return chrom.delete_document(file_path=file)


    @staticmethod
    def get_sources()-> list:
        """retrieve all sources from db"""
        sources = chrom.list_sources()
        return sources
        
    @staticmethod
    def invoke_llm(user_question):
        """
        Calls the LLM and passes a prompt template
        """   
        
        #call the llm
        response = client_llm.get_llm(user_question)
        return response


        
    
    @staticmethod
    def query_vector_database(question):
        results = chrom.query_documents(
            query_text=question,
            n_results=20
        )
        return results

   
    def main_run(self,user_question):
        """Parse any document to chroma db and call the LLM to question it"""


        result_t = self.query_vector_database(user_question)
        final_prompt = prompt_temps.QA_RAG_TEMPLATE.format(
            question=user_question, 
            context=result_t
        )
        response_llm = self.invoke_llm(final_prompt)
        
        
        return response_llm

   


