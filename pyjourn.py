import base64
import os
import getpass
import tkinter as tk
import time
from cryptography.fernet import Fernet as fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PyJournRoot(tk.Frame):
	def __init__(self, master):
		self.master = master
		master.title("PyJourn v0.01")

		menubar = tk.Menu(master)

		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="New Journal", command=self.new_journal)#, state=tk.DISABLED)
		filemenu.add_command(label="Open Journal", command=self.donothing, state=tk.DISABLED)
		filemenu.add_separator()
		filemenu.add_command(label="New Entry", command=self.donothing, state=tk.DISABLED)
		filemenu.add_command(label="Open Entry", command=self.donothing, state=tk.DISABLED)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=master.quit)

		menubar.add_cascade(label="File", menu=filemenu)

		master.config(menu=menubar)

	def encrypt_and_writelines(self, file, lines):
		outstream = []
		for line in lines:
			outstream.append(self.session_fernet.encrypt(str(line).encode('utf-8')))

		file.writelines(outstream)

	def new_journal(self):
		self.file_dialog = tk.Toplevel()
		self.file_dialog.title("New Journal")

		self.prompt = tk.Label(file_dialog, text="Create a New Journal")
		self.prompt.grid(row=0, column=0, columnspan=4)

		name_prompt = tk.Label(file_dialog, text="Name:")
		name_prompt.grid(row=1, column=0)

		self.name_box = tk.Entry(file_dialog)
		self.name_box.grid(row=1, column=1, columnspan=2)

		password_prompt = tk.Label(file_dialog, text="Password")
		password_prompt.grid(row=2, column=0)

		self.password_box = tk.Entry(file_dialog, show="*")
		self.password_box.grid(row=2, column=1, columnspan=2)

		create_button = tk.Button(file_dialog, text="Create", command=self.create_journal)
		create_button.grid(row=1, column=3, rowspan=2)

	def create_journal(self):
		try:
			self.journal_name = self.name_box.get()
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
			self.session_fernet = fernet(key)

			os.makedirs(self.journal_name)
			self.journal_index = open(self.journal_name + ".pji", "w+b")

			self.journal_index.write((str(salt)+"\n").encode('utf-8'))
			preamble = [(self.journal_name+"\n").encode('utf-8'), (getpass.getuser()+"\n").encode('utf-8'), (time.strftime("%x") + "\n").encode('utf-8'), (time.strftime("%X") + "\n").encode('utf-8')]
			self.encrypt_and_writelines(self.journal_index, preamble)

			self.file_dialog.destroy()
		except OSError:
			self.prompt["text"] = "A Journal with this name already exists. Please use another name."

	def new_entry(self):
		entry_window = tk.Toplevel()
		entry_window.title("New Entry in Journal " + self.journal_name)

		menubar = tk.Menu(entry_window)

		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Save", command=self.donothing)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=entry_window.destroy)

		menubar.add_cascade(label="File", menu=filemenu)

		self.prompt = tk.Label(entry_window, text="Create a new Journal entry.")
		#self.prompt.grid(row=0, column=0, columnspan=8)
		self.prompt.pack()

		nameprompt = tk.Label(entry_window, text="Name:")
		#name_prompt.grid(row=2, column=0)
		nameprompt.pack()

		self.name_box = tk.Entry(entry_window)
		#self.name_box.grid(row=2, column=2, columnspan=6)
		self.name_box.pack()

		entry_frame = tk.Frame(entry_window)
		#entry_frame.grid(row=3, column=0, columnspan=8)
		entry_frame.pack()

		self.entry_box = tk.Text(entry_frame, height=16, width=80)
		#self.entry_box.grid(row=0, column=0)
		self.entry_box.pack(side=tk.LEFT, fill=tk.Y)		

		entry_box_scrollbar = tk.Scrollbar(entry_frame)
		#entry_box_scrollbar.grid(row=0, column=1)
		entry_box_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		entry_box_scrollbar.config(command=self.entry_box.yview)
		self.entry_box.config(yscrollcommand=entry_box_scrollbar.set)

		entry_create_button = tk.Button(entry_window, text="Create", command=self.donothing)

	def create_entry(self):

		entry_text = self.entry_box.get()
		outstream = self.session_fernet.encrypt(entry_text.encode('utf-8'))
		self.

	def donothing(self):
		return 0

window_root = tk.Tk()
PyJourn = PyJournRoot(window_root)
window_root.mainloop()