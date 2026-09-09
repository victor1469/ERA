import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5:3b"



def generate_answer(question, context):

    prompt = f"""
你是一个企业智能文档助手。

请严格根据下面的文档内容回答问题。

如果文档没有相关信息，请回答：
"文档中没有找到相关信息。"

文档内容：

{context}


用户问题：

{question}

"""


    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )


    result = response.json()


    return result["response"]