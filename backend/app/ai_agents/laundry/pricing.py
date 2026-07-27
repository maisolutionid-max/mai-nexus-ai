
PRICE_LIST = {
    "regular": 7000,
    "express": 12000,
    "premium": 18000
}


def calculate_price(
    service_type: str,
    weight: float
):

    price = PRICE_LIST.get(
        service_type.lower(),
        7000
    )

    return price * weight
