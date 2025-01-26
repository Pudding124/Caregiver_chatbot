from langchain_redis import RedisChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


# Add messages to the history
# history.add_message(HumanMessage(content="Hello, AI!"))
# history.add_message(
#   AIMessage(content="Hello, human! How can I assist you today?")
# )
def get_history(session_id):

    history = RedisChatMessageHistory(
        session_id=session_id,
        redis_url="redis://localhost:6379",
        ttl=3600  # Messages expire after 1 hour
    )

    return history

def setup_history(history, question, answer):
    history.add_message(HumanMessage(content=question))
    history.add_message(
      AIMessage(content=answer)
    )

