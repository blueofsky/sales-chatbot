# 智能销售机器人
## 介绍
销售机器人,应用于不同的销售场景，如：电器、家装、教育等.

为了测试，每个场景的数据，均可以通过Spider从大模型爬取。


## 开始使用
### 环境准备
```bash
# 克隆仓库
git clone https://github.com/blueofsky/sales-chatbot.git
# 安装依赖
cd sales-chatbot
pip install -r requirements.txt
# 设置环境变量
export OPENAI_API_KEY="sk-xxx"
```

### 使用说明
#### 1. 爬取数据
> 执行`python main.py spider --help`：
```bash
usage: main.py spider [-h] [--topic TOPIC] [--model_name MODEL_NAME] [--data_path DATA_PATH] [--data_num DATA_NUM] [--verbose VERBOSE]

options:
  -h, --help            show this help message and exit
  --topic TOPIC         spide data topic,default is 房地产
  --model_name MODEL_NAME
                        spide model name,default is gpt-4o-mini
  --data_path DATA_PATH
                        data store path,default is ./.kb
  --data_num DATA_NUM   fetch data num,default is 50
  --verbose VERBOSE     verbose mode,default is True
```
> 举例：
```bash
python main.py spider --topic 电器 
```

#### 2. 聊天机器人
> 执行`python main.py chat --help`：
```bash
usage: main.py chat [-h] [--model_name MODEL_NAME] [--data_path DATA_PATH]

options:
  -h, --help            show this help message and exit
  --model_name MODEL_NAME
                        chat model name,default is gpt-4o-mini
  --data_path DATA_PATH
                        data store path,default is ./.kb
```
> 举例：
```bash
python main.py chat --model_name gpt-4o
```
> 访问地址：http://localhost:7860/
