from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

BLOCK_SIZE = 16  # AES block size (bytes)

def format_key(key: str) -> bytes:
    """
    Formats the key to ensure it is exactly 16 bytes (AES-128).
    Pads with zeros if too short, trims if too long.
    """
    return key.ljust(16, '0').encode('utf-8')[:16]

def encrypt_message(message: str, key: str) -> str:
    """
    Encrypts a plaintext message using AES with the provided key.
    Returns the base64-encoded string (IV + ciphertext).
    """
    key = format_key(key)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), BLOCK_SIZE))
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt_message(encoded_data: str, key: str) -> str:
    """
    Decrypts a base64-encoded AES-encrypted message using the provided key.
    Returns the original plaintext.
    """
    key = format_key(key)
    data = base64.b64decode(encoded_data)
    iv = data[:BLOCK_SIZE]
    ciphertext = data[BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
    return plaintext.decode('utf-8')


# Example usage
if __name__ == "__main__":
    key = "mysecretotp1234"  # Even if short, it'll be padded safely

    msg = "Hello from VaultComm!"

    encrypted = encrypt_message(msg, key)
    print("Encrypted:", encrypted)

    decrypted = decrypt_message(encrypted, key)
    print("Decrypted:", decrypted)
