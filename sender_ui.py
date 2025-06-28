import customtkinter as ctk
from tkinter import messagebox
from encryption import encrypt_message
from otp_sender import generate_otp, send_otp_via_sms

# Appearance and theme
ctk.set_appearance_mode("Light")  # "Light", "Dark", or "System"
ctk.set_default_color_theme("dark-blue")

class SenderApp:
    def __init__(self, root):
        self.root = root
        root.title("VaultComm - Sender")
        root.geometry("640x620")
        root.grid_columnconfigure(0, weight=1)

        padding_y = 10  # consistent vertical spacing

        # Title
        ctk.CTkLabel(root, text="VaultComm Encryption Console", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=(20, 10))

        # Phone number input
        ctk.CTkLabel(root, text="Receiver Phone Number:", anchor="w").grid(row=1, column=0, sticky="ew", padx=20)
        self.phone_entry = ctk.CTkEntry(root, width=300, placeholder_text="+2547XXXXXXXX")
        self.phone_entry.insert(0, "+254700000000")
        self.phone_entry.grid(row=2, column=0, pady=(0, padding_y), padx=20, sticky="ew")

        # Message input
        ctk.CTkLabel(root, text="Message to Encrypt:", anchor="w").grid(row=3, column=0, sticky="ew", padx=20)
        self.msg_input = ctk.CTkTextbox(root, height=80)
        self.msg_input.grid(row=4, column=0, pady=(0, padding_y), padx=20, sticky="ew")

        # Encrypt button
        ctk.CTkButton(root, text="Encrypt Message", command=self.encrypt_msg).grid(row=5, column=0, pady=(0, padding_y), padx=20)

        # OTP Label
        self.otp_label = ctk.CTkLabel(root, text="OTP Key: ", anchor="w")
        self.otp_label.grid(row=6, column=0, sticky="ew", padx=20, pady=(0, 5))

        # Send SMS button
        ctk.CTkButton(root, text="Send OTP via SMS", command=self.send_otp_sms).grid(row=7, column=0, pady=(0, padding_y), padx=20)

        # Encrypted message display
        ctk.CTkLabel(root, text="Encrypted Message (Cipher Text):", anchor="w").grid(row=8, column=0, sticky="ew", padx=20)
        self.encrypted_output = ctk.CTkTextbox(root, height=80)
        self.encrypted_output.grid(row=9, column=0, pady=(0, padding_y), padx=20, sticky="ew")

        # Copy buttons
        ctk.CTkButton(root, text="Copy Encrypted Text", command=self.copy_encrypted).grid(row=10, column=0, pady=(0, 5), padx=20)
        ctk.CTkButton(root, text="Copy OTP", command=self.copy_otp).grid(row=11, column=0, pady=(0, 20), padx=20)

        self.generated_otp = ""
        self.encryption_success = False

    def encrypt_msg(self):
        msg = self.msg_input.get("1.0", "end").strip()
        if not msg:
            messagebox.showerror("Missing Message", "Please enter a message to encrypt.")
            return

        self.generated_otp = generate_otp()
        self.otp_label.configure(text=f"OTP Key: {self.generated_otp}")

        try:
            encrypted = encrypt_message(msg, self.generated_otp)
            self.encrypted_output.delete("1.0", "end")
            self.encrypted_output.insert("end", encrypted)
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
        encrypted_text = self.encrypted_output.get("1.0", "end").strip()
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
    root = ctk.CTk()
    app = SenderApp(root)
    root.mainloop()
