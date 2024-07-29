import os
import sys
import gradio as gr
import warnings

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from util import ArgumentParser,LOG
from knowledge import Spider
from chatbot import SalesChatbot

# 关闭所有警告
warnings.simplefilter('ignore')

def sales_chat(message, history,topic) -> str:
    LOG.debug(f"[topic]: {topic},[message]: {message},[history]: {history}")
    bot=SalesChatbot(model_name=args.model_name,kb_path=args.data_path,topic=topic)
    return bot.invoke(message)

def launch_gradio():
    iface = gr.ChatInterface(
        fn=sales_chat,
        title="销售助手",
        additional_inputs_accordion='知识库',
        additional_inputs=[gr.Dropdown(label='专业领域',value="房地产",choices=["房地产", "教育", "电器"], allow_custom_value=True)],
        # retry_btn=None,
        # undo_btn=None,
        chatbot=gr.Chatbot(),
    )
    iface.launch(share=True, server_name="0.0.0.0")

def launch_spider():
    spider=Spider(model_name=args.model_name,kb_path=args.data_path)
    spider.agent.chain.verbose = args.verbose
    file_path,docs_num=spider.fetch(topic=args.topic,num=args.data_num)
    LOG.info(f'store file path: {file_path},vector store doc num: {docs_num}')

if __name__ == "__main__":
    args=ArgumentParser().parse_arguments()
    if args.command == 'spider':
        launch_spider()
    elif args.command == 'chat':
        launch_gradio()