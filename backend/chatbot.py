import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


SYSTEM_PROMPT = """
You are AgriSense AI, an agricultural assistant.

Your job is to help users with:
- crop diseases
- disease symptoms
- crop care
- prevention
- integrated pest management (IPM)
- general agricultural questions
- safe treatment guidance

Rules:
1. Give clear, practical and farmer-friendly answers.
2. Do not invent pesticide names, doses, registration claims or PHI.
3. Do not claim fertilizer cures a disease.
4. Do not confidently diagnose a disease from text alone.
5. If the user describes symptoms, explain possible causes and recommend visual verification.
6. For chemical treatment, recommend following the product label and local agricultural guidance.
7. If a situation is serious or uncertain, recommend consulting an agricultural expert.
8. Stay focused on agriculture.
9. Do not pretend to have inspected a plant unless an actual image/model result is provided.
10. Keep answers reasonably concise.
"""


def ask_agrisense(question, history=None):

    if not question or not question.strip():
        return "Please ask me an agricultural question."

    history = history or []

    conversation = ""

    for item in history[-10:]:
        role = item.get("role", "")
        content = item.get("content", "")

        if role == "user":
            conversation += f"User: {content}\n"

        elif role == "assistant":
            conversation += f"AgriSense AI: {content}\n"

    conversation += f"User: {question}\nAgriSense AI:"

    prompt = SYSTEM_PROMPT + "\n\nConversation:\n" + conversation

    try:

        response = client.models.generate_content(
           model="gemini-3.5-flash-lite",
            contents=prompt
        )

        answer = response.text

        if not answer:
            return "I couldn't generate a response. Please try again."

        return answer.strip()

    except Exception as error:

        print("Gemini error:", error)

        return (
            "I'm temporarily unable to connect to the AI service. "
            "Please try again in a moment."
        )