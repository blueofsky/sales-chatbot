from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import (
    Optional,
    Union,
    List,
)
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


class KnowledgeBase:
    """ Knowledge Base """
    # metadata name
    _METADATA_TOPIC_NAME = "topic"

    def __init__(self,kb_path:Optional[str]="./.kb"):
        self.vector_store_path=f'{kb_path}/faiss'

    def append(self,docs: List[Union[str,Document]],topic: Optional[str]=None) -> int:
        """ Append docs to knowledge base """

        # convert str to Document
        if isinstance(docs[0],str):
            docs = [Document(page_content=doc,metadata={self._METADATA_TOPIC_NAME: topic}) for doc in docs]
        
        # split docs
        text_splitter = CharacterTextSplitter(
            separator = r'\d+\.',
            chunk_size = 100,
            chunk_overlap  = 0,
            length_function = len,
            is_separator_regex = True,)
        docs = text_splitter.split_documents(docs)

        # add docs to kb
        db = self.load()
        db.add_documents(docs)

        # save kb to disk
        db.save_local(self.vector_store_path)
        return db.index.ntotal
    
    def load(self) -> FAISS:
        """ Load knowledge base """
        embedding=OpenAIEmbeddings()
        try:
            return FAISS.load_local(self.vector_store_path, embedding,allow_dangerous_deserialization=True)
        except:
            return FAISS.from_texts([''], embedding)

    def _clear(self):
        """ Clear knowledge base """
        import shutil
        shutil.rmtree(self.vector_store_path)
