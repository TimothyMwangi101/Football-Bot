"""
Use the discord bot using the cmd prompt
Timothy Mwangi
"""
from openai import OpenAI
from model import prompt

def read_file(file: str) -> str:
    """Reads txt files"""
    with open(file, 'r', encoding="utf-8") as f:
        return f.read()

key = read_file("API_Key.txt")
client = OpenAI(api_key=key)

def main() -> None:
    print("Hey there. I am a MASSIVE fan of FOOTBALL not 🤮\"soccer\"🤮. Ask me about football and i can answer.")
    bye = ["bye", "goodbye", "later"]
    while True:
        utterance = input(">>> ")
        message = {"role": "user", "content": utterance}
        print(prompt(message))

        if utterance.lower() in bye:
            break

if __name__ == "__main__":
    main()
