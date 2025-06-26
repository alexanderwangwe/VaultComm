from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

BLOCK_SIZE = 16  # AES block size in bytes

def encrypt_message(message: str, key: str) -> str:
    try:
        key = key[:16].encode('utf-8')  # Ensure 16-byte key
        iv = get_random_bytes(BLOCK_SIZE)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(message.encode('utf-8'), BLOCK_SIZE))
        return base64.b64encode(iv + ciphertext).decode('utf-8')
    except Exception as e:
        print("❌ Encryption failed:", e)
        raise ValueError("Encryption failed. Please try again.")

def decrypt_message(encoded_data: str, key: str) -> str:
    try:
        key = key[:16].encode('utf-8')  # Ensure 16-byte key
        data = base64.b64decode(encoded_data)

        if len(data) < 32:
            raise ValueError("Encrypted data too short to contain IV + ciphertext.")

        iv = data[:16]
        ciphertext = data[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

        return plaintext.decode('utf-8')

    except (ValueError, KeyError, base64.binascii.Error) as e:
        print("❌ Decryption failed:", e)
        raise ValueError("Decryption failed: Check if OTP and message are correct.")
