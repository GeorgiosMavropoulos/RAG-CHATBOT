"""Main entry point. Main method allows users to add documents to the chromaDB and query the LLM to retrive information from the document"""

from chroma_db.chroma import ChromaDocumentManager

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

    
   

def query_vector_database(question):
    results = chrom.query(
        query_texts=[question],
        n_results=1
    )
    results_text = results['documents'][0][0]
    return results_text

def main():
    """Parse any document to chroma db and call the LLM to question it"""

    #add file
    add_file(file)



main()


