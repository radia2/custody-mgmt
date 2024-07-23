import jwt
from datetime import datetime, timezone
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_jwt(payload, private_key):
    try:
        print("Received Private Key:", private_key)
        
        if private_key is None:
            raise ValueError("Private key is missing")

        
        if not private_key.startswith("-----BEGIN PRIVATE KEY-----") or not private_key.endswith("-----END PRIVATE KEY-----"):
            raise ValueError("Private key must have the correct delimiters")
        
        key = serialization.load_pem_private_key(
            private_key.encode(),
            password=None,
            backend=default_backend()
        )
        print("Private Key Loaded Successfully")
        
        headers = {
            "alg": "RS256",
            "typ": "JWT"
        }
        
        print("Payload to Encode:", payload)
        token = jwt.encode(payload, key, algorithm='RS256', headers=headers)
        print("Generated Token:", token)
        
        return {"token": token}
    except Exception as e:
        print("Error during JWT generation:", str(e))
        return {"error": str(e)}
