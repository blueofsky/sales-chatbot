
import faiss
from typing import (
    Optional,
)
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings,ChatOpenAI

from .write_file_tool import KbWriteFileTool
from .text_loader import KbTextLoader
from .kbase import KnowledgeBase
from autogpt import AutoGPT

class Spider:
    def __init__(self,model_name:Optional[str]="gpt-4o-mini",kb_path:Optional[str]="./.kb"):
        self.model_name=model_name
        self.doc_store_path=f'{kb_path}/spider'
        # init agent
        embedding_size = 1536 # OpenAI Embedding 向量维数
        self.vectorstore = FAISS(OpenAIEmbeddings().embed_query, 
                                 faiss.IndexFlatL2(embedding_size), 
                                 InMemoryDocstore({}), {})
        self.kbWriteTools=KbWriteFileTool(root_dir=self.doc_store_path)
        self.agent = AutoGPT.from_llm_and_tools(
            ai_name="Jarvis",
            ai_role="Assistant",
            tools=[self.kbWriteTools],
            llm=ChatOpenAI(model_name=self.model_name, temperature=0.8, verbose=True),
            memory=self.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": 0.8}),
        )        
        self.agent.chain.verbose = False
        # create kb
        self.kbase=KnowledgeBase(kb_path)

    def fetch(self,topic: Optional[str]=None,num: Optional[int]=100) :
        self.agent.run([
        f"""
        你是中国顶级的 `{topic}` 领域销售,现在培训职场新人,请给出 `{num}` 条实用的销售话术。

        每条销售话术以如下格式给出：
        [客户问题]
        [销售回答]

        例如：
        1. [客户问题] 这个小区有什么配套设施？
        [销售回答] 这个小区有完善的配套设,包括健身房、游泳池和儿童游乐场,还有24小时安保服务。

        2. [客户问题] 附近有没有好的学校？
        [销售回答] 是的,附近有几所非常不错的学校,包括XXX小学和XXX中学,教育资源非常丰富。

        """
        ])
        file_path=self.kbWriteTools.write_path
        textLoader=KbTextLoader(file_path=file_path,
                                encoding="utf-8",
                                topic=topic)
        docs = textLoader.lazy_load()
        ntotal = self.kbase.append(list(docs),topic)
        return file_path,ntotal