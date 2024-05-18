import hashlib

class PasswordManager:
    def hash_password(self, password: str) -> str:
        # Create a SHA-256 hash object
        sha256_hash = hashlib.sha256()

        # Update the hash object with the password (as bytes)
        sha256_hash.update(password.encode())

        # Get the hexadecimal digest of the hash
        hashed_password = sha256_hash.hexdigest()
        return hashed_password

    def verify(self, password, hashed_password):
        if self.hash_password(password) == hashed_password:
            return True
        return False
    
password_manager = PasswordManager()