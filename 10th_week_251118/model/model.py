from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel
import os


class PromptModel(BaseModel):
    prompt: str
    temperature: float


class AnswerModel(BaseModel):
    answer: str
    process_time: str


def get_model():
    if os.path.exists("model/gpt2-small"):
        model = AutoModelForCausalLM.from_pretrained("model/gpt2-small")
        tokenizer = AutoTokenizer.from_pretrained("model/gpt2-small")
    else:
        model = AutoModelForCausalLM.from_pretrained("gpt2")
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model.save_pretrained("model/gpt2-small")
        tokenizer.save_pretrained("model/gpt2-small")
    tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer
