from tkinter import *
from tkinter import messagebox
import random
from PIL import ImageTk, Image
import pygame
pygame.mixer.init()
import os

GAME_SOUND = pygame.mixer.Sound(os.path.join("sounds", "林海 - 欢沁(1).wav"))

price = {2: "Belt", 1: "GT2", -1:"Wiskey", -2:"gotdrunk", 0:"Matepad", 3: "headset"}

# name of the person
data = ["A", "B", "C", "D"]

# image of the person
images = ["A", "B", "C", "D"]


r = lambda: random.randint(0,255)
win_width = 800
win_height = 800

Huawei_cap = None
decoration = None


class Show:
	def __init__(self):
		global decoration
		self.win = Tk()
		self.win.geometry('1500' + 'x' +'1020')
		self.win.title("Circle Sup!!!")
		self.data = data[:]
		self.img_names = images[:]
		self.imgs = []
		for name in self.img_names:
			img = Image.open('roll_img/' + name + '.png')
			img = img.resize((200, 200), Image.ANTIALIAS)
			img = ImageTk.PhotoImage(img)
			self.imgs.append(img)
		self.default_color = self.win.cget('bg')
		self.winner_img = None
		self.is_going = False

		self.c = Canvas(self.win, width=win_width + 300, height=win_height + 200)
		self.c.place(x=300, y=50)

		self.winner_img_label = Label(self.c, image=self.winner_img)
		self.winner_img_label.place(x=win_width + 20, y = win_height // 2 - 100)
		decoration = Image.open('img/decoration.png')
		decoration = decoration.resize((win_width, win_height), Image.ANTIALIAS)
		decoration = ImageTk.PhotoImage(decoration)
		self.times = 0 # How many time already rolled
		# Label(self.c, image=decoration).place(x=0, y=0)

		self.c.create_image(0, 0, image=decoration, anchor=NW)
		self.winner_label = Label(self.c, text='', font=("Arial", 20))
		self.winner_label.place(x=win_width + 60, y=win_height // 2 + 120)
		self.names = [] # for show_all_label
		self.temp_winner = [] # 被移除后的
		self.sim_winner = -1
		self.stuck = Image.open('roll_img/90d.png')
		self.stuck = self.stuck.resize((200, 200), Image.ANTIALIAS)
		self.stuck = ImageTk.PhotoImage(self.stuck)

		self.circle = []
		self.colors = []
		for i in range(len(self.data)):
			start = 90 + 360 / len(self.data) / 2 + i * 360 / len(self.data)
			color = "#%02X%02X%02X" % (r(),r(),r())
			while color in self.circle:
				color = "#%02X%02X%02X" % (r(),r(),r())
			self.colors.append(color)
			part = self.c.create_arc(25, 30, win_width - 25, win_height - 30, fill=color,
								     style=PIESLICE, start=start,
								     extent=360 / len(self.data), width=2)
			# print(self.c.itemconfigure(part, 'start')[4])
			self.circle.append([part, start, color, data[i]])
		pointer_img = Image.open('img/pointer.png')
		pointer_img = pointer_img.resize((20, 150), Image.ANTIALIAS)
		self.pointer_img = ImageTk.PhotoImage(pointer_img)
		self.c.create_image(win_width / 2, 75, image=self.pointer_img)
		# self.roll_button = Button(self.win, text="surprise!", font=("Comicsansms", 30),
		# 	command=self.space_pressed, bd=4, width=15, height=2)
		#
		# self.win.bind('<space>', self.space_pressed)
		# self.roll_button.place(x=win_width // 2 + 100, y=win_height + 50)

		Huawei_cap = Image.open('roll_img/crown.png')
		Huawei_cap = Huawei_cap.resize((150, 100), Image.ANTIALIAS)
		Huawei_cap = ImageTk.PhotoImage(Huawei_cap)
		self.huawei_cap_label = Label(self.c, image=Huawei_cap)

		# 几等奖按钮
		self.price_3 = Button(self.win, text="三等奖 (7)", font=("Arial", 20), command=self.space_pressed, bd=4)
		self.price_2 = Button(self.win, text="二等奖 (5)", font=("Arial", 20), command=self.space_pressed, bd=4)
		self.price_1 = Button(self.win, text="一等奖 (2)", font=("Arial", 20), command=self.space_pressed, bd=4)
		self.price_s = Button(self.win, text="特等奖 (1)", font=("Arial", 20), command=self.space_pressed, bd=4)
		self.price_3.place(x=200, y=900)

		# 几等奖 Label
			# store imgs
		for p in price.keys():
			if p == -2:
				price[p] = Image.open("roll_img/" + price[p] + '.png')
				price[p] = price[p].resize((180, 180), Image.ANTIALIAS)
				price[p] = ImageTk.PhotoImage(price[p])
			else:
				price[p] = Image.open("roll_img/" + price[p] + '.png')
				price[p] = price[p].resize((100, 100), Image.ANTIALIAS)
				price[p] = ImageTk.PhotoImage(price[p])
		Label(self.win, image=price[3]).place(x=1360, y=0)
		Label(self.win, text="三等奖: ", font=("Arial", 20)).place(x=1500, y=50)
		self.label_price_3 = Label(self.win, text="", font=("Arial", 18, 'italic'), fg='red')
		self.label_price_3.place(x=1500, y=100)
		Label(self.win, image=price[2]).place(x=1360, y=250)
		Label(self.win, text="二等奖: ", font=("Arial", 20)).place(x=1500, y=300)
		self.label_price_2 = Label(self.win, text="", font=("Arial", 18, 'italic'), fg='red')
		self.label_price_2.place(x=1500, y=350)
		Label(self.win, image=price[1]).place(x=1360, y=450)
		Label(self.win, text="一等奖: ", font=("Arial", 20)).place(x=1500, y=500)
		self.label_price_1 = Label(self.win, text="", font=("Arial", 18, 'italic'), fg='red')
		self.label_price_1.place(x=1500, y=550)
		Label(self.win, image=price[0]).place(x=1360, y=600)
		Label(self.win, text="特等奖: ", font=("Arial", 20)).place(x=1500, y=650)
		self.label_price_s = Label(self.win, text="", font=("Arial", 18, 'italic'), fg='red')
		self.label_price_s.place(x=1500, y=700)
		self.failed_label = Label(self.win, text="特别奖: ", font=("Arial", 20))
		self.label_price_failed = Label(self.win,  text="", font=("Arial", 18, 'italic'), fg='red')
		self.label_price_failed.place(x=1500, y=850)

		self.price_3.place(x=200, y=900)

		self.price_2.place(x=200 + 300, y=900)
		self.price_2['state'] = 'disabled'
		self.price_1.place(x=200 + 2 * 300, y=900)
		self.price_1['state'] = 'disabled'
		self.price_s.place(x=200 + 3 * 300, y=900)
		self.price_s['state'] = 'disabled'


		self.al_rotate_times = 0 # already_rotate_tims
		self.step = 5

		self.show_all_label()
		# Label(self.win, width=100, height=800).place(x=)
		self.win.mainloop()

	def create_c(self):
		for i in range(len(self.data)):
			start = 90 + 360 / len(self.data) / 2 + i * 360 / len(self.data)
			part = self.c.create_arc(25, 30, win_width - 25, win_height - 30, fill=self.colors[i],
								     style=PIESLICE, start=start,
								     extent=360 / len(self.data), width=2)
			# print(self.c.itemconfigure(part, 'start')[4])
			self.circle.append([part, start, self.colors[i], self.data[i]])


	def show_all_label(self):
		for i, part in enumerate(self.circle):
			frame = Frame(self.win)
			frame.place(x=50, y=50 + i * 40 + i * 10)
			name_label = Label(frame, text=' ' + part[3], font=('Arial', 20))
			name_label.pack(side=RIGHT)
			color_label = Label(frame, bg=part[2], width=2)
			color_label.pack(side=RIGHT)
			self.names.append((name_label, color_label))


	def space_pressed(self, event=None):
		self.huawei_cap_label.place_forget()
		if not self.is_going:
			pygame.mixer.unpause()
			self.step = 20
			self.al_rotate_times = 0 # already_rotate_tims
			self.is_going = True
			rotate_times = random.randint(150, 250)
			print(rotate_times)
			if self.times >= 12 and self.times < 16:
				self.sim_winner = self.get_winner(rotate_times)
				if self.sim_winner != -1:
					# if self.data[self.sim_winner] == "name1" or self.data[self.sim_winner] == "name2":
						# print("los")
						# rotate_times += 8
			if len(self.data) != len(data):
				self.circle = []
				self.create_c()
				self.c.create_image(win_width / 2, 75, image=self.pointer_img)
			self.roll(rotate_times)

	def get_winner(self, r_t):
		step = self.step
		al_rotate_times = self.al_rotate_times
		circle = []
		t_canvas = Canvas(self.win)
		for i in range(len(self.data)):
			start = 90 + 360 / len(self.data) / 2 + i * 360 / len(self.data)
			part = t_canvas.create_arc(25, 30, win_width - 25, win_height - 30, fill=self.colors[i],
								     style=PIESLICE, start=start,
								     extent=360 / len(self.data), width=2)
			circle.append([part, start, self.colors[i], self.data[i]])

		while step != 0:
			for i, part in enumerate(circle):
				circle[i][1] -= step
				if circle[i][1] <= -360:
					circle[i][1] += 360
				start = float(t_canvas.itemconfigure(part[0], 'start')[4])
				end = start + float(t_canvas.itemconfigure(part[0], 'extent')[4])
				start = circle[i][1]
				t_canvas.itemconfigure(circle[i][0], start=start)

			al_rotate_times += 1
			if r_t - al_rotate_times < 50 and (r_t - al_rotate_times) % 10 == 0:
				step -= 1

		for i in range(len(circle)):
			start = float(t_canvas.itemconfigure(circle[i][0], 'start')[4])
			end = start + float(t_canvas.itemconfigure(circle[i][0], 'extent')[4])
			if 90 > start and 90 < end:
				return i
			elif start == 90 or end == 90:
				return -1
		return -1


	def roll(self, rotate_times):
		if self.is_going:
			self.config_winner()
			self.al_rotate_times += 1
			if rotate_times - self.al_rotate_times < 50 and (rotate_times - self.al_rotate_times) % 10 == 0:
				self.step -= 1
			if self.step == 0:
				self.is_going = False
				pygame.mixer.pause()
				self.huawei_cap_label.place(x=win_width + 50, y = win_height // 2 - 200)
				winner_ind = self.check_winner(90)
				if winner_ind == -2:
					winner_ind = self.check_winner(90)
				if winner_ind != -1:
					self.times += 1
					self.temp_winner.append(self.data[winner_ind])
					text = ''

					if self.times < 8:
						for i in range(len(self.temp_winner)):
							if i % 2 != 0:
								text += self.temp_winner[i] + '\n'
							else:
								text += self.temp_winner[i] + '  '
						self.label_price_3['text'] = text

					if self.times < 13 and self.times >= 8:
						for i in range(7, len(self.temp_winner)):
							if i % 2 == 0:
								text += self.temp_winner[i] + '\n'
							else:
								text += self.temp_winner[i] + ' '
						self.label_price_2['text'] = text

					if self.times < 15 and self.times >= 13:
						for i in range(12, len(self.temp_winner)):
							if i % 2 != 0:
								text += self.temp_winner[i] + '\n'
							else:
								text += self.temp_winner[i] + ' '
						self.label_price_1['text'] = text

					if self.times < 16 and self.times >= 15:
						for i in range(14, len(self.temp_winner)):
							if i % 2 == 0:
								text += self.temp_winner[i] + '\n'
							else:
								text += self.temp_winner[i] + ' '
						self.label_price_s['text'] = text


					if self.times == 7:
						self.price_3['state'] = 'disabled'
						self.price_2['state'] = 'normal'
					if self.times == 12:
						self.price_2['state'] = 'disabled'
						self.price_1['state'] = 'normal'
					if self.times == 14:
						self.price_1['state'] = 'disabled'
						self.price_s['state'] = 'normal'
					if self.times == 16:
						self.price_s['state'] = 'disabled'
						text = ''
						for i in range(len(self.data)):
							if i % 2 != 0:
								text += self.data[i] + '\n'
							else:
								text += self.data[i] + ' '
						Label(self.win, image=price[-1]).place(x=1360, y=800)
						self.failed_label.place(x=1500, y=800)
						self.label_price_failed['text'] = text
						# self.names[winner_ind][0]['fg'] = 'black'
						# self.names[self.check_winner(90)][0]['bg'] = self.default_color
						self.reset_name_color()
						self.huawei_cap_label.place_forget()
						self.broadcast_winner("借酒消愁", price[-2])

					del self.data[winner_ind]
					del self.circle[winner_ind]
					del self.img_names[winner_ind]
					del self.imgs[winner_ind]
					if self.times != 16:
						self.names[winner_ind][0]['bg'] = "#ff00ff"
						self.names[winner_ind][0]['fg'] = "black"
					del self.names[winner_ind]
					del self.colors[winner_ind]
					for i in range(len(self.circle)):
						self.names[i][1]['bg'] = self.circle[i][2]
				else:
					self.broadcast_winner("卡住了", self.stuck)
					# messagebox.showinfo("Oh my god", "正好卡在中间...")

			self.win.after(1, self.roll, rotate_times)

	def check_winner(self, angle):
		for i in range(len(self.circle)):
			start = float(self.c.itemconfigure(self.circle[i][0], 'start')[4])
			end = start + float(self.c.itemconfigure(self.circle[i][0], 'extent')[4])
			if angle > start and angle < end:
				return i
			elif start == 90 or end == 90:
				return -1
		return -2

	def config_winner(self):
		for i, part in enumerate(self.circle):
			self.circle[i][1] -= self.step
			if self.circle[i][1] <= -360:
				self.circle[i][1] += 360
			start = float(self.c.itemconfigure(part[0], 'start')[4])
			end = start + float(self.c.itemconfigure(part[0], 'extent')[4])
			if 90 > start and 90 < end:
				self.reset_name_color()
				self.broadcast_winner(part[3], self.imgs[i])
				self.winner = part
				self.names[i][0]['fg'] = 'red'
				self.names[i][0]['bg'] = 'yellow'
			start = self.circle[i][1]
			self.c.itemconfigure(self.circle[i][0], start=start)

	def reset_name_color(self):
		for name in self.names:
			name[0]['fg'] = 'black'
			name[0]['bg'] = self.default_color

	def broadcast_winner(self, name, img):
		self.winner_img = img
		self.winner_img_label['image'] = self.winner_img
		self.winner_label['text'] = name + ' !!!'


if __name__ == '__main__':
	GAME_SOUND.play(-1)
	Show()
