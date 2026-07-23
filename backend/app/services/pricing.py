def calculate_price(service: str, weight: float):

    prices = {
        "cuci": 7000,
        "express": 12000,
        "dryclean": 25000
    }

    price_per_kg = prices.get(service.lower(), 7000)

    return weight * price_per_kg
