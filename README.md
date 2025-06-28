# VaultComm

VaultComm is a secure message exchange application that uses AES encryption and OTP (One-Time Password) for message confidentiality. The sender encrypts a message with a randomly generated OTP, sends the OTP via SMS, and the receiver decrypts the message using the OTP.

## Features

- **AES Encryption**: Messages are encrypted using AES (CBC mode) with a 16-byte OTP as the key.
- **OTP Generation**: Secure OTPs are generated for each message.
- **SMS Delivery**: OTPs are sent to the receiver via Africa's Talking SMS API.
- **User-Friendly GUI**: Both sender and receiver interfaces are built with Tkinter for ease of use.
- **Clipboard Support**: Easily copy and paste encrypted messages and OTPs.

## Libraries Used

- **tkinter**: Provides the graphical user interface for both sender and receiver applications.
- **pycryptodome**: Supplies cryptographic primitives, specifically AES encryption/decryption and secure random number generation.
- **africastalking**: Used to send OTPs via SMS to the receiver's phone number.
- **base64**: Encodes and decodes binary data (IV and ciphertext) to text for easy transfer.
- **secrets**: Generates cryptographically secure OTPs.

## How It Works

1. **Sender Side**:
    - User enters a message.
    - Application generates a secure OTP.
    - Message is encrypted using AES with the OTP as the key.
    - OTP is sent to the receiver via SMS.
    - Encrypted message can be copied and sent to the receiver.

2. **Receiver Side**:
    - User pastes the encrypted message and OTP.
    - Application decrypts the message using the provided OTP.

## Setup

1. **Install Dependencies**:
    ```
    pip install -r requirements.txt
    ```

2. **Configure Africa's Talking**:
    - Edit `config.py` with your Africa's Talking username, API key, and receiver's phone number.

## Running the Application

- **Sender UI**:
    ```
    python sender_ui.py
    ```
- **Receiver UI**:
    ```
    python receiver_ui.py
    ```

## Testing

To test the application:

1. Run `sender_ui.py` and enter a message.
2. Click "Encrypt Message" to generate an OTP and encrypted message.
3. Click "Send OTP via SMS" (ensure your Africa's Talking credentials are valid).
4. Copy the encrypted message.
5. Run `receiver_ui.py`, paste the encrypted message and OTP.
6. Click "Decrypt Message" to view the original message.

Note : that this runs as a demo and thus uses Africa's talking sandbox mode(sms is viewed in the simulator).
If you want to test without SMS, manually copy the OTP from the sender UI to the receiver UI.

---
![Screenshot 2025-06-28 140536](https://github.com/user-attachments/assets/7650a728-c043-41c9-bf16-61360056da7e)
<img width="478" alt="image" src="https://github.com/user-attachments/assets/f2af799a-118d-4ecb-aa49-f958de7e9707" />



**Note:** This project is for educational purposes. Do not use in production without proper security review.
