import tkinter as tk
from tkinter import messagebox
from encryption import encrypt_message
from otp_sender import generate_otp, send_otp_via_sms

class SenderApp:
    def __init__(self, root):
        self.root = root
        root.title("VaultComm - Sender")
        root.geometry("600x550")
        root.config(padx=20, pady=20)

        # Phone number input
        tk.Label(root, text="Enter Receiver Phone Number:").pack()
        self.phone_entry = tk.Entry(root)
        self.phone_entry.insert(0, "+254700000000")

        #In live mode, this accepts any phone number. For demo purposes, we’ll use the test number to show the OTP in Africa’s Talking simulator
        self.phone_entry.pack(pady=5)

        # Message input
        tk.Label(root, text="Enter Message to Encrypt:").pack()
        self.msg_input = tk.Text(root, height=4)
        self.msg_input.pack()

        # Encrypt button
        tk.Button(root, text="Encrypt Message", command=self.encrypt_msg).pack(pady=5)

        # OTP Label + Send SMS button
        self.otp_label = tk.Label(root, text="OTP Key: ")
        self.otp_label.pack()
        tk.Button(root, text="Send OTP via SMS", command=self.send_otp_sms).pack(pady=5)

        # Encrypted message display
        tk.Label(root, text="Encrypted Message (Cipher-Text):").pack()
        self.encrypted_output = tk.Text(root, height=4)
        self.encrypted_output.pack()

        # Copy buttons
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

        phone = self.phone_entry.get().strip()
        if not phone.startswith("+2547") or len(phone) != 13:
            messagebox.showerror("Invalid Number", "Please enter a valid phone number in the format +2547XXXXXXXX.")
            return

        success = send_otp_via_sms(phone, self.generated_otp)
        if success:
            messagebox.showinfo("OTP Sent", f"OTP sent via SMS to {phone}.")
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
