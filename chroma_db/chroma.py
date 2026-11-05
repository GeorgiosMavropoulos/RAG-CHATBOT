import os
import logging
from typing import Dict, Any, Optional
from langchain_community.document_loaders import  PyPDFLoader, TextLoader
import chromadb

from chromadb.errors import ChromaError
from langchain_text_splitters import RecursiveCharacterTextSplitter




# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ChromaDocumentManager:
    """
    A manager class to handle Chroma DB initialization, 
    document processing, text splitting, and querying.
    """
    def __init__(self, persist_directory: str = "./my_chroma_db", collection_name: str = "documents_collection"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        
        # Initialize the database client and collection
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initializes the persistent Chroma DB client and gets or creates the collection."""
        try:
            logging.info(f"Initializing Chroma DB persistent client at: {self.persist_directory}")
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            logging.info(f"Accessing collection: {self.collection_name}")
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
        except Exception as e:
            logging.error(f"Failed to initialize Chroma DB: {str(e)}")
            raise RuntimeError(f"Database initialization failed: {e}")


    def get_file_find_its_type(self, file_path: str):
        """Helper method to user pdf loader if user inputs a pdf file"""

        #get file's extension
        ext = ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
         pages = PyPDFLoader(file_path).load()
         return "\n\n".join(p.page_content for p in pages)
        elif  ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
             return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        

    def load_and_index_txt(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 120) -> bool:
        """
        Reads a text file, splits it into chunks, and indexes it into the vector database.
        """
 
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return False


        try:
            #get file's type
            logging.info(f"Reading file: {file_path}")
            raw_text = self.get_file_find_its_type(file_path)
            print(raw_text[:1000])

            if not raw_text.strip():
                logging.warning(f"File {file_path} is empty. Skipping indexing.")
                return False

            # 2. Split the text into manageable chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            chunks = text_splitter.split_text(raw_text)
            logging.info(f"Split text into {len(chunks)} chunks.")

            # 3. Prepare data lists for vector insertion
            documents = []
            ids = []
            metadatas = []
            
            base_filename = os.path.basename(file_path)
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                # Create a unique ID combining filename and chunk index
                ids.append(f"{base_filename}_chunk_{i}")
                metadatas.append({"source": file_path, "chunk_index": i})

            # 4. Insert chunks into Chroma DB collection
            logging.info(f"Adding chunks to collection '{self.collection_name}'...")
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            logging.info(f"Successfully indexed {len(chunks)} chunks from {base_filename}.")
            return True

        except ChromaError as ce:
            logging.error(f"Chroma DB error while adding documents: {str(ce)}")
            return False
        except IOError as ioe:
            logging.error(f"File I/O error while reading {file_path}: {str(ioe)}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error occurred during indexing: {str(e)}")
            return False

    def query_documents(self, query_text: str, n_results: int = 20) -> Optional[Dict[str, Any]]:
        """
        Queries the database for the most semantically relevant text chunks.
        """
        try:
            logging.info(f"Executing query: '{query_text}' requesting {n_results} results.")
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            logging.info(f"Retrieved: {results['documents']}")
            logging.info(f"Distances: {results['distances']}")
            return results
        except ChromaError as ce:
            logging.error(f"Chroma DB query execution failed: {str(ce)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error occurred during query: {str(e)}")
            return None



    def delete_document(self, file_path: str) -> bool:
        """
        Deletes all chunks that came from a specific file, using the 'source' metadata.
        """
        try:
            logging.info(f"Deleting chunks from source: {file_path}")
            self.collection.delete(where={"source": file_path})
            logging.info(f"Deleted chunks for {file_path}.")
            return True
        except ChromaError as ce:
            logging.error(f"Chroma DB error while deleting document: {str(ce)}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error while deleting document: {str(e)}")
            return False
