import sys
import os
import sqlite3
import random
from tkinter import *
import itertools
import tkinter as tk


class student:
	def __init__(self,SID = 0,Name="",Age=0,Debt=0):
		self.SID = SID
		self.Name = Name
		self.Age = Age
		self.Debt = Debt


	@property
	def full_set(self):
		return '{} {} {} {}'.format(self.SID,self.Name, self.Age,self.Debt)
	
	def __repr__(self):
		return "student({},'{}',{},{})".format(self.SID,self.Name,self.Age,self.Debt)

class Data(tk.Tk):
	def __init__(self):
		super().__init__()
		
		stu = student()


		#self.tasks_canvas = tk.Canvas(self)
		try:
			self.wm_iconbitmap("@/usr/include/X11/bitmaps/tie_fighter")
		except:
			pass
		
		self.tasks_frame = tk.Frame(self)
		self.title("Student Database")
		self.geometry("400x400")

		menu = Menu(self)
		filemenu = Menu(menu,tearoff = 0)

		self.config(menu=menu)
		menu.add_cascade(label = "Info",menu = filemenu)
		filemenu.add_command(label="Help",command = self.help)


		self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

		self.search_input = Entry(self)
		self.button_print = tk.Button(self, text='Print To Terminal',command=self.print_all)
		self.search_label = Label(self,text = "Search...")
		self.button_find = tk.Button(self,text = 'Search For Student', command = self.find_student)
		self.delete_input = tk.Entry(self)
		self.delete_label = tk.Label(self,text = "Delete Student") 
		self.button_delete = tk.Button(self,text = "Delete",command = self.remove_student)
		self.add_input = tk.Entry(self)
		self.add_label = tk.Label(self,text = "Add student example: 123456 John 33 10000")
		self.button_add = tk.Button(self,text = "Add Student",command=self.input_student)
		self.button_bulk = tk.Button(self,text = "Bulk Add",command = self.add_stuff)
		
		self.search_input.pack(anchor = 'w',padx = 2,pady =2)
		self.search_label.pack(anchor = 'w',padx = 2,pady =2)
		self.button_find.pack(side= TOP,anchor='e',padx = 2,pady =2)	
		self.delete_input.pack(anchor = 'w',padx = 2,pady =2)
		self.delete_label.pack(anchor = 'w',padx = 2,pady =2)
		self.button_delete.pack(anchor='e',padx = 2,pady =2)
		self.add_input.pack(anchor = 'w',padx = 2,pady =2)
		self.add_label.pack(anchor = 'w',padx = 2,pady =2)
		self.button_add.pack(anchor='e',padx = 2,pady =2)
		self.button_bulk.pack(side = BOTTOM,anchor='e',padx = 5,pady =5)

		self.button_print.pack(side = BOTTOM,anchor='w',padx = 5,pady =5)
		self.add_input.focus()
		
		#self.bind("<Return>", self.input_student)
		
	def find_student(self,event=None):	
		'''Search for entry by ID. Returns true if student is found'''
		SID_find = self.search_input.get()
		conn = sqlite3.connect('example.db')
		curs = conn.cursor()
		flag = False
		sql = "SELECT * FROM students WHERE SID =?"
		curs.execute(sql,[(SID_find)])

		row = curs.fetchone()
		

		while row:
			flag = True
			print("SID is:",row[0],", Name:",row[1]
				,", Age:",row[2], ", Debt:",row[3])
 
			findy = "SID is:"+str(row[0]) +" Name: " + row[1]+" Age: "+ str(row[2])+ " Debt: " + str(row[3])
			self.search_label.configure(text = findy)
			row = curs.fetchone()
			self.search_input.delete(0,END)
		if flag:
			conn.close()
			return True
		else: 
			#if not deletey:
			
			notFind = "Student Was Not Found"
			#self.error_find()
			#self.popup(notFind)
			
			self.search_label.configure(text = notFind)
			conn.close()
			return False
		
		conn.close()
	def print_all(self,event=None):
		command = "SELECT * FROM students"
		Data.runQuery(command)

	def error_find(self):
		tk.messagebox.showinfo("ERROR","Student Was Not Found")  ##print error popup
	def insert_student(self,stu):
		'''Inserts student if they are not in the database'''
		check = self.find_student(stu.SID)
		
		if not check:
			#print("Adding Student ",stu.SID,", ",stu.Name)
			#stu=student(add_field.split())
			default_student = "INSERT INTO students VALUES (:SID,:Name,:Age,:Debt)"
			default_add = {'SID':stu.SID,'Name':stu.Name,'Age':stu.Age,'Debt':stu.Debt,}
			Data.runQuery(default_student,default_add)
		else:
			print(stu.SID," Already In Database")
			
	def remove_student(self,event=None):
		''' Removes student based on ID, currently doesn't return accurate search results if ID is not in  '''
		SID_Del = self.delete_input.get()
		#check = self.find_student(SID_Del)
		conn = sqlite3.connect('example.db')
		curs = conn.cursor()
		#print(check)
		#if check:
		print("Deleting Student: ",SID_Del)
		dell = "Deleting Student: " + str(SID_Del)
		self.delete_label.configure(text = dell)
		self.delete_input.delete(0,END)
		with conn:
			curs.execute("DELETE FROM students WHERE SID = ?",[(SID_Del)])
		# else:
		# 	print("Student Not in Database")	
		# 	self.delete_label.configure(text = "Student Not in Database")
		self.delete_input.delete(0,END)	
		conn.close()


	def input_student(self, event = None):
		add_field = self.add_input.get()
		check_input = parse_input(add_field)
		self.add_input.delete(0,END)

		if check_input == False:
			print("Wrong Input")
			return False
		else:
			sp = add_field.split(" ")
			s = student(sp[0],sp[1],sp[2],sp[3])
			print(s)
			self.add_label.configure(text ="Added " +str(sp))

		self.insert_student(s)


	def help(self,event=None):
		tk.messagebox.showinfo("Info Herer","Search for students \nPrint all to find or look for students")
		print("Pressed")



	@staticmethod
	def runQuery(sql, data=None, receive=False):
		conn = sqlite3.connect("example.db")
		cursor = conn.cursor()
		row = False
		if data:
			cursor.execute(sql, data)

		else:
			cursor.execute(sql)
			rows = cursor.fetchall()
			for row in rows:
				print("SID is:",row[0],", Name:",row[1]
				,", Age:",row[2], ", Debt:",row[3])
			print("=========================================")

		if receive:

			print("meh")

		else:
			conn.commit()


		conn.close()

	@staticmethod
	def firstTimeDB():
		stu = student(0," ",0,0)
		create_tables = (""" CREATE TABLE students
		(SID integer,Name text, Age integer, Debt real) """)

		Data.runQuery(create_tables)

	def add_stuff(self):

		a = file_len("name.txt")

		b = read_count("store.txt")
		print("Press ctrl+c to stop")
		print(a,b)
		count = b
		num = 1
		try:
			names = []
			with open("name.txt") as f:
				for line in itertools.islice(f,b,a,None):
					#print(count,":",line)
					entry = line
					l = entry.split(" ")
					add_entry = student(random.randint(100000,999999),l[0],random.randint(00,99),random.randint(0000000,9999999))
					names.append(add_entry)
					#print(add_entry.SID,add_entry.Name)
					self.insert_student(add_entry)

					if count > num:
						print("Marker is at",count , "out of" ,a)
						num = count*1.05

					count +=1

		except KeyboardInterrupt:
			write_count("store.txt",count)

			print("Interrupts at",count)

			return
		write_count("store.txt",count)
		print("Finnish")
	

def parse_input(st = ""):

	out = st.split(" ")

	count = len(out)
	#print(len(out))

	if count < 4:
		print("Missed Field")
		return False

	if not out[0].isdigit() or not out[2].isdigit() or not out[3].isdigit():
		print("Non Digit Entered")
		return False

	if  len(out[0]) != 6:
		print("Input Must be 6 numbers")
		return False

	return True


def read_count(f_name = " "):

	
	try:
		f = open(f_name,"r+")
		a = f.read()
	except:
		f = open(f_name,"w")
		f.write('0')
		f.close()
		f = open(f_name,"r")
		a = f.read()

	f.close()
	return int(a)

def write_count(f_name ,count):
	with open(f_name, "w") as f:
		f.write('%d' % count)


def file_len(f_name):
	with open(f_name) as f:
		for i, l in enumerate(f):
			pass

		return i+1

