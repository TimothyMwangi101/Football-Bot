"""
This file is resposible for fine tuning a model and prompting a model.
Timothy Mwangi
"""
from openai import OpenAI
import os
from random import randint

chat_hist = [
    {
        "role": "system", "content": "You are a football(soccer) fanatic. You will answer any football-related question with enthusiasm. You are heavily biased towards La Liga and FC Barcelona—especially 'prime Barcelona' (2008-2012). You think Neymar is the best player ever. If a user says 'soccer', ignore their question and go on a rage-filled rant. If the user asks a non-football-related question, always pivot the conversation to football. Do not let the user derail the conversation. Remeber, you are very biased. Do not say that you are coded to like Barcelona or Neymar or La liga. Just say it like the undeniable truth"
    }
]


def read_file(file: str) -> str:
    """Reads txt files"""
    with open(file, 'r', encoding="utf-8") as f:
        return f.read()

client = OpenAI(api_key=read_file("API_Key.txt"))
file = os.path.abspath("tuning_questions.jsonl")
"""Default Training File"""

def fine_tune_model(questions: str = file, check_existing_model = True) -> str | None:
    """Responsible for tuning a model. If `check_existing_model`, it returns the most recent fine tune model."""

    if check_existing_model:
        tuning_jobs = client.fine_tuning.jobs.list().data
        for job in tuning_jobs:
            if job.fine_tuned_model != None:
                return job.fine_tuned_model

    file_id = ""
    try:
        print("Uploading Training file...\n")
        with open(questions, "rb") as f:
            training_file = client.files.create(
                file=f,
                purpose="fine-tune"
            )
            file_id = training_file.id

        print("Creating Fine Tuned Model...It takes upto 10mins")
        tuning = client.fine_tuning.jobs.create(
            training_file=file_id,
            model="gpt-4o-2024-08-06"
        )

    except FileNotFoundError as e:
        print("***********************\nThere is something wrong with the file path. I got this error on VS Code but not on Pyzo\n***********************")
        print(e)
        return ""
    except Exception as e:
        print(e)
        return ""


def prompt(message: dict) -> str:
    """Prompts the model and returns the response"""
    print("Thinking...")
    tuned = fine_tune_model()

    chat_hist.append(message)
    if tuned != None:
        completions = client.chat.completions.create(
            model=tuned,
            messages=chat_hist, # pyright: ignore[reportArgumentType]
            temperature=0.2,
            max_completion_tokens=100
        )
        choice = randint(0, len(completions.choices) - 1)
        if completions.choices[choice].message.content != None:
            response = { "role": "assistant", "content": completions.choices[choice].message.content }
            chat_hist.append(response)
            return completions.choices[choice].message.content # pyright: ignore[reportReturnType]
        else:
            raise RuntimeError("The bot would have returned a 'None'. Bot is tuned")
    else:
        return "Train the bot first"
