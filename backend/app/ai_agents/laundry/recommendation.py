def generate_recommendation(data):

    weight = data.get(
        "weight",
        0
    )

    if weight >= 10:
        return "Recommend bulk discount."

    if weight >= 5:
        return "Recommend loyalty points."

    return "Standard service."
