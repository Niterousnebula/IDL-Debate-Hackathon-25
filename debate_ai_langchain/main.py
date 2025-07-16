from agents.debater_uk import generate_uk_debate_speech
from agents.debater_asia import generate_asia_debate_speech
from agents.adjudicator import judge_apd_debate, judge_bpd_debate
from utils import log_debate, compare_scores

def main():
    print("🎙️ Welcome to AI Debate Simulator!")
    print("------------------------------")

    # Step 1: Format selection
    format_choice = input("Choose debate format (BP or AP): ").strip().upper()
    if format_choice not in ["BP", "AP"]:
        print("❌ Invalid format. Please choose 'BP' or 'AP'.")
        return

    # Step 2: Topic and context input
    topic = input("\n📝 Enter the debate topic: ").strip()
    context = input("🗂️ Enter the context/background (optional): ").strip()

    print("\n🧠 Generating speeches...\n")

    # Step 3: Speech generation
    if format_choice == "BP":
        speech_for = generate_uk_debate_speech(topic, context, role="for")
        speech_against = generate_uk_debate_speech(topic, context, role="against")
    else:
        speech_for = generate_asia_debate_speech(topic, context, role="for")
        speech_against = generate_asia_debate_speech(topic, context, role="against")

    print("🟢 FOR the Motion:\n")
    print(speech_for, "\n")

    print("🔴 AGAINST the Motion:\n")
    print(speech_against, "\n")

    # Step 4: AI Adjudication
    print("🧑‍⚖️ Judging the debate...\n")
    if format_choice == "BP":
        judgment = judge_bpd_debate(speech_for, speech_against, topic, context)
    else:
        judgment = judge_apd_debate(speech_for, speech_against, topic, context)

    print("🤖 AI Judgment:\n")
    print(judgment)

    # Step 5: Optional human judging
    print("\n📋 Your Turn to Judge:")
    try:
        user_for = int(input("Your score for FOR speaker (0–100): "))
        user_against = int(input("Your score for AGAINST speaker (0–100): "))
        compare_scores(judgment, user_for, user_against)
    except ValueError:
        print("⚠️ Invalid score input. Skipping human judging.")

    # Step 6: Save to file
    log_debate(topic, context, speech_for, speech_against, judgment)
    print("\n✅ Debate session saved successfully.\n")

if __name__ == "__main__":
    main()
