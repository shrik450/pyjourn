import base64
import os
import getpass
import tkinter as tk
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
		filemenu.add_command(label="New Journal", command=self.create_journal)#, state=tk.DISABLED)
		filemenu.add_command(label="Open Journal", command=self.donothing, state=tk.DISABLED)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=master.quit)

		menubar.add_cascade(label="File", menu=filemenu)

		master.config(menu=menubar)

	def create_journal(self):
		file_dialog = tk.Toplevel()
		file_dialog.title("New Journal")

		self.prompt = tk.Label(file_dialog, text="Create a New Journal")
		self.prompt.grid(row=0, column=0, columnspan=4)

		name_prompt = tk.Label(file_dialog, text="Name:")
		name_prompt.grid(row=1, column=0)

		self.name_box = tk.Entry(file_dialog)
		self.name_box.grid(row=1, column=1, columnspan=2)

		password_prompt = tk.Label(file_dialog, text="Password")
		password_prompt.grid(row=2, column=0)

		self.password_box = tk.Entry(file_dialog)
		self.password_box.grid(row=2, column=1, columnspan=2)

		create_button = tk.Button(file_dialog, text="Create", command=self.donothing())
		create_button.grid(row=1, column=3, rowspan=2)



	def donothing(self):
		return 0

window_root = tk.Tk()
PyJourn = PyJournRoot(window_root)
window_root.mainloop()


