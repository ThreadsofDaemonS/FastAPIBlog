from decouple import config
from google import genai
from google.genai.types import GenerateContentConfig

GOOGLE_API_KEY = config("GOOGLE_API_KEY")

# Initialize the client
client = genai.Client(api_key=GOOGLE_API_KEY)

def is_text_toxic(text: str) -> bool:
    # List of banned words for manual checking
    blacklist = ["dick", "cant", "fuck", "cock", "Bitch", "Whore"]

    # Check for presence of words from the list
    if any(bad_word in text.lower() for bad_word in blacklist):
        print("[MANUAL TOXICITY DETECTED] YES")
        return True

    # If no match, use AI for checking
    prompt = (
        "Determine if the following text is offensive, toxic, or inappropriate. "
        "Answer only 'YES' or 'NO'.\n\n"
        f"Text: {text}"
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
        "Generate a short, relevant reply in English to this comment, considering the post content. "
        "The reply should be simple, sincere, and informal. "
        "No unnecessary explanations, no introductions, no quotes, no formatting. "
        "Write only the reply — one to two sentences maximum.\n\n"
        f"Post: {post_text}\n"
        f"Comment: {comment_text}"
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
        return "Thank you for your comment!"