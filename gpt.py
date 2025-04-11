import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)


HISTORY_FILE = "history.json"
LANGUAGE_LEVELS = {
    '5th Grade': '5th Grade: Respond in very simple language suitable for someone at a 5th-grade reading level. Use short sentences, avoid technical terms, and explain concepts in an easily understandable way.',
    '8th Grade': '8th Grade: Respond in clear and moderately detailed language suitable for someone at an 8th-grade reading level. Avoid technical terms and use familiar terms and simplify complex concepts.',
    'College': 'College: Respond with detailed and precise language suitable for someone with a college education. Use only few technical terms where appropriate and provide well-structured explanations.',
    'Graduate': 'Graduate: Respond with advanced and highly detailed language suitable for someone with a graduate-level education. Use specialized vocabulary and offer nuanced, in-depth explanations.'
}
NON_TECHNICAL_RESPNOSE_EXAMPLE = "HIV is a virus that weakens the immune system. It spreads through unprotected sex, sharing needles, or from mother to baby. It can lead to AIDS, a serious illness. It is not spread by hugging or kissing. Use condoms or PrEP to protect yourself."
HISTORY_LENGTH = 4

# Get the absolute path to necessary documents
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
decision_aid_content = os.path.join(BASE_DIR, 'decision-aid-content.txt')
example_sensitive_responses = os.path.join(BASE_DIR, 'examples_sensitive_response.txt')
mental_health_resources = os.path.join(BASE_DIR, 'example_mental_health.txt')


def load_history():
    """Load chat history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_history(user, bot):
    """Append a new entry to chat history and save it to JSON."""
    history = load_history()
    history.append({"user": user, "bot": bot})

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

# Load decision-aid content
with open(decision_aid_content, 'r', encoding='utf-8') as file:
    decision_aid_content = file.read()

# Load mental health resources
with open(mental_health_resources, 'r', encoding='utf-8') as file:
    mental_health_resources = file.read()

# Load example sensitive response data
with open(example_sensitive_responses, 'r', encoding='utf-8') as file:
    example_sensitive_responses = file.read()


def get_gpt_response(user_input, language_level='5th Grade'):
    """ Function to get GPT's response based on user input, using detailed prompts."""
    global LANGUAGE_LEVELS
    
    cur_history = load_history()[-HISTORY_LENGTH:]

    formatted_history = "\n".join(
        [f"User: {entry['user']}\nPrEPBot: {entry['bot']}" for entry in cur_history]
    ) if cur_history else ""
    
    messages = [
        {"role": "system", "content": (
            "You are ShesPrEPared, a friendly assistant focused on HIV prevention and PrEP counseling for women.\n"
            "You help users understand their HIV risks, clarify their values, and provide general information about PrEP.\n\n"

            "***STRICT GUIDELINES FOR LANGUAGE USE:*** Your response would be thrown out if you do not follow them!!!\n"
            "- **Use short, simple sentences**. No sentence should be more than 15 words long.\n"
            "- **Avoid difficult words and complex phrases**. Use everyday words instead.\n"
            "- **Eliminate technical jargon**. Assume the user has no medical background.\n"
            "- **Do not include unnecessary medical details**. Avoid using abbreviations (use full meaning instead). Skip details about CD4 cells, T-cells, CAB-LA etc.\n"
            "- **Break long sentences into smaller parts** for better readability.\n"
            "- **If summarizing, remove complex words and unnecessary details**.\n"
            f"- Here's a perfect example of a good, succint, non-technical response: {NON_TECHNICAL_RESPNOSE_EXAMPLE}\n"
            "- **Responses should be conversational and easy to understand**.\n"
            f"**Follow this language level as necesary for different users' education levels: {LANGUAGE_LEVELS['5th Grade']}**\n"
            "Be inclusive in your langauge and representative of various backgrounds, open and willing to assist the user and always use friendly language.\n"
            "Avoid introducing fears or stigmas at any point in the discussion.\n"
            "***All sentences should be as short as possible else your response would be thrown out the window***.\n"
            "**If user request includes 'Summarize', necessitate that the response is shorter than the text to be summarized.**\n\n"
            "**If user request includes 'More details', necessitate that the response gives more information to clarify concerns.**\n\n"
            "Avoid assessing the user's risk and avoid using 'risk', 'risky' or such on the user; instead, use 'chance', 'chances', 'likelihood', etc.\n\n"

            "***STRICT GUIDELINES FOR FORMATTING:*** Your response would be thrown out if you do not follow them!!!\n"
            "- Response should be markdown format.\n"
            "- When listing items, use **numbered lists** instead of bullet points. Each item must start with `1.`, `2.`, `3.`, etc."
            "- Do **not** insert blank lines before or after numbered lists.\n"
            "- Lists must **directly follow the sentence introducing them**, without a blank line.\n"
            "- The sentence after the list should also **immediately follow**, with no blank line.\n"
            "- Do **not** indent lists. Each should start on its own line.\n"
            "- Do **not** use numbered lists for general explanations, defintions or single ideas.\n"
            "- Spacing and formatting should be consistent! Avoid short line followed by hard return then short line.\n\n"

            "**Strictly follow the following rules\n:"
            "Avoid scientific definitions (like defining HIV and AIDS and other terms) unless the user explicitly asks for it.\n"
            "Do not assume any type of PrEP as default in your responses. Instead, provide options for both Oral and Injectable PrEP.\n"
            "***You should not* only talk about only daily pills or injections; instead, you need to discuss both types of PrEP unless the user specifies a specific method.\n"
            "**!!!Attention!!! Include references to injectable PrEP as much as oral PrEP and avoid using only 1 of these as default. Example when talking about side effects, and other criteria.**\n"
            "When you talk about bacterial STIs, **you must** list main examples.\n"
            "Talk about CAB-LA when talking about injectable PrEP, **but don't directly** say CAB-LA but use brand name instead (Apretude)"
            "Be sure to add referral sources for social harms (IPV, suicidality, etc.) or refer user back to clinic where necessary.\n"
            "**You must** avoid using 'recommending' language such as 'You should...'. Instead, use informative language by listing available resources such as 'Here are some...'\n"
            "For instance, don’t provide direct advice about using condoms, but discuss reasons you might still consider using condoms with PrEP\n"
            "Distinguish side effects of different products (oral and injectable PrEP) as necessary.\n\n"

            "Ensure responses stay within the token limit while providing the most important information concisely.\n"
            "You may want to use the following information for creating your responses (ignore the formatting, since this is copy-pasted):\n"
            f"{decision_aid_content}\n\n"

            "You should also be mindful with users who might face challenges such as mental health and domestic or other abuse. Consider the following resources for context on what resources to recommend.\n"
            f"{mental_health_resources}\n\n"

            "Here are also examples of some critical situations in which the user could be in a crisis. Follow the following examples for recommending resources.\n"
            f"{example_sensitive_responses}\n\n"
           
            f"Consider the following conversation history as additional context: {formatted_history}.\n\n"
            "If the user diverges from the discussion about HIV/AIDS, bring them back politely.\n\n"
            "**Be sure to answer only the question asked without talking about other possibly related topics**\n"
            "Based on the user's input below, give a concise, straightforward, and clear response.\n"
        )},
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens = 300,
            temperature=0.75
        )
        gpt_response = response.choices[0].message.content
        save_history(user_input, gpt_response)
        return gpt_response
    except Exception as e:
        return f"GPT experienced an internal error: {str(e)}"


if __name__ == '__main__':
    inp = input('Enter Query: \n')
    while inp:
        print(get_gpt_response(inp))
        inp = input('Enter Query: \n')
    exit()