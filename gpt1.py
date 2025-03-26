import os
# import json
from dotenv import load_dotenv
from openai import OpenAI
# from helpers import word_count, token_count, is_complete_response, enforce_limits
# from databse.database import load_history, get_last_bot_response, save_history, init_db, clear_history, get_all


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)


# DB_FILE = "chat_history.db"

# HISTORY_FILE = "conversation_history.json"
MORE_DETAILS_TEXT = "Give a littel more details on this"
SUMMARIZE_TEXT = "Summarize this"

LANGUAGE_LEVELS = {
    '5th Grade': 'Respond in very simple language suitable for someone at a 5th-grade reading level. Use short sentences, avoid technical terms, and explain concepts in an easily understandable way.',
    '8th Grade': 'Respond in clear and moderately detailed language suitable for someone at an 8th-grade reading level. Use familiar terms and simplify complex concepts, but provide more detail than at the 5th-grade level.',
    'College': 'Respond with detailed and precise language suitable for someone with a college education. Use technical terms where appropriate and provide well-structured explanations.',
    'Graduate': 'Respond with advanced and highly detailed language suitable for someone with a graduate-level education. Use specialized vocabulary and offer nuanced, in-depth explanations.'
}

# init_db()

# gpt_history = load_history()
history_length = 2
gpt_history = []

# Get the absolute path to the current directory (shesprepared/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'decision-aid-content.txt')


# Saving history in array
def get_last_bot_response():
    """Fetch the last bot response from history array."""
    return gpt_history[-1]['bot'] if gpt_history else "No previous response available."


def load_history(limit=2):  # Reduce if needed
    """Load the last N messages from history array."""
    return gpt_history[-limit:] if gpt_history else []


def save_history(user, bot):
    """Save chat history in memory."""
    gpt_history.append({"user": user, "bot": bot})


# Load decision-aid content
with open(file_path, 'r', encoding='utf-8') as file:
    decision_aid_content = file.read()


def get_gpt_response(user_input, language_level='College'):
    """ Function to get GPT's response based on user input, using detailed prompts."""
    global gpt_history, LANGUAGE_LEVELS
    
    token_count = 200
    last_bot_response = get_last_bot_response()
    
    cur_history = load_history(history_length)
    formatted_history = "\n".join(
        [f"User: {entry['user']}\nChatbot: {entry['bot']}" for entry in cur_history]
    ) if cur_history else ""
    
    if user_input == MORE_DETAILS_TEXT:
        history_entry = {"user": user_input, "bot": None}
        user_input = f"{MORE_DETAILS_TEXT}: {last_bot_response}"
        token_count = 300
    elif user_input == SUMMARIZE_TEXT:
        history_entry = {"user": user_input, "bot": None}
        user_input = f"{SUMMARIZE_TEXT}: {last_bot_response}"
        token_count = 150
    else:
        history_entry = {"user": user_input, "bot": None}
        user_input = formatted_history + "\n" + user_input

    messages = [
        {"role": "system", "content": (
            "You are ShesPrEPared, a friendly assistant focused on HIV prevention and PrEP counseling for women.\n"
            "You help users understand their HIV risks, clarify their values, and provide general information about PrEP.\n"

            "***STRICT GUIDELINES FOR LANGUAGE USE:*** Your response would be thrown out if you do not follow them!!!\n"
            "- **Use short, simple sentences**. No sentence should be more than 15 words long.\n"
            "- **Avoid difficult words and complex phrases**. Use everyday words instead.\n"
            "- **Eliminate technical jargon**. Assume the user has no medical background.\n"
            "- **Do not include unnecessary medical details**. Avoid using abbreviations (use full meaning instead). Skip details about CD4 cells, T-cells, CAB-LA etc.\n"
            "- **Break long sentences into smaller parts** for better readability.\n"
            "- **If summarizing, remove complex words and unnecessary details**.\n"
            "- **Responses should be conversational and easy to understand**.\n\n"

            f"**Strictly follow this rule: {LANGUAGE_LEVELS[language_level]}\n\n**"

            "Response should be markdown format.\n"
            "Be inclusive in your langauge and representative of various backgrounds, open and willing to assist the user and always use friendly language..\n"
            "Avoid introducing fears or stigmas at any point in the discussion.\n"
            # "- Ensure proper indentation for nested lists.\n\n"
            "***Your sentences should be as short as possible else your response would be thrown out the window***.\n"
            # "Keep responses as concise and brief as possible, limiting to 100 tokens. Use clear and direct language. Avoid unnecessary details or verbosity.\n"
            "Ensure responses stay within the token limit while providing the most important information concisely.\n\n"

            "You may want to use the following information for creating your responses (ignore the formatting, since this is copy-pasted):\n\n"
            f"{decision_aid_content}\n\n"
            "**Include references to injectable PrEP as much as possible and avoid always defaulting to oral PrEP.**\n"
           
            # f"**Make sure to list points only or shorten text if user input mentions 'Summarize'. In this case consider the previous response only from chat history**.\n"
            f"Consider the following conversation history as additional context: {formatted_history}.\n\n"
            "If the user diverges from the discussion about HIV/AIDS, bring them back politely.\n\n"
            "**Be sure to answer only the question asked without talking about other possibly related topics**\n"
            "Based on the user's input below, give a concise, straightforward, and clear response."
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

        # if not is_complete_response(gpt_response):
        #     gpt_response += " (Response truncated. Please ask for more details.)"
        
        # gpt_response = enforce_limits(gpt_response)


        history_entry['bot'] = gpt_response
        gpt_history.append(history_entry)
        save_history(user_input, gpt_response)

        return gpt_response
    except Exception as e:
        return f"GPT experienced an internal error: {str(e)}"



if __name__ == '__main__':
    inp = input('Enter Query: \n')
    while inp:
        print(get_gpt_response(inp))
        inp = input('Enter Query: \n')
    # clear_history()
    # print(get_all())