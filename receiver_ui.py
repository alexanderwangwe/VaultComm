import tkinter as tk
from tkinter import messagebox
from encryption import decrypt_message

class ReceiverApp:
    def __init__(self, root):
        self.root = root
        root.title("VaultComm - Receiver")
        root.geometry("600x500")
        root.config(padx=20, pady=20)

        tk.Label(root, text="Enter Encrypted Text:").pack()
        self.encrypted_input = tk.Text(root, height=4)
        self.encrypted_input.pack()

        tk.Button(root, text="Paste Encrypted Text from Clipboard", command=self.paste_encrypted).pack(pady=5)

        tk.Label(root, text="Enter OTP Key:").pack()
        self.otp_input = tk.Entry(root)
        self.otp_input.pack()

        tk.Button(root, text="Paste OTP from Clipboard", command=self.paste_otp).pack(pady=5)

        tk.Button(root, text="Decrypt Message", command=self.decrypt_msg).pack(pady=5)
        tk.Label(root, text="Decrypted Message:").pack()
        self.decrypted_output = tk.Text(root, height=3)
        self.decrypted_output.pack()

        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack(pady=5)

    def decrypt_msg(self):
        cipher_text = self.encrypted_input.get("1.0", tk.END).strip()
        otp = self.otp_input.get().strip()
        self.status_label.config(text="", fg="green")

        if not cipher_text or not otp:
            messagebox.showerror("Missing Input", "Both OTP and message are required.")
            return

        if len(cipher_text) < 32:
            messagebox.showerror("Input Error", "The encrypted message is too short or incomplete.")
            return

        try:
            decrypted = decrypt_message(cipher_text, otp)
            self.decrypted_output.delete("1.0", tk.END)
            self.decrypted_output.insert(tk.END, decrypted)
            self.status_label.config(text="✅ Message decrypted successfully.", fg="green")
            messagebox.showinfo("Success", "Message decrypted successfully!")

        except Exception as e:
            self.decrypted_output.delete("1.0", tk.END)
            self.status_label.config(text="❌ Decryption failed.", fg="red")
            messagebox.showerror("Decryption Failed", f"Decryption failed.\n\nDetails:\n{str(e)}")

    def paste_encrypted(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.encrypted_input.delete("1.0", tk.END)
            self.encrypted_input.insert(tk.END, clipboard_text)
        except Exception:
            messagebox.showerror("Clipboard Error", "Failed to read from clipboard.")

    def paste_otp(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.otp_input.delete(0, tk.END)
            self.otp_input.insert(0, clipboard_text)
        except Exception:
            messagebox.showerror("Clipboard Error", "Failed to read OTP from clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiverApp(root)
    root.mainloop()
