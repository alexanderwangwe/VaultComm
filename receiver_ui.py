import customtkinter as ctk
from tkinter import messagebox
from encryption import decrypt_message

# Theme & Appearance
ctk.set_appearance_mode("Light")  # Light, Dark, or System
ctk.set_default_color_theme("dark-blue")  # Consistent with Sender

class ReceiverApp:
    def __init__(self, root):
        self.root = root
        root.title("VaultComm - Receiver")
        root.geometry("700x600")
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        padding_y = 10

        # Card frame (the "card" look)
        self.card = ctk.CTkFrame(root, corner_radius=18, border_width=2, border_color="#2a2d2e")
        self.card.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.card.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(self.card, text="VaultComm Decryption Console", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=(20, 10))

        # Encrypted Text Input
        ctk.CTkLabel(self.card, text="Enter Encrypted Text:", anchor="w").grid(row=1, column=0, sticky="ew", padx=20)
        self.encrypted_input = ctk.CTkTextbox(self.card, height=80)
        self.encrypted_input.grid(row=2, column=0, pady=(0, padding_y), padx=20, sticky="ew")

        # Paste Encrypted Text Button
        ctk.CTkButton(self.card, text="Paste Encrypted Text from Clipboard", command=self.paste_encrypted).grid(row=3, column=0, pady=(0, padding_y), padx=20)

        # OTP Input
        ctk.CTkLabel(self.card, text="Enter OTP Key:", anchor="w").grid(row=4, column=0, sticky="ew", padx=20)
        self.otp_input = ctk.CTkEntry(self.card)
        self.otp_input.grid(row=5, column=0, pady=(0, padding_y), padx=20, sticky="ew")

        # Paste OTP Button
        ctk.CTkButton(self.card, text="Paste OTP from Clipboard", command=self.paste_otp).grid(row=6, column=0, pady=(0, padding_y), padx=20)

        # Decrypt Button
        ctk.CTkButton(self.card, text="Decrypt Message", command=self.decrypt_msg).grid(row=7, column=0, pady=(0, padding_y), padx=20)

        # Decrypted Message Display
        ctk.CTkLabel(self.card, text="Decrypted Message:", anchor="w").grid(row=8, column=0, sticky="ew", padx=20)
        self.decrypted_output = ctk.CTkTextbox(self.card, height=60)
        self.decrypted_output.grid(row=9, column=0, pady=(0, padding_y), padx=20, sticky="ew")

        # Status Log
        self.status_label = ctk.CTkLabel(self.card, text="", text_color="green")
        self.status_label.grid(row=10, column=0, pady=(5, 20))

    def decrypt_msg(self):
        cipher_text = self.encrypted_input.get("1.0", "end").strip()
        otp = self.otp_input.get().strip()
        self.status_label.configure(text="", text_color="green")

        # Input validation
        if not cipher_text or not otp:
            messagebox.showerror("Missing Input", "Both OTP and encrypted message are required.")
            return

        if len(cipher_text) < 32:
            messagebox.showerror("Input Error", "The encrypted message is too short or incomplete.")
            return

        # Decrypt and display result
        try:
            decrypted = decrypt_message(cipher_text, otp)
            self.decrypted_output.delete("1.0", "end")
            self.decrypted_output.insert("end", decrypted)
            self.status_label.configure(text="✅ Message decrypted successfully.", text_color="green")
            messagebox.showinfo("Success", "Message decrypted successfully!")
        except Exception as e:
            self.decrypted_output.delete("1.0", "end")
            self.status_label.configure(text="❌ Decryption failed.", text_color="red")
            messagebox.showerror("Decryption Failed", f"Decryption failed.\n\nDetails:\n{str(e)}")

    def paste_encrypted(self):
        # Paste encrypted text from clipboard
        try:
            clipboard_text = self.root.clipboard_get()
            self.encrypted_input.delete("1.0", "end")
            self.encrypted_input.insert("end", clipboard_text)
        except Exception:
            messagebox.showerror("Clipboard Error", "Failed to read from clipboard.")

    def paste_otp(self):
        # Paste OTP from clipboard
        try:
            clipboard_text = self.root.clipboard_get()
            self.otp_input.delete(0, "end")
            self.otp_input.insert(0, clipboard_text)
        except Exception:
            messagebox.showerror("Clipboard Error", "Failed to read OTP from clipboard.")


if __name__ == "__main__":
    root = ctk.CTk()
    app = ReceiverApp(root)
    root.mainloop()