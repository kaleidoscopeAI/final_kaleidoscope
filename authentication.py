from fastapi import HTTPException
import jwt
import time

SECRET_KEY = "YOUR_SECRET_KEY"

class AuthManager:
    def login(self, credentials: dict) -> dict:
        # Dummy login: in production, validate against a database
        username = credentials.get("username")
        password = credentials.get("password")
        if username == "admin" and password == "password":
            token = jwt.encode({"username": username, "exp": time.time() + 3600}, SECRET_KEY, algorithm="HS256")
            return {"status": "success", "token": token}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

