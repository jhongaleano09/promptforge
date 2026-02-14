from cryptography.fernet import Fernet
import os
from pathlib import Path

# In a real production app, this should be loaded from a secure environment variable
# or a secure file vault. For this local desktop app, we will store it in a .env file
# or generate it on the fly if missing (persisting it).

SECRET_KEY_FILE = Path(".env")

class SecurityService:
    def __init__(self):
        self._key = self._load_or_generate_key()
        self.fernet = Fernet(self._key)

    def _load_or_generate_key(self) -> bytes:
        # Check environment variable first
        env_key = os.getenv("PROMPTFORGE_SECRET_KEY")
        if env_key:
            return env_key.encode()

        # Check .env file
        if SECRET_KEY_FILE.exists():
            with open(SECRET_KEY_FILE, "r") as f:
                for line in f:
                    if line.startswith("PROMPTFORGE_SECRET_KEY="):
                        return line.strip().split("=")[1].encode()

        # Generate new key
        new_key = Fernet.generate_key()
        # Save to .env (append or create)
        with open(SECRET_KEY_FILE, "a") as f:
            f.write(f"\nPROMPTFORGE_SECRET_KEY={new_key.decode()}\n")
        
        return new_key

    def encrypt_key(self, raw_key: str) -> bytes:
        if not raw_key:
            return b""
        return self.fernet.encrypt(raw_key.encode())

    def decrypt_key(self, encrypted_key: bytes) -> str:
        if not encrypted_key:
            return ""
        return self.fernet.decrypt(encrypted_key).decode()

security_service = SecurityService()
