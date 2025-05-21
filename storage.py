# storage.py
import json
from pathlib import Path

SEEN_FILE = Path("seen_ids.json")
PRICE_FILE = Path("price_history.json")

def load_seen_ids():
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()

def save_seen_ids(seen):
    SEEN_FILE.write_text(json.dumps(list(seen)))

def load_price_history():
    if PRICE_FILE.exists():
        return json.loads(PRICE_FILE.read_text())
    return {}

def update_price_history(history, message):
    from filters import extract_price

    text = message.message
    price = extract_price(text)
    if not price:
        return

    for word in text.split():
        if word.lower() in history:
            history[word.lower()].append(price)
            break
    else:
        for keyword in history.keys():
            if keyword in text.lower():
                history[keyword].append(price)
                break

    PRICE_FILE.write_text(json.dumps(history))
