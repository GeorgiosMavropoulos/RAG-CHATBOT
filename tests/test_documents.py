import pytest
from ..chroma_db.chroma import ChromaDocumentManager
import logging



from unittest.mock import MagicMock, patch

from ..llm.llm_client import LLM

llm = LLM()

@pytest.fixture
def manager(tmp_path):
    return ChromaDocumentManager(
        persist_directory=str(tmp_path / "db"),
        collection_name="test_collection",
    )


@pytest.fixture
def txt_file(tmp_path):
    path = tmp_path / "story.txt"
    path.write_text("Hellen works as a Data Scientist on Athens. " * 50, encoding="utf-8")
    return str(path)


def test_index_txt_file(manager, txt_file):
    """Test that a file can be indexed"""
    assert manager.load_and_index_txt(txt_file, display_name="story.txt") is True
    assert manager.collection.count() > 0


def test_sources_show_display_name(manager, txt_file):
    """Verify that sources show only the display name, not hte whole path"""
    manager.load_and_index_txt(txt_file, display_name="story.txt")
    sources = manager.list_sources()
    assert "story.txt" in sources
    assert sources["story.txt"] == txt_file


def test_query_returns_results(manager, txt_file):
    
    manager.load_and_index_txt(txt_file)
    results = manager.query_documents("data scientist", n_results=3)
    assert results is not None
    assert len(results["documents"][0]) > 0


def test_delete_document_removes_chunks(manager, txt_file):
    manager.load_and_index_txt(txt_file)
    assert manager.delete_document(txt_file) is True
    assert manager.collection.count() == 0


def test_delete_unknown_document_returns_false(manager):
    assert manager.delete_document("does_not_exist.txt") is False


def test_empty_file_is_not_indexed(manager, tmp_path):
    empty = tmp_path / "empty.txt"
    empty.write_text("   ", encoding="utf-8")
    assert manager.load_and_index_txt(str(empty)) is False


def test_missing_file_returns_false(manager):
    assert manager.load_and_index_txt("nope.txt") is False


### Supported ttypes

def test_txt_content_is_returned(manager, tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("Hello world", encoding="utf-8")
    assert manager.get_file_find_its_type(str(path)) == "Hello world"


def test_uppercase_extension_is_accepted(manager, tmp_path):
    path = tmp_path / "NOTES.TXT"
    path.write_text("hello", encoding="utf-8")
    assert manager.get_file_find_its_type(str(path)) == "hello"

from unittest.mock import MagicMock, patch




### Unsupported types
UNSUPPORTED = ["doc.docx", "image.png", "data.csv", "script.py", "noextension"]


@pytest.mark.parametrize("filename", UNSUPPORTED)
def test_unsupported_type_raises_value_error(manager, tmp_path, filename):
    path = tmp_path / filename
    path.write_text("content", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported file type"):
        manager.get_file_find_its_type(str(path))


@pytest.mark.parametrize("filename", UNSUPPORTED)
def test_unsupported_type_is_not_indexed(manager, tmp_path, filename, caplog):
    path = tmp_path / filename
    path.write_text("content", encoding="utf-8")

    with caplog.at_level(logging.ERROR):
        assert manager.load_and_index_txt(str(path)) is False

    assert "Unsupported file type" in caplog.text
    assert manager.collection.count() == 0


## Test unsupported types
def test_missing_file_logs_not_found(manager, caplog):
    with caplog.at_level(logging.ERROR):
        assert manager.load_and_index_txt("missing.txt") is False
    assert "File not found: missing.txt" in caplog.text


def test_empty_file_logs_warning(manager, tmp_path, caplog):
    path = tmp_path / "empty.txt"
    path.write_text("   \n", encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        assert manager.load_and_index_txt(str(path)) is False
    assert "is empty. Skipping indexing." in caplog.text


def test_unsupported_type_error_message_contains_extension(manager, tmp_path):
    path = tmp_path / "doc.docx"
    path.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        manager.get_file_find_its_type(str(path))
    assert str(exc.value) == "Unsupported file type: .docx"



