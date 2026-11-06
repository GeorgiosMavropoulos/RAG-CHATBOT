import logging
import os
from typing import Any

import chromadb
from chromadb.errors import ChromaError
from langchain_text_splitters import RecursiveCharacterTextSplitter

#from langchain_core.document_loaders import TextLoader
from pypdf import PdfReader

# Configure logging
logger = logging.getLogger(__name__)
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
            logger.info(f"Initializing Chroma DB persistent client at: {self.persist_directory}")
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            logger.info(f"Accessing collection: {self.collection_name}")
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
        except RuntimeError as e:
            logger.error(f"Failed to initialize Chroma DB: {e!s}")
            raise RuntimeError(f"Database initialization failed: {e}")


    def get_file_find_its_type(self, file_path: str):
        """Helper method to use pdf loader if user inputs a pdf file"""
        # Cleaned up duplicate assignment ext = ext = ...
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".pdf":
            # 1. Initialize Reader
            reader = PdfReader(file_path)
            # 2. Loop through pages and extract text properly using extract_text()
            extracted_pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_pages.append(text)
            return "\n\n".join(extracted_pages)
            
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        

    def load_and_index_txt(self, file_path: str, chunk_size: int = 1000, display_name: str | None = None, chunk_overlap: int = 120) -> bool:
        """
        Reads a text file, splits it into chunks, and indexes it into the vector database.
        """
 
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False


        try:
            #get file's type
            logger.info(f"Reading file: {file_path}")
            raw_text = self.get_file_find_its_type(file_path)
            print(raw_text[:1000])

            if not raw_text.strip():
                logger.warning(f"File {file_path} is empty. Skipping indexing.")
                return False

            # 2. Split the text into manageable chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            chunks = text_splitter.split_text(raw_text)
            logger.info(f"Split text into {len(chunks)} chunks.")

            # 3. Prepare data lists for vector insertion
            documents = []
            ids = []
            metadatas = []
            
            base_filename = os.path.basename(file_path)
            name = display_name or base_filename
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                ids.append(f"{base_filename}_chunk_{i}")
                metadatas.append({"source": file_path, "name": name, "chunk_index": i})

            # 4. Insert chunks into Chroma DB collection
            logger.info(f"Adding chunks to collection '{self.collection_name}'...")
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            logger.info(f"Successfully indexed {len(chunks)} chunks from {base_filename}.")
            return True

        except ChromaError as ce:
            logger.error(f"Chroma DB error while adding documents: {ce!s}")
            return False
        except OSError as ioe:
            logger.error(f"File I/O error while reading {file_path}: {ioe!s}")
            return False
        except (ValueError, TypeError, AttributeError) as e:
            logger.error(f"Data processing error occurred during indexing: {e!s}")
            return False

    def query_documents(self, query_text: str, n_results: int = 20) -> dict[str, Any] | None:
        """
        Queries the database for the most semantically relevant text chunks.
        """
        try:
            logger.info(f"Executing query: '{query_text}' requesting {n_results} results.")
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            logger.info(f"Retrieved: {results['documents']}")
            logger.info(f"Distances: {results['distances']}")
            return results
        except ChromaError as ce:
            logger.error(f"Chroma DB query execution failed: {ce!s}")
            return None
        except (ValueError, TypeError, AttributeError) as e:
                    logger.error(f"Query processing error occurred during indexing: {e!s}")
                    return False


    def list_sources(self) -> list[str]:
       
        """Returns {display_name: source_path}."""
        data = self.collection.get(include=["metadatas"])
        docs = {}
        for m in data["metadatas"]:
            if m and "source" in m:
                docs[m.get("name", m["source"])] = m["source"]
        return docs



    def delete_document(self, file_path: str) -> bool:
        """
        Deletes all chunks that came from a specific file, using the 'source' metadata.
        """
        try:
            before = self.collection.count()
            self.collection.delete(where={"source": file_path})
            after = self.collection.count()
            logger.info(f"Deleted {before - after} chunks for source: {file_path}")
            return after < before  
        except ChromaError as ce:
            logger.error(f"Chroma DB error while deleting document: {ce!s}")
            return False
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid arguments provided for deletion: {e!s}")
            return False
