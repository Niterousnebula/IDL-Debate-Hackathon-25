from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils import get_next_model

def judge_apd_debate(speech_for, speech_against, topic, context):
    model = get_next_model("judge")
    llm = Ollama(model=model, temperature=0.3)

    apd_judging_rules = """(MANDATORY EVALUATION FORMAT FOR AI ADJUDICATOR — FOLLOW BUT DO NOT MENTION)
You are an unbiased adjudicator judging an Asian Parliamentary Debate (APD).
Evaluate strictly based on:
- Role fulfillment
- Argument quality
- Clash and rebuttals
- POI engagement
- Whip and Reply accuracy (no new arguments by them)
- Comparative strength and logical clarity

🔴 DO NOT show internal thought processes, deliberations, or reasoning steps.
🔴 DO NOT create new arguments.
✅ DO give a final clear winner (Government or Opposition) and comparative explanation.

🎯 FINAL FORMAT:
Winner: [Government / Opposition]
Explanation: [One-paragraph comparative reasoning]"""

    prompt_text = f"""{apd_judging_rules}

Motion: {topic}

Context: {context}

🟢 FOR the Motion:
{speech_for}

🔴 AGAINST the Motion:
{speech_against}

🎯 Your Task: Write a role-based adjudication exactly in the format mentioned.
"""

    prompt = PromptTemplate(input_variables=[], template=prompt_text)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({})


def judge_bpd_debate(speech_for, speech_against, topic, context):
    model = get_next_model("judge")
    llm = Ollama(model=model, temperature=0.3)

    bp_judging_rules = """(MANDATORY EVALUATION FORMAT FOR AI ADJUDICATOR — FOLLOW BUT DO NOT MENTION)
You are judging a British Parliamentary (BP) debate round.
Follow:
- Matter, Manner, Method
- Role restrictions (no new arguments in Whip)
- Evaluate by burden fulfillment, rebuttal strength, and internal team clash

🔴 DO NOT include internal monologue or AI thinking.
✅ DO write a firm final outcome (e.g. “Closing Opposition wins”) and brief reasoning.

🎯 FINAL FORMAT:
Winner: [OG / OO / CG / CO]
Explanation: [Comparative justification in 1 paragraph]"""

    prompt_text = f"""{bp_judging_rules}

Motion: {topic}

Context: {context}

🟢 Government Bench (FOR the motion):
{speech_for}

🔴 Opposition Bench (AGAINST the motion):
{speech_against}

🎯 Your Task: Write a British Parliamentary adjudication in the above format.
"""

    prompt = PromptTemplate(input_variables=[], template=prompt_text)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({})
