
import os
import json
import functools

from openai import OpenAI, RateLimitError, APIConnectionError

# Connect to Groq API
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-120b"

# Bakery Menu
MENU = {
    "plum cake": 500,
    "chocolate cake": 650,
    "cupcake": 80
}

# System Prompt
SYSTEM = f"""
ROLE: You are the friendly assistant for Sweet Crumbs Home Bakery.

FACTS:
Menu with prices in rupees: {json.dumps(MENU)}
Orders need 24 hours' notice.
All cakes have eggless versions.

RULES:
Never promise a delivery time.
If it isn't in FACTS, say "I'll check with the owner."
Remember the customer's name and order during the chat.

FORMAT:
Under 50 words, friendly, English or Telugu matching the customer.
"""

# Decorator for Logging
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[log] {func.__name__}{args} -> {result!r}")
        return result
    return wrapper


# Price Calculation Function
@log_call
def get_price(item: str, qty: int = 1) -> int:
    """Return the total price in rupees for an item."""
    return MENU[item.lower().strip()] * qty


# Chat History
history = [
    {"role": "system", "content": SYSTEM}
]

MAX_TURNS = 8


# Chatbot Function
def chat(user_text: str) -> str:

    history.append({
        "role": "user",
        "content": user_text
    })

    recent = [history[0]] + history[1:][-MAX_TURNS:]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=recent,
            temperature=0.3
        )

        reply = response.choices[0].message.content

    except RateLimitError:
        reply = "We're a little busy. Please try again in a minute."

    except APIConnectionError:
        reply = "I can't reach the server right now. Please try again shortly."

    history.append({
        "role": "assistant",
        "content": reply
    })

    return reply


# Interactive Chatbot
if __name__ == "__main__":

    print("Welcome to Sweet Crumbs Home Bakery!")
    print("Type 'bye', 'exit' or 'quit' to stop.\n")

    while True:

        text = input("You: ")

        if text.lower().strip() in ("bye", "exit", "quit"):
            print("Bot: Thank you for visiting Sweet Crumbs!")
            break

        print("Bot:", chat(text))
