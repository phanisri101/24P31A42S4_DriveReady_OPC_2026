# Day 2 – AI Agents Training

## Task: Building an Interactive AI Chatbot using OpenAI SDK and Groq

### Objective
To build an interactive AI-powered customer support chatbot for Sweet Crumbs Home Bakery using the OpenAI SDK with the Groq API.

### Technologies Used
- Python
- OpenAI SDK
- Groq API
- Google Colab
- JSON
- Large Language Models (LLMs)

### 1. Install Required Library

```python
!pip install -q openai
```

### 2. Connect to Groq API

```python
from google.colab import userdata
from openai import OpenAI

client = OpenAI(
    api_key=userdata.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": "You are a funny joker"},
        {"role": "user", "content": "Tell me a joke"}
    ]
)

print(response.choices[0].message.content)
```

### 3. Define System Prompt

```python
SYSTEM = """ROLE: You are the assistant for Sweet Crumbs Home Bakery.
FACTS: We bake to order. Orders need 24 hours' notice.
All cakes have eggless versions.
Plum cake Rs 500. Chocolate cake Rs 650. Cupcake Rs 80.
RULES: Never promise a delivery time.
If the answer isn't in FACTS, say "I'll check with the owner."
FORMAT: Under 50 words, friendly, English or Telugu matching the customer."""
```

### 4. Create Menu Using Dictionary

```python
MENU = {
    "plum cake": 500,
    "chocolate cake": 650,
    "cupcake": 80
}

print(MENU.get("donut", "Donuts not available"))
```

### 5. Create an Order Using Dictionary

```python
order = {
    "name": "Ravi",
    "item": "plum cake",
    "qty": 2,
    "eggless": True
}

total = order["qty"] * MENU[order["item"]]

print("Total Price:", total)
```

### 6. JSON Serialization and Deserialization

```python
import json

text = json.dumps(order)
back = json.loads(text)

print(text)
print(back)
```

### 7. Create Price Calculation Function

```python
def get_price(item: str, qty: int = 1) -> int:
    return MENU[item.lower().strip()] * qty

print(get_price("cupcake", 6))
print(get_price("Plum Cake"))
```

### 8. Exception Handling

```python
try:
    a = 10
    print(a + b)
    print("hi")

except:
    print("b is not defined")
```

### 9. Build an Interactive AI Chatbot

```python
import json
import functools
from openai import RateLimitError, APIConnectionError

MODEL = "openai/gpt-oss-120b"

MENU = {
    "plum cake": 500,
    "chocolate cake": 650,
    "cupcake": 80
}

SYSTEM = f"""ROLE: You are the friendly assistant for Sweet Crumbs Home Bakery.
FACTS: Menu with prices in rupees: {json.dumps(MENU)}
Orders need 24 hours' notice. All cakes have eggless versions.
RULES: Never promise a delivery time.
If it isn't in FACTS, say "I'll check with the owner."
Remember the customer's name and order during the chat.
FORMAT: Under 50 words, friendly, English or Telugu matching the customer."""

# Logging Decorator
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[log] {func.__name__}{args} -> {result!r}")
        return result
    return wrapper

# Price Calculation
@log_call
def get_price(item: str, qty: int = 1) -> int:
    return MENU[item.lower().strip()] * qty

# Chat History
history = [{"role": "system", "content": SYSTEM}]
MAX_TURNS = 8

# Chat Function
def chat(user_text: str) -> str:

    history.append({"role": "user", "content": user_text})

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

    history.append({"role": "assistant", "content": reply})

    return reply

# Interactive Chatbot
while True:

    text = input("You: ")

    if text.lower().strip() in ("bye", "exit", "quit"):
        print("Bot: Thank you for visiting Sweet Crumbs!")
        break

    print("Bot:", chat(text))
```

### Implementation Explanation

1. **OpenAI SDK with Groq:** Used to connect to the Groq API and communicate with the LLM.
2. **System Prompt:** Defines the chatbot's role, bakery information, rules and response format.
3. **Dictionary:** Stores bakery menu items and their prices.
4. **JSON:** Converts Python dictionaries into JSON strings and back.
5. **Functions:** Calculates the total price based on the item and quantity.
6. **Decorators:** Uses a logging decorator to display function calls and their results.
7. **Exception Handling:** Handles API rate-limit and connection errors.
8. **Chat History:** Stores previous user and assistant messages to maintain conversational context.
9. **Interactive Chatbot:** Continuously accepts user questions and generates responses until the user exits.

### Conclusion

Successfully developed an interactive AI chatbot for Sweet Crumbs Home Bakery using the OpenAI SDK and Groq API. Implemented Python data structures, JSON handling, functions, decorators, exception handling and conversational memory.

### Learning Outcomes

- Learned to connect Groq API using the OpenAI SDK.
- Understood system prompts and LLM responses.
- Practiced Python dictionaries and JSON operations.
- Learned functions and decorators.
- Understood exception handling.
- Implemented chat history and conversational memory.
- Built an interactive AI-powered chatbot.
