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
		filemenu.add_command(label="New Journal", command=self.donothing, state=tk.DISABLED)
		filemenu.add_command(label="Open Journal", command=self.donothing, state=tk.DISABLED)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=master.quit)

		menubar.add_cascade(label="File", menu=filemenu)

		master.config(menu=menubar)

	def donothing():
		return 0

window_root = tk.Tk()
PyJourn = PyJournRoot(window_root)
window_root.mainloop()


