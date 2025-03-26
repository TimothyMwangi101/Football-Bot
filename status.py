"""
Use this file to chech the status of the models
Timothy Mwangi
"""

from openai import OpenAI
from openai.pagination import SyncCursorPage
from openai.types.fine_tuning.fine_tuning_job import FineTuningJob

def read_file(file: str) -> str:
    """Reads txt files"""
    with open(file, 'r', encoding="utf-8") as f:
        return f.read()

key = read_file("API_Key.txt")
client = OpenAI(api_key=key)


def get_models() -> SyncCursorPage[FineTuningJob]:
    """Returns a list of fine tune models"""
    return client.fine_tuning.jobs.list()

def get_successful_models(arr: SyncCursorPage[FineTuningJob]) -> list[str]:
    """Returns only successfully fine-tuned models"""
    return [x.fine_tuned_model for x in arr.data if x.status == "succeeded" and x.fine_tuned_model != None]


def cancel(id: str) -> None:
    """Cancels tuning job given the fine_tuning_job_id"""
    client.fine_tuning.jobs.cancel(id)

print(get_successful_models(get_models()))
