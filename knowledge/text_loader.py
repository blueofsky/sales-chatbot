import logging
from pathlib import Path
from typing import Iterator, Optional, Union

from langchain_core.documents import Document

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.helpers import detect_file_encodings

logger = logging.getLogger(__name__)

class KbTextLoader(TextLoader):
    """Load text file.


    Args:
        file_path: Path to the file to load.

        encoding: File encoding to use. If `None`, the file will be loaded
        with the default system encoding.

        autodetect_encoding: Whether to try to autodetect the file encoding
            if the specified encoding fails.
    """
    
    # metadata name
    _METADATA_TOPIC_NAME = "topic"

    def __init__(self,
                 file_path: Union[str, Path],
                 encoding: Optional[str] = None,
                 autodetect_encoding: bool = False,
                 topic: Optional[str] = None):
        super().__init__(file_path, encoding, autodetect_encoding)
        self.topic = topic

    def lazy_load(self) -> Iterator[Document]:
        """Load from file path."""
        text = ""
        try:
            with open(self.file_path, encoding=self.encoding) as f:
                text = f.read()
        except UnicodeDecodeError as e:
            if self.autodetect_encoding:
                detected_encodings = detect_file_encodings(self.file_path)
                for encoding in detected_encodings:
                    logger.debug(f"Trying encoding: {encoding.encoding}")
                    try:
                        with open(self.file_path, encoding=encoding.encoding) as f:
                            text = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
            else:
                raise RuntimeError(f"Error loading {self.file_path}") from e
        except Exception as e:
            raise RuntimeError(f"Error loading {self.file_path}") from e

        metadata = {"source": str(self.file_path),self._METADATA_TOPIC_NAME:str(self.topic) or None}
        yield Document(page_content=text, metadata=metadata)