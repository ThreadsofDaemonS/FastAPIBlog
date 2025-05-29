from decouple import config
from google import genai
from google.genai.types import GenerateContentConfig

GOOGLE_API_KEY = config("GOOGLE_API_KEY")

# Инициализация клиента
client = genai.Client(api_key=GOOGLE_API_KEY)

def is_text_toxic(text: str) -> bool:
    prompt = (
        "Визнач, чи є наступний текст образливим, токсичним або неприйнятним." 
        "Відповідай тільки 'YES' або 'NO'.\n\n"
        f"Текст: {text}"
    )

    try:
        # Синхронный вызов модели
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=20
            )
        )
        content = response.text.strip()
        print("[AI RESPONSE]", content)
        return "yes" in content.lower()
    except Exception as e:
        print("[AI MODERATION ERROR]", e)
        return False
