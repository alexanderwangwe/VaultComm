import tkinter as tk
from tkinter import messagebox
from encryption import encrypt_message
from otp_sender import generate_otp, send_otp_via_sms
from config import RECEIVER_PHONE_NUMBER

class SenderApp:
    def __init__(self, root):
        self.root = root
        root.title("VaultComm - Sender")
        root.geometry("600x500")
        root.config(padx=20, pady=20)

        tk.Label(root, text="Enter Message to Encrypt:").pack()
        self.msg_input = tk.Text(root, height=4)
        self.msg_input.pack()

        # Encrypt Message Button
        tk.Button(root, text="Encrypt Message", command=self.encrypt_msg).pack(pady=5)

        # OTP display and Send button
        self.otp_label = tk.Label(root, text="OTP Key: ")
        self.otp_label.pack()
        tk.Button(root, text="Send OTP via SMS", command=self.send_otp_sms).pack(pady=5)

        # Encrypted Message Output
        tk.Label(root, text="Encrypted Message(Text):").pack()
        self.encrypted_output = tk.Text(root, height=4)
        self.encrypted_output.pack()

        # Copy Buttons
        tk.Button(root, text="Copy Encrypted Text", command=self.copy_encrypted).pack(pady=5)
        tk.Button(root, text="Copy OTP", command=self.copy_otp).pack(pady=2)

        self.generated_otp = ""
        self.encryption_success = False

    def encrypt_msg(self):
        msg = self.msg_input.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showerror("Missing Message", "Please enter a message to encrypt.")
            return

        self.generated_otp = generate_otp()
        self.otp_label.config(text=f"OTP Key: {self.generated_otp}")

        try:
            encrypted = encrypt_message(msg, self.generated_otp)
            self.encrypted_output.delete("1.0", tk.END)
            self.encrypted_output.insert(tk.END, encrypted)
            self.encryption_success = True
            messagebox.showinfo("Encryption Complete", "Message encrypted successfully.\nOTP generated and ready.")
        except Exception as e:
            self.encryption_success = False
            print("❌ Encryption error:", e)
            messagebox.showerror("Encryption Failed", f"Could not encrypt message.\n\nError:\n{e}")

    def send_otp_sms(self):
        if not self.generated_otp:
            messagebox.showwarning("No OTP", "You must encrypt a message before sending the OTP.")
            return

        success = send_otp_via_sms(RECEIVER_PHONE_NUMBER, self.generated_otp)
        if success:
            messagebox.showinfo("OTP Sent", f"OTP sent via SMS to {RECEIVER_PHONE_NUMBER}.")
        else:
            messagebox.showerror("SMS Error", "Failed to send OTP via Africa's Talking.")

    def copy_encrypted(self):
        encrypted_text = self.encrypted_output.get("1.0", tk.END).strip()
        if encrypted_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(encrypted_text)
            messagebox.showinfo("Copied", "Encrypted message copied to clipboard.")

    def copy_otp(self):
        if self.generated_otp:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.generated_otp)
            messagebox.showinfo("Copied", "OTP copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SenderApp(root)
    root.mainloop()
