import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image, ImageTk

class AppPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings
		self.current_item = self.settings.items[0]
		self.last_current_item_index = 0
		self.update_mode = False
		self.items_index = []

		super().__init__(parent)
		self.grid(row = 0, column=0, sticky = "nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_leftright_frame()

	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg="pink")
		self.left_frame.grid(row=0, column=0, sticky="nsew")

		self.create_left_header()
		self.create_left_content()

	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg="white", width=2*self.settings.width//3)
		self.right_frame.grid(row=0, column=1, sticky="nsew")

		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()

	def config_leftright_frame(self):
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=2)
		self.grid_rowconfigure(0, weight=1)

	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5
		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h)
		self.left_header.pack()

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio), int(i_h/ratio))
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.logo)
		self.label_logo.pack()

		self.search_box_frame = tk.Frame(self.left_frame, bg="white", width=frame_w, height=frame_h//4)
		self.search_box_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.search_box_frame, bg="white", fg="black", font=("Arial", 12), textvariable=self.entry_search_var)
		self.entry_search.grid(row=0, column=0)

		self.button_search = tk.Button(self.search_box_frame, bg="white", fg="black", text="Find", font=("Arial", 12), command=self.clicked_search_btn)
		self.button_search.grid(row=0, column=1)

		self.search_box_frame.grid_columnconfigure(0, weight=3)
		self.search_box_frame.grid_columnconfigure(1, weight=1)

	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = 4*self.settings.height//5
		self.left_content = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_content.pack(fill="x")

		self.item_list_box = tk.Listbox(self.left_content, bg="white", fg="black", font=("Arial", 12), height=frame_h)
		self.item_list_box.pack(side="left", fill="both", expand=True)

		self.list_scroll = tk.Scrollbar(self.left_content)
		self.list_scroll.pack(side="right", fill="y")

		self.show_all_items_in_listbox()

		self.item_list_box.configure(yscrollcommand=self.list_scroll.set)
		self.list_scroll.configure(command=self.item_list_box.yview)

		self.item_list_box.bind("<<ListboxSelect>>", self.clicked_item_inList)



	def show_list_items_in_listbox(self):
		items = self.settings.items

		for index in self.items_index:
			item = items[index]
			for code, info in item.items():
				item_name = (info['name']).title()
				self.item_list_box.insert("end", item_name)

	def show_all_items_in_listbox(self):
		self.item_list_box.delete(0, 'end')
		items = self.settings.items
		self.items_index = []
		counter = 0
		for item in items:
			self.items_index.append(counter)
			counter += 1
		self.show_list_items_in_listbox()

	def clicked_item_inList(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try : 
				clicked_item_index = selection[0]
			except IndexError:
				clicked_item_index = self.last_current_item_index

			index = self.items_index[clicked_item_index]
			self.last_current_item_index = index
			self.current_item = self.settings.items[index]
			print(clicked_item_index, "==>", index)
			for code, info in self.current_item.items():
				item_code = code
				name = (info['name']).title()
				types = (info['type']).title()
				mfg = (info['mfg']).title()
				exp = (info['exp']).title()

			self.item_label.configure(text=name)
			self.table_info[0][1].configure(text=code)
			self.table_info[1][1].configure(text=types)
			self.table_info[2][1].configure(text=mfg)
			self.table_info[3][1].configure(text=exp)



	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_header.pack()

		self.create_detail_right_header()

	def create_detail_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="green")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		self.virt_img = tk.PhotoImage(width=1, height=1)

		for code, info in self.current_item.items():
			name = (info['name']).title()
			self.item_label = tk.Label(self.detail_header, text=name, font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound='c', bg="white")
			self.item_label.pack()

		self.right_header.grid_rowconfigure(0, weight=1)
		self.right_header.grid_columnconfigure(0, weight=1)

	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_content.pack(expand=True, pady=90)

		self.create_detail_right_content()

	def create_detail_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		for code, info in self.current_item.items():
			info = [
				['Code : ', (code).upper()],
				['Type :', (info['type']).title()],
				['MFG :', (info['mfg']).title()],
				['EXP :', (info['exp']).title()]
			]

		self.table_info = []
		rows, columns = len(info), len(info[0]) # 3, 2
		for row in range(rows):
			aRow = []
			for column in range(columns):
				label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 12), bg="white")
				aRow.append(label)
				if column == 0:
					sticky = "e"
				else:
					sticky = "w"
				label.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)

		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)

	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_footer.pack(expand=True)

		self.create_detail_right_footer()

	def create_detail_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update', 'Delete', 'Add New']
		commands = [self.clicked_update_btn, self.clicked_delete_btn, self.clicked_add_new_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)



	def clicked_delete_btn(self):
		self.update_mode = True
		index = self.last_current_item_index

		confirm = msg.askyesno('Item Removal Confirmation', 'Are you sure to delete this item?')
		if confirm:
			del self.settings.items[index]

			self.settings.save_data_to_json()

			self.item_list_box.delete(0, 'end')
			self.show_all_items_in_listbox()

			self.current_item = self.settings.items[0]
			self.last_current_item_index = 0

			self.detail_header.destroy()
			self.detail_content.destroy()
			self.detail_footer.destroy()

			self.create_detail_right_footer()
			self.create_detail_right_content()
			self.create_detail_right_header()

		self.update_mode = False

	def clicked_update_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for code, info in self.current_item.items():
			info = [
				['Code : ', code],
				['Name : ', info['name']],
				['Type : ', info['type']],
				['MFG : ', info['mfg']],
				['EXP : ', info['exp']]
			]

		self.table_info = []
		self.entry_update_data_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

		rows, columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="white")
					aRow.append(label)
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
				else:
					entry = tk.Entry(self.detail_update_content, font=("Arial", 12), bg="white", textvariable=self.entry_update_data_vars[row])
					entry.insert(0, info[row][column])
					sticky = "w"
					aRow.append(entry)
					entry.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)

		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_data_btn, self.clicked_cancel_data_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)

	def clicked_save_data_btn(self):
		self.update_mode = False

		confirm = msg.askyesnocancel('Warehouse Data Save Confirmation', 'Are you sure you want to update this data ? ')
		index = self.last_current_item_index

		if confirm :
			code = self.entry_update_data_vars[0].get()
			name = self.entry_update_data_vars[1].get()
			types = self.entry_update_data_vars[2].get()
			mfg = self.entry_update_data_vars[3].get()
			exp = self.entry_update_data_vars[4].get()

			self.settings.items[index] = {
					code : {
					"name" : name,
					"type" : types,
					"mfg" : mfg, 
					"exp" : exp
				}
			}
			self.settings.save_data_to_json()

		self.current_item = self.settings.items[index]

		self.recreate_right_frame_after_update()

		self.item_list_box.delete(0, 'end')
		self.show_list_items_in_listbox()

	def clicked_cancel_data_btn(self):
		self.update_mode = False

		self.recreate_right_frame_after_update()

	def recreate_right_frame_after_update(self):
		self.detail_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()

		self.create_detail_right_header()
		self.create_detail_right_content()
		self.create_detail_right_footer()



	def clicked_add_new_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_add_item = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_add_item.grid(row=0, column=0, sticky="nsew")

		for code, info in self.current_item.items():
			info = [
				['Code : ', ''],
				['Name : ', ''],
				['Type : ', ''],
				['MFG : ', ''],
				['EXP : ', '']
			]

		self.table_info = []
		self.entry_add_data_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

		rows, columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_add_item, text=info[row][column], font=("Arial", 12), bg="white")
					aRow.append(label)
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
				else:
					entry = tk.Entry(self.detail_add_item, font=("Arial", 12), bg="white", textvariable=self.entry_add_data_vars[row])
					entry.insert(0, info[row][column])
					sticky = "w"
					aRow.append(entry)
					entry.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)

		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_add_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_add_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_new_data_btn, self.clicked_cancel_new_data_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_add_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)

	def clicked_save_new_data_btn(self):
		self.update_mode = False
		confirm = msg.askyesnocancel('Warehouse Data Save Confirmation', 'Are you sure you want to add this data ? ')
		index = self.last_current_item_index

		if confirm :
			code = self.entry_add_data_vars[0].get()
			name = self.entry_add_data_vars[1].get()
			types = self.entry_add_data_vars[2].get()
			mfg = self.entry_add_data_vars[3].get()
			exp = self.entry_add_data_vars[4].get()

			data = {
				code : {
					"name" : name,
					"type" : types,
					"mfg" : mfg, 
					"exp" : exp
				}
			}

			self.settings.items.append(data)

			self.settings.save_data_to_json()

		self.current_item = self.settings.items[index]

		self.recreate_right_frame_after_adding()

		self.item_list_box.delete(0, 'end')
		self.show_all_items_in_listbox()

	def clicked_cancel_new_data_btn(self):
		self.update_mode = False
		self.recreate_right_frame_after_adding()

	def recreate_right_frame_after_adding(self):
		self.detail_header.destroy()
		self.detail_add_item.destroy()
		self.detail_add_footer.destroy()

		self.create_detail_right_header()
		self.create_detail_right_content()
		self.create_detail_right_footer()


	def clicked_search_btn(self):

		item_search = self.entry_search_var.get()
		if item_search:
			items = self.settings.items
			self.items_index = []
			index_counter = 0

			for item in items:
				for code, info in item.items():
					if item_search in code:
						print(code)
						self.items_index.append(index_counter)

					elif item_search in info['name']:
						print(info['name'])
						self.items_index.append(index_counter)

					elif item_search == " ":
						self.items_index.append(index_counter)

				index_counter += 1

		print (self.items_index)
		self.item_list_box.delete(0, 'end')
		self.show_list_items_in_listbox()