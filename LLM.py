from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama.llms import OllamaLLM
from langchain.memory import ConversationBufferMemory
from history import get_history, setup_history
import json


class LLM():
    def __init__(self, model, base_url):
        self.llm = OllamaLLM(model=model, base_url=base_url)

    def extract(self, qustion):
        try:
            prompt = ChatPromptTemplate([
                ("system", "你是一位專業的看護仲介，會幫助使用者回答有關於醫療看護的問題，並且會提供看護人選供客戶使用"),
                ("human", "{question}")  # 當前用戶輸入
            ])
            chain = prompt | self.llm

            prompt_question = f"""
                請你判斷使用者是否有尋找用戶的意圖，並整理他提到的特徵，尋找特徵方法如下，如果沒有尋找到就不需隨意猜測。
                - 被照顧者的病症或狀況
                - 被照顧者的年齡或性別
                - 需求的看護類型（例如：輪班、全日照顧等）
                - 能需要具備的特別才能（例如：語言能力）

                以下是用戶的問題
                {qustion}

                最後請只要回傳 JSON 格式，不要說明或介紹，格式如下

                {{"caregiver_intent": true, "feature": ["male", "english", "24 hours"]}}
            """

            # 讓 LLM 產生回應
            response = chain.invoke({
                "question": prompt_question
            })

            # print(f"response: {response}")

            return json.loads(response)
        except Exception:
            return json.loads({"caregiver_intent": False, "feature": []})
        
    def chat_with_ai(self, session_id, question):
        try:
            history = get_history(session_id)

            memory = ConversationBufferMemory(
                memory_key="history",
                chat_memory=history,
                return_messages=True
            )

            if len(history.message) == 0:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "你是一位專業的看護仲介，會幫助使用者回答有關於醫療看護的問題，並且會提供看護人選供客戶使用"),
                    MessagesPlaceholder(variable_name="history"),  # 插入歷史對話
                    ("human", "{question}")  # 當前用戶輸入
                ])
            else:
                # 創建 Prompt 模板
                prompt = ChatPromptTemplate.from_messages([
                    MessagesPlaceholder(variable_name="history"),  # 插入歷史對話
                    ("human", "{question}")  # 當前用戶輸入
                ])

            # print(memory.load_memory_variables({})["history"])

            chain = prompt | self.llm

            # 讓 LLM 產生回應
            response = chain.invoke({
                "history": memory.load_memory_variables({})["history"],  # 載入 Redis 中的對話歷史
                "question": question
            })

            setup_history(history, question, response)

            return response
        except Exception:
            return "聊天機器人忙碌中，請再次輸入你的問題，謝謝"

