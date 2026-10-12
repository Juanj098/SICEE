def ok(data=None, status=200):
    return {"data":data, "error": None}, status

def created(data=None):
    return ok(data, 201)
