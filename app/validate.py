def validateAdd(body):
    error = []
    if "link" not in body:
        error.append("Image link missing")
    if "cost" not in body:
        error.append("Cost missing")
    else:
        try:
            val = int(body["cost"])
            if val < 0:
                error.append("Cost must be positive")
        except ValueError:
            error.append("Cost must be an integer in cents")
    return ", ".join(error)
