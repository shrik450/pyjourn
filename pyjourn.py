import base64
import os
import getpass
import tkinter as tk
import time
from cryptography.fernet import Fernet as fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import windowclasses

class PyJournRoot(tk.Frame):
	def __init__(self, master):
		self.master = master
		master.title("PyJourn v0.01")

		menubar = tk.Menu(master)

		self.filemenu = tk.Menu(menubar, tearoff=0)
		self.filemenu.add_command(label="New Journal", command=self.new_journal)
		self.filemenu.add_command(label="Open Journal", command=self.open_journal)
		self.filemenu.add_command(label="New Entry", command=self.donothing, state=tk.DISABLED)
		self.filemenu.add_command(label="Open Entry", command=self.donothing, state=tk.DISABLED)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=master.quit)

		menubar.add_cascade(label="File", menu=self.filemenu)

		master.config(menu=menubar)

		self.session_journal_location = None
		self.session_fernet = None

	def new_journal(self):
		new_journal_window = windowclasses.new_journal(self)

	def open_journal_master(self):
		self.session_journal_index = open(self.session_journal_location, "r+")
		session_journal_salt = self.session_journal_index.readline()
		self.session_journal_params = []
		for i in range(4):
			self.session_journal_params.append(self.session_fernet.decrypt(self.session_journal_index.readline().encode('utf-8')).decode('utf-8'))
		print(self.session_journal_params)
		self.filemenu.entryconfig("New Entry", state=tk.ACTIVE)
		self.filemenu.entryconfig("Open Entry", state=tk.ACTIVE)

	def open_journal(self):
		open_journal_window = windowclasses.open_journal(self)

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

		entry_create_button = tk.Button(entry_window, text="Create", command=self.donothing)

	def create_entry(self):

		entry_text = self.entry_box.get()
		outstream = self.session_fernet.encrypt(entry_text.encode('utf-8'))

	def donothing(self):
		return 0

window_root = tk.Tk()
PyJourn = PyJournRoot(window_root)
window_root.mainloop()