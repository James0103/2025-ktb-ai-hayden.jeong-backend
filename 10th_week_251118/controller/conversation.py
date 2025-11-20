from model.model import PromptModel, AnswerModel
from model.model import get_model
import time


def generate_text(user_input: PromptModel) -> AnswerModel:
    start_time = time.time()
    model, tokenizer = get_model()
    # 텍스트 생성
    inputs = tokenizer(user_input.prompt, return_tensors="pt", padding=True)

    # 생성 파라미터 설정
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=20,
        min_new_tokens=5,
        num_return_sequences=1,
        temperature=user_input.temperature if user_input.temperature > 1.0 else 1.0,
        top_k=50,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        early_stopping=True,
        no_repeat_ngram_size=2
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return AnswerModel(answer=answer, process_time=f"answer generation time : {(time.time() - start_time):.2f}초")
