from LLM import LLM

def main():

    user_session_id = "test_user"
    user_question = "我媽媽有腎臟病，想要尋找中文看護，只需要照顧早上就好"


    LLM_model = LLM(model="llama3.1:8b", base_url="http://127.0.0.1:8888")

    intention = LLM_model.extract(user_question)
    print(f"intent: {intention}")

    # find the RAG
    if intention.caregiver_intent:
        
    else:
        return LLM_model.chat_with_ai(user_session_id, user_question)

if __name__ == "__main__":
    main()
