import jwt

SECRET = "secret123"

def verify_token(token):
    try:
        data = jwt.decode(token.split(" ")[1], SECRET, algorithms=["HS256"])
        return data["user"]
    except:
        return "guest"
