import sys
import os
import sqlite3
import random
from tkinter import *
import tkinter as tk
import tkinter.messagebox as msg

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

		self.tasks_frame = tk.Frame(self)
		self.title("Student Database")
		self.geometry("400x400")

		menu = Menu(self)
		filemenu = Menu(menu)

		self.config(menu=menu)
		menu.add_cascade(label = "File",menu = filemenu)
		filemenu.add_command(label="New",command = self.newFile)
		#filemenu.add_command(label = "New")

		self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

		self.search_input = Entry(self)
		self.button_print = tk.Button(self, text='Print To Terminal',command=self.print_all)
		self.search_label = Label(self,text = "Search...")
		self.button_find = tk.Button(self,text = 'Search For Student', command = self.find_student)
		self.delete_input = tk.Entry(self)
		self.delete_label = tk.Label(self,text = "Delete Student") 
		self.button_delete = tk.Button(self,text = "Delete",command = self.remove_student)
		self.add_input = tk.Entry(self)
		self.add_label = tk.Label(self,text = "Add Student")
		self.button_add = tk.Button(self,text = "Add Student",command=self.input_student)
		
		self.search_input.pack(anchor = 'w',padx = 2,pady =2)
		self.search_label.pack(anchor = 'w',padx = 2,pady =2)
		self.button_find.pack(side= TOP,anchor='e',padx = 2,pady =2)	
		self.delete_input.pack(anchor = 'w',padx = 2,pady =2)
		self.delete_label.pack(anchor = 'w',padx = 2,pady =2)
		self.button_delete.pack(anchor='e',padx = 2,pady =2)
		self.add_input.pack(anchor = 'w',padx = 2,pady =2)
		self.add_label.pack(anchor = 'w',padx = 2,pady =2)
		self.button_add.pack(anchor='e',padx = 2,pady =2)

		self.button_print.pack(side = BOTTOM,padx = 5,pady =5,anchor='w')
		self.add_input.focus()
		
		self.bind("<Return>", self.input_student)
		
	def find_student(self,event=None):	
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
			#self.popup(notFind)
			
			self.search_label.configure(text = notFind)
			conn.close()
			return False
		
		conn.close()
	def print_all(self,event=None):
		command = "SELECT * FROM students"
		Data.runQuery(command)


	def insert_student(self,stu):

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

		SID_Del = self.delete_input.get()
		print(SID_Del)
		check = self.find_student(SID_Del)
		conn = sqlite3.connect('example.db')
		curs = conn.cursor()
		print(check)
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
		#s = student(sid,name,age,debt)
		self.insert_student(s)

	# def popup(self,event = None,message = " "):
	# 	pop = tk.Frame(self)
	# 	self.labe_msg = Label(self,text = message).pack()

	def newFile(self,event=None):
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

		f = open('name.txt')

		c = 0
		names = []
		while c != 88798:

			entry = f.readline()

			line = entry.split(" ")
			add_entry = student(random.randint(100000,999999),line[0],random.randint(00,99),random.randint(0000000,9999999))
			names.append(add_entry)
		
			c += 1

		for entry in names:
			#print(entry)
			self.insert_student(entry)
		f.close()

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



def menu():
	print("========================")
	print(" 1: Add Students ",'\n', "2: Find by SID",
		'\n',"3: Delete by SID",'\n',"4: Print All",
		'\n',"5: Add Student: ",'\n',"6: Quit")
	print("========================")



if __name__ == "__main__":
	if not os.path.isfile("example.db"):
		Data.firstTimeDB()

	data = Data()
	data.mainloop()