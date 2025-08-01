from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils import get_next_model, build_bpd_prompt

def build_debate_chain(model_name: str, temperature: float, prompt_text: str) -> LLMChain:
    llm = Ollama(model=model_name, temperature=temperature)
    prompt = PromptTemplate(input_variables=[], template=prompt_text)
    return LLMChain(llm=llm, prompt=prompt)

def generate_uk_debate_speech(topic, context, role="for", task="speech"):
    assert role in ["for", "against"], "Invalid role: must be 'for' or 'against'"
    assert task in ["speech", "rebuttal", "reply"], "Invalid task"

    model = get_next_model(role)
    prompt_text = build_bpd_prompt(topic=topic, context=context, role=role, task=task)

    print(f"[BPD Generator] Generating {task} for {role.upper()} on: {topic}")
    chain = build_debate_chain(model, temperature=0.7, prompt_text=prompt_text)

    return chain.run({})
