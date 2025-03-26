
MAX_WORDS = 600
MAX_TOKENS = 100000

def word_count(text):
    return len(text.split())


def token_count(text):
    # Approximate token count by splitting on spaces. OpenAI has a more precise tokenization tool.
    return len(text.split())


def is_complete_response(text):
    return text.strip()[-1] in [".", "!", "?"]


def enforce_limits(response):
    words = response.split()
    tokens = token_count(response)

    if len(words) > MAX_WORDS or tokens > MAX_TOKENS:
        truncated_response = " ".join(words[:MAX_WORDS]) + "..."
        return truncated_response + "\n\nPlease let me know if you'd like more details!"
    return response
