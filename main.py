from LLM import OllamaLLMModel
from db.query import Chroma

def main():

    user_session_id = "test_user_2"
    user_question = "我媽媽有糖尿病，需要定期找人陪伴看醫生，請推薦給我看護"


    LLM_model = OllamaLLMModel(model="llama3.1:8b", base_url="http://127.0.0.1:8888")

    intention = LLM_model.extract(user_question)
    print(f"intent: {intention}")

    # find the RAG
    if intention['caregiver_intent']:
        chroma = Chroma()
        person_id_arr, person_data_arr = chroma.get_top3_result(intention['feature'])

        recommdation = []

        for i in range(len(person_data_arr)):
            candidate = person_id_arr[i] + " - " + person_data_arr[i] + "\n"
            recommdation.append(candidate)

        compose_question = f"""
            用戶目前有尋找看護的意圖，這是用戶的問題：
            {user_question}
            
            以下是目前尋找到的人選：
            {recommdation}，
            請彙整結果並條列後，再給用戶。
        """
        print(f"compose_question: {compose_question}")
        print(f"RAG Final: {LLM_model.chat_with_ai(user_session_id, compose_question)}")
    else:
        print(f"Final: {LLM_model.chat_with_ai(user_session_id, user_question)}")

if __name__ == "__main__":
    main()
