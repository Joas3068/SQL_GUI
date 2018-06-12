import sys
import os
import sqlite3
import random
from Data import Data
from tkinter import *
import tkinter as tk
import tkinter.messagebox as msg


if __name__ == "__main__":
	if not os.path.isfile("example.db"):
		Data.firstTimeDB()

	data = Data()
	data.mainloop()
