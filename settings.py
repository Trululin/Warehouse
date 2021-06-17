from json import load, dump

class Settings : 

	def __init__(self):

		self.title = "Warehouse"

		base = 50
		ratio = (16, 9)
		self.width = base*ratio[0]
		self.height = base*ratio[1]
		self.screen = f"{self.width}x{self.height}+200+100"

		self.login_pic = "img/login.jfif"
		self.logo = "img/sembako.jfif"

		self.user_path = "data/worker.json"
		self.items_path = "data/items.json"

		self.load_data_from_json()

	def load_worker(self, path):
		with open(path, "r") as json_data:
			self.worker = load(json_data)
		return self.worker

	def save_worker(self):
		with open("data/worker.json", "w") as json_data:
			dump(self.worker, json_data)

	def login(self, username, password):
		users = self.load_worker(self.user_path)

		if username in users:
			if password == users[username]["password"]:
				return True
			else : 
				return False
		else : 
			return False

	def load_data_from_json(self):
		with open(self.items_path, "r") as file_json:
			self.items = load(file_json)

	def save_data_to_json(self):
		with open(self.items_path, "w") as file_json:
			dump(self.items, file_json)


