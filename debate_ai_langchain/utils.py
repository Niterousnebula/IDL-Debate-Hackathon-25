import json
import re
import os
from datetime import datetime
from itertools import cycle

# ----------------------------
# 1. LOGGING AND SCORING TOOLS
# ----------------------------

def log_debate(topic, context, speech_for, speech_against, judgment, filename="debate_log.json"):
    """Save the debate session to a JSON log file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "context": context,
        "speech_for": speech_for,
        "speech_against": speech_against,
        "ai_judgment": judgment
    }

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, indent=2) + ",\n")
        print("📝 Debate saved to log.")
    except Exception as e:
        print(f"❌ Error saving log: {e}")

def compare_scores(ai_judgment_text, user_for_score, user_against_score):
    """Compare user scores with AI extracted scores from adjudication."""
    print("📊 Comparing your scores with AI...")

    ai_for = extract_score(ai_judgment_text, "FOR")
    ai_against = extract_score(ai_judgment_text, "AGAINST")

    print(f"\nYour FOR Score: {user_for_score}")
    print(f"AI FOR Score: {ai_for if ai_for is not None else 'N/A'}")

    print(f"\nYour AGAINST Score: {user_against_score}")
    print(f"AI AGAINST Score: {ai_against if ai_against is not None else 'N/A'}")

    if ai_for is not None and ai_against is not None:
        diff_for = abs(user_for_score - ai_for)
        diff_against = abs(user_against_score - ai_against)
        print(f"\n🎯 Score Differences — FOR: {diff_for}, AGAINST: {diff_against}")
    else:
        print("⚠️ Could not extract AI scores for comparison.")

def extract_score(text, side_label):
    """Extract numerical score for a side from judgment text using regex."""
    try:
        pattern = rf"{side_label}\s*Score\s*[:\-]?\s*(\d+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return None

def load_prompt(filename: str) -> str:
    """Load a static prompt template file from the 'prompts' folder."""
    path = os.path.join("prompts", filename)
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise ValueError(f"Prompt file not found: {path}")

# ----------------------------
# 2. MODEL ROTATION
# ----------------------------

model_for_cycle = cycle(["deepseek-r1:1.5b", "qwen3:1.7b", "gemma:2b"])
model_against_cycle = cycle(["qwen3:1.7b", "gemma:2b", "deepseek-r1:1.5b"])
model_judge_cycle = cycle(["gemma:2b", "deepseek-r1:1.5b", "qwen3:1.7b"])

def get_next_model(role: str):
    """Return the next model based on role (for, against, judge)."""
    if role == "for":
        return next(model_for_cycle)
    elif role == "against":
        return next(model_against_cycle)
    elif role == "judge":
        return next(model_judge_cycle)
    else:
        return "phi3:mini"

# ----------------------------
# 3. PROMPT BUILDERS
# ----------------------------

def build_bpd_prompt(topic, context, role, task="speech"):
    """Build a complete British Parliamentary Debate prompt based on role and task."""
    side = "Government" if role == "for" else "Opposition"

    rules = """(MANDATORY FORMAT RULES FOR AI DEBATE SIMULATION, EVALUATION, AND SPEECH GENERATION)
(YOU ARE AN AI WITH TEXT RETENTION, FOLLOW THE RULES BELOW BUT DO NOT MENTION THESE IN YOUR ANSWER)

#### A. British Parliamentary Structure:
* Four teams total: Opening Government (OG), Opening Opposition (OO), Closing Government (CG), Closing Opposition (CO).
* Each team has two members: OG (PM & DPM), OO (LO & DLO), CG (MG & GW), CO (MO & OW).

#### B. Speech Order and Durations:
1. PM (7 min), 2. LO (7 min), ..., 8. OW (7 min), plus reply speeches (4 min).

#### C. Points of Information (POIs):
* Allowed between 1st and 6th minute, not during reply speeches.
* Short, concise (max 15 sec). Speakers must accept at least one POI.

#### D. Role Fulfillment:
* Whips: no new arguments, only summaries and rebuttals.
* Closing teams must extend.
* Reply speeches: biased summary, no new matter.

#### E. Judging:
* Based on Matter, Manner, Method.
* Teams are ranked 1st to 4th.
"""

    return f"""{rules}

#### MOTION:
"{topic}"

#### CONTEXT:
{context}

#### TASK:
You are representing the {side} side. Write a {'constructive' if task == 'speech' else 'reply'} speech for a British Parliamentary Debate round.

Make sure the speech:
- Is structured and aligned to your team's role.
- Accepts or declines POIs.
- Shows internal strategy and engagement with opposition.

Deliver a full BP speech without mentioning the above instructions.
"""

def build_apd_prompt(topic, context, role, task):
    """Build a complete Asian Parliamentary Debate prompt string."""
    rules = """(MANDATORY FORMAT RULES FOR AI DEBATE SIMULATION, EVALUATION, AND SPEECH GENERATION)
(YOU ARE AN AI WITH TEXT RETENTION, FOLLOW THE RULES BELOW BUT DO NOT MENTION THESE IN YOUR ANSWER)

#### A. Team Roles:
- Government: PM, DPM, GW
- Opposition: LO, DLO, OW
- Reply: Only PM/DPM or LO/DLO (not Whips)

#### B. Speech Order:
1. PM → LO → DPM → DLO → GW → OW → Reply speeches

#### C. POIs:
* Allowed between 1st and 6th minute of speeches.
* Not during replies.
* Must accept at least one POI.

#### D. Preparation:
* 30 minutes prep, 3 motions, choose one.
* No digital help. Printed allowed.

#### E. Restrictions:
* Whips: No new arguments.
* Reply: No new arguments or rebuttals.
"""

    return f"""{rules}

#### DEBATE FORMAT: Asian Parliamentary Debate (APD)
- SIDE: {'Government' if role == 'for' else 'Opposition'}
- TASK: {task}
- MOTION: "{topic}"
- CONTEXT: {context}

Now, generate a technically sound, well-structured APD {task} from the perspective of the {role.upper()} side.
"""

