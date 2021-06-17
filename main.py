import sys

import tkinter as tk
from tkinter import messagebox as msg

from settings import Settings
from appPage import AppPage
from loginPage import LoginPage
from checkAgain import CheckAgain
from seePage import SeePage
from enterUser import EnterUser
from addWorker import AddWorker

class Window(tk.Tk):

	def __init__(self, App):
		self.app = App
		self.settings = App.settings

		super().__init__()
		self.title(self.settings.title)
		self.geometry(self.settings.screen)

		self.create_menus()

		self.create_container()

		self.pages = {}
	
		self.create_loginPage()

		self.settings.load_worker(self.settings.user_path)

	def change_page(self, page):
		pages=self.pages[page]
		pages.tkraise()

	def check_login(self):
		self.username = self.pages['loginPage'].var_username.get()
		self.password = self.pages['loginPage'].var_password.get()

		granted = self.settings.login(self.username, self.password)
		if granted :
			if self.settings.worker[self.username]["level"] == "owner" or self.settings.worker[self.username]["level"] == "manager" :
				self.create_appPage()
				self.change_page('appPage')

			elif self.settings.worker[self.username]["level"] == "worker" :
				self.create_seePage()
				self.change_page('seePage')

		else :
			self.create_checkAgain()
			self.change_page('checkAgain')

	def clicked_add_worker(self):

		confirm = msg.askyesno('Warehouse Worker', 'Are you sure you want to add this worker ? ')

		if confirm :
			self.add_username = self.pages['addWorker'].var_add_username.get()
			self.add_password = self.pages['addWorker'].var_add_password.get()
			self.add_level = self.pages['addWorker'].var_add_level.get()

			data = {
				"password" : self.add_password,
				"level" : self.add_level
			}

			self.settings.worker[self.add_username] = data

			self.settings.save_worker()

		self.change_page('loginPage')

	def create_menus(self):
		self.menuBar = tk.Menu(self)
		self.configure(menu=self.menuBar)

		self.fileMenu = tk.Menu(self.menuBar, tearoff = 0)
		self.fileMenu.add_command(label = "Exit", command=self.exit)
		self.fileMenu.add_command(label = "Log Out", command=self.logout)
		self.fileMenu.add_command(label = "Add Worker", command=self.new_worker)

		self.helpMenu = tk.Menu(self.menuBar, tearoff = 0)
		self.helpMenu.add_command(label = "About", command=self.show_about_info)

		self.menuBar.add_cascade(label = "File", menu=self.fileMenu)
		self.menuBar.add_cascade(label = "Help", menu=self.helpMenu)

	def create_container(self):
		self.container = tk.Frame(self)
		self.container.pack(fill="both", expand=True)

	def create_appPage(self):

		self.pages['appPage'] = AppPage(self.container, self)

	def create_loginPage(self):

		self.pages['loginPage'] = LoginPage(self.container, self)

	def create_checkAgain(self):

		self.pages['checkAgain'] = CheckAgain(self.container, self)

	def create_enterUser(self):

		self.pages['enterUser'] = EnterUser(self.container, self)

	def create_seePage(self):

		self.pages['seePage'] = SeePage(self.container, self)

	def create_addWorker(self):

		self.pages['addWorker'] = AddWorker(self.container, self)

	def show_about_info(self):

		msg.showinfo(" About Warehouse App", "This app was created for project by lin \n\nCopyright 2021")

	def exit(self):
		respon = msg.askyesno("Exit Program", "Are you sure to close the program ?")
		if respon : 
			sys.exit()

	def logout(self):
		respon = msg.askyesno("Log Out", "Are you sure to log out?")
		if respon : 
			self.change_page('loginPage')

	def new_worker(self):
		respon = msg.askyesno("New Worker", "Are you sure you want to add new worker? This page will be closed.")
		if respon :
		#	try :
		#		if self.settings.worker[self.username]["level"] == "owner" or self.settings.worker[self.username]["level"] == "manager" :
			self.create_addWorker()
			self.change_page('addWorker')
		#	except AttributeError:
		#		self.create_enterUser()
		#		self.change_page('enterUser')

		#	else :
		#		print("Sorry, You need to be the Manager or Owner to add new Worker")

class Warehouse:

	def __init__(self):
		self.settings = Settings()
		self.window = Window(self)

	def run(self):
		self.window.mainloop()

if __name__ == '__main__':
	myWarehouse = Warehouse()
	myWarehouse.run()