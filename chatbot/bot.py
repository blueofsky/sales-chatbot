from langchain_openai import ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from typing import (
    Optional
)
from knowledge import KnowledgeBase
from util import LOG

class SalesChatbot:

    def __init__(self,kb_path: Optional[str]="./.kb",model_name:str="gpt-4o-mini",topic: Optional[str]=None):
        self.kb_path=kb_path
        self.model_name=model_name
        self.topic=topic
        self.reload()

    def reload(self):
        db = KnowledgeBase(self.kb_path).load()
        search_kwargs={"score_threshold": 0.8}
        if self.topic:
            search_kwargs['filter']={'topic':self.topic}
        retriever=db.as_retriever(search_type="similarity_score_threshold",
                                   search_kwargs=search_kwargs)
        
        system_template = """请使用以下上下文片段来回答用户的问题。
        如果您不知道答案，请以销售人员的视角委婉回答，且不要试图凭空编造答案。
        ----------------
        {context}"""
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
        prompt=  ChatPromptTemplate.from_messages(messages)
        llm=ChatOpenAI(model_name=self.model_name, temperature=0)
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        self._salesbot = create_retrieval_chain(retriever, question_answer_chain)

    def invoke(self,message) -> str:
        ans = self._salesbot.invoke({"input": message})
        LOG.debug(ans)
        # if ans['context']:
        print(f"[answer]{ans['answer']}")
        print(f"[context]{ans['context']}")
        return ans["answer"]
        # else:
        #     return "这个问题我要问问领导"
