import base64
import os
import getpass
import tkinter as tk
import time
from cryptography.fernet import Fernet as fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt_and_writelines(file, lines, session_fernet):
	for line in lines:
		file.write(session_fernet.encrypt(str(line).encode('utf-8')).decode('utf-8') + "\n")

class new_journal():
	def __init__(self, master):
		self.master = master

		self.file_dialog = tk.Toplevel()
		self.file_dialog.title("New Journal")

		self.prompt = tk.Label(self.file_dialog, text="Create a New Journal")
		self.prompt.grid(row=0, column=0, columnspan=4)

		name_prompt = tk.Label(self.file_dialog, text="Name:")
		name_prompt.grid(row=1, column=0)

		self.name_box = tk.Entry(self.file_dialog)
		self.name_box.grid(row=1, column=1, columnspan=2)

		password_prompt = tk.Label(self.file_dialog, text="Password")
		password_prompt.grid(row=2, column=0)

		self.password_box = tk.Entry(self.file_dialog, show="*")
		self.password_box.grid(row=2, column=1, columnspan=2)

		create_button = tk.Button(self.file_dialog, text="Create", command=self.create_journal)
		create_button.grid(row=1, column=3, rowspan=2)	

	def create_journal(self):
		try:
			journal_name = self.name_box.get()
			password = self.password_box.get()

			salt = os.urandom(16)
			kdf = PBKDF2HMAC(
				algorithm=hashes.SHA256,
				length=32,
				salt=salt,
				iterations=100000,
				backend=default_backend()
			)
			key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
			session_fernet = fernet(key)

			os.makedirs(journal_name)
			journal_index = open(journal_name + ".pjindex", "w+")

			journal_index.write(str(salt) + "\n")
			preamble = [journal_name, getpass.getuser(), time.strftime("%x"), time.strftime("%X")]
			encrypt_and_writelines(journal_index, preamble, session_fernet)

			self.file_dialog.destroy()
			journal_index.close()

			self.master.session_journal = journal_name
			self.master.session_fernet = session_fernet

			self.master.open_journal_master()

		except OSError:
			self.prompt["text"] = "A Journal with this name already exists. Please use another name."


