import os
from datetime import datetime

def save_conversation(call_sid, user_input, bot_reply):
    folder = "conversations"
    os.makedirs(folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{folder}/{call_sid}_{timestamp}.txt"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"User: {user_input}\n")
        f.write(f"Sofia: {bot_reply}\n\n")
