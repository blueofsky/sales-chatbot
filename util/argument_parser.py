import argparse

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='sales assistant')        
        subparsers = self.parser.add_subparsers(dest='command', help='default command: chat')
        
        spider_parsers = subparsers.add_parser('spider', help='fetch data from llm.')
        spider_parsers.add_argument('--topic', type=str,default='房地产', help='spide data topic,default is 房地产')
        spider_parsers.add_argument('--model_name', type=str, default='gpt-4o-mini', help='spide model name,default is gpt-4o-mini')
        spider_parsers.add_argument('--data_path', type=str,default='./.kb', help='data store path,default is ./.kb')
        spider_parsers.add_argument('--data_num', type=int,default=50, help='fetch data num,default is 50')
        spider_parsers.add_argument('--verbose', type=bool,default=True, help='verbose mode,default is True')
        

        chat_parsers = subparsers.add_parser('chat', help='chat with llm.')
        chat_parsers.add_argument('--model_name', type=str, default='gpt-4o-mini', help='chat model name,default is gpt-4o-mini')
        chat_parsers.add_argument('--data_path', type=str,default='./.kb', help='data store path,default is ./.kb')

    def parse_arguments(self):
        args = self.parser.parse_args()
        if args.command is None:
            args.command = 'chat'
        return args