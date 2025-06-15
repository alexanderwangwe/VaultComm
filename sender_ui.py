import tkinter as tk
from tkinter import messagebox
from encryption import encrypt_message
from otp_sender import generate_otp

class SenderApp:
    def __init__(self, root):
        self.root = root
        root.title("VaultComm - Sender")
        root.geometry("600x450")
        root.config(padx=20, pady=20)

        tk.Label(root, text="Enter Message to Encrypt:").pack()
        self.msg_input = tk.Text(root, height=4)
        self.msg_input.pack()

        tk.Button(root, text="Generate OTP", command=self.generate_otp).pack(pady=5)
        self.otp_label = tk.Label(root, text="OTP Key: ")
        self.otp_label.pack()

        tk.Button(root, text="Encrypt Message", command=self.encrypt_msg).pack(pady=5)
        tk.Label(root, text="Encrypted Message:").pack()
        self.encrypted_output = tk.Text(root, height=4)
        self.encrypted_output.pack()

        tk.Button(root, text="Copy Encrypted Text", command=self.copy_encrypted).pack(pady=5)
        tk.Button(root, text="Copy OTP", command=self.copy_otp).pack(pady=2)

        self.generated_otp = ""

    def generate_otp(self):
        self.generated_otp = generate_otp()
        self.otp_label.config(text=f"OTP Key: {self.generated_otp}")
        messagebox.showinfo("OTP Generated", f"OTP:\n{self.generated_otp}")

    def encrypt_msg(self):
        msg = self.msg_input.get("1.0", tk.END).strip()
        otp = self.generated_otp
        if not msg or not otp:
            messagebox.showerror("Missing Data", "Message or OTP is missing!")
            return
        encrypted = encrypt_message(msg, otp)
        self.encrypted_output.delete("1.0", tk.END)
        self.encrypted_output.insert(tk.END, encrypted)

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
