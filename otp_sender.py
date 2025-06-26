import africastalking
from config import AFRICASTALKING_USERNAME, AFRICASTALKING_API_KEY

# Initialize Africa's Talking
africastalking.initialize(AFRICASTALKING_USERNAME, AFRICASTALKING_API_KEY)
sms = africastalking.SMS

def generate_otp(length=16):
    from secrets import token_hex
    return token_hex(length // 2)

def send_otp_via_sms(phone, otp):
    try:
        message = f"VaultComm OTP: {otp}"
        response = sms.send(message, [phone])
        print("✅ OTP sent successfully:", response)
        return True
    except Exception as e:
        print("❌ SMS failed:", e)
        return False
