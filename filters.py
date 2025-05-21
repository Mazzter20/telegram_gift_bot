# filters.py
import re

def extract_price(text):
    prices = [float(p[1:]) for p in re.findall(r'\$\d+', text)]
    return min(prices) if prices else None

def is_good_deal(message, price_history, filters):
    text = message.message
    price = extract_price(text)

    if not price:
        return False

    if filters['max_price'] and price > filters['max_price']:
        return False

    if not any(k.lower() in text.lower() for k in filters['keywords']):
        return False

    key = next((k.lower() for k in filters['keywords'] if k.lower() in text.lower()), None)
    if not key:
        return False

    previous_prices = price_history.get(key, [])
    if previous_prices:
        avg_price = sum(previous_prices) / len(previous_prices)
        discount = ((avg_price - price) / avg_price) * 100
        if discount < filters['min_discount']:
            return False

    return True

def update_user_filters(filters, keywords, max_price, min_discount):
    filters['keywords'] = [k.strip() for k in keywords if k.strip()]
    filters['max_price'] = max_price if max_price else None
    filters['min_discount'] = min_discount
