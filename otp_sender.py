from twilio.rest import Client
from secrets import token_hex
from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

def generate_otp(length=16) -> str:
    """
    Generates a secure hexadecimal OTP key of given length.
    Default is 16 characters for AES-128 compatibility.
    """
    return token_hex(length // 2)  # 16 hex chars = 8 bytes = 64 bits

def send_otp_via_sms(recipient_phone: str, otp_key: str) -> str:
    """
    Sends the OTP via SMS to the recipient using Twilio API.
    """
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your VaultComm OTP key: {otp_key}",
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_phone
        )
        print("✅ OTP sent via SMS. SID:", message.sid)
        return message.sid
    except Exception as e:
        print("❌ Error sending SMS:", e)
        return ""

#test the OTP generation and sending
# configure twilio credentials in config.py and sender receiver messaging
if __name__ == "__main__":
    phone = input("Enter recipient phone number (e.g. +2547xxxxxxx): ")
    otp = generate_otp()
    print("Generated OTP:", otp)
    send_otp_via_sms(phone, otp)
