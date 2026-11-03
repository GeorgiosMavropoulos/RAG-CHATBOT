"""Module with an instance to add any document to chroma"""
from chroma import ChromaDocumentManager
chrom = ChromaDocumentManager(
    persist_directory="./my_chroma_db",
    collection_name="my_persistent_collection"
)
collection = chrom.create_collection("my_persistent_collection")

chrom.load_and_index_txt(
    file_path="./mock_story.txt"
)