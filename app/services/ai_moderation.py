from decouple import config
from google import genai
from google.genai.types import GenerateContentConfig

GOOGLE_API_KEY = config("GOOGLE_API_KEY")

# Ініціалізація клієнта
client = genai.Client(api_key=GOOGLE_API_KEY)

def is_text_toxic(text: str) -> bool:
    prompt = (
        "Визнач, чи є наступний текст образливим, токсичним або неприйнятним. "
        "Відповідай тільки 'YES' або 'NO'.\n\n"
        f"Текст: {text}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=20
            )
        )
        content = response.text.strip()
        print("[AI TOXICITY RESPONSE]", content)
        return "yes" in content.lower()
    except Exception as e:
        print("[AI MODERATION ERROR]", e)
        return False


def generate_reply(post_text: str, comment_text: str) -> str:
    prompt = (
        "Сформуй коротку, релевантну відповідь українською мовою на цей коментар, враховуючи зміст поста. "
        "Відповідь має бути простою, щирою, неформальною. "
        "Без зайвих пояснень, без вступів, без лапок, без форматування. "
        "Пиши лише відповідь — одне-два речення максимум.\n\n"
        f"Пост: {post_text}\n"
        f"Коментар: {comment_text}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=50
            )
        )
        reply = response.text.strip()
        print("[AI REPLY GENERATED]", reply)
        return reply
    except Exception as e:
        print("[AI REPLY ERROR]", e)
        return "Дякую за ваш коментар!"
