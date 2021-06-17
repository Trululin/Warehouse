import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image, ImageTk

class SeePage(tk.Frame):

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
			#print(clicked_item_index, "==>", index)
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