import base64
import os
import getpass
import tkinter as tk
import time
from cryptography.fernet import Fernet as fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tkinter.filedialog import askopenfilename

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

			self.master.session_journal_location = journal_name + ".pjindex"
			self.master.session_fernet = session_fernet

			self.master.open_journal_master()

		except OSError:
			self.prompt["text"] = "You cannot use this name, as either a Journal with that name already exists, or it is invalid."

class open_journal():
	def __init__(self, master):
		self.master = master

		self.file_dialog = tk.Toplevel()
		self.file_dialog.title("Open Journal")

		prompt = tk.Label(self.file_dialog, text="Open Journal:")
		prompt.grid(row=0, column=0, columnspan=2)

		name_prompt = tk.Label(self.file_dialog, text="Name:")
		name_prompt.grid(row=1, column=0)

		self.name_box = tk.Entry(self.file_dialog)
		self.name_box.grid(row=1, column=1, columnspan=5)

		browse_button = tk.Button(self.file_dialog, text="Browse", command=self.browse)
		browse_button.grid(row=1, column=6, columnspan=2)

		password_prompt = tk.Label(self.file_dialog, text="Password:")
		password_prompt.grid(row=2, column=0)

		self.password_box = tk.Entry(self.file_dialog)
		self.password_box.grid(row=2, column=1, columnspan=5)

		open_button = tk.Button(self.file_dialog, text="Open", command=self.open_now)
		open_button.grid(row=2, column=6, columnspan=2)

	def browse(self):
		journal_location = askopenfilename(initialdir="/", title="Select Journal", filetypes=(("PyJourn Index Files","*.pjindex"), ("All Files", "*.*")))
		self.name_box.insert(0, journal_location)

	def open_now(self):
		journal_location = self.name_box.get()
		journal_password = self.password_box.get()

		self.master.session_journal_location = journal_location

		journal_index = open(journal_location, "r+")
		journal_salt = journal_index.readline()[2:-4].encode('utf-8')
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256,
			length=32,
			salt=journal_salt,
			iterations=100000,
			backend=default_backend()
		)
		key = base64.urlsafe_b64encode(kdf.derive(journal_password.encode('utf-8')))
		journal_fernet = fernet(key)

		self.master.session_fernet = journal_fernet

		self.master.open_journal_master()