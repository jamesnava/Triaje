import pyodbc
from tkinter import messagebox
import configparser

class Conexion_Galen(object):
	def __init__(self):
		self.configuracion=configparser.ConfigParser()
		self.configuracion.read('config_GALEN.ini')
	def ejecutar_conn(self):
		servidor=self.configuracion['DEFAULT']['SERVER']
		bd=self.configuracion['DEFAULT']['DATABASE']
		user=self.configuracion['DEFAULT']['USER']
		password=self.configuracion['DEFAULT']['PASSWORD']
		driver='{SQL Server}'					
		self.conn = pyodbc.connect(f"""DRIVER={driver};SERVER={servidor};DATABASE={bd};UID={user};PWD={password}""")		
	def get_cursor(self):
		try:
			self.puntero=self.conn.cursor()
			return self.puntero
		except Exception as e:
			messagebox.showinfo('Notificación','No pudo conectarse al servidor SISGALENPLUS')		
		
	def close_conection(self):
		self.conn.close()

class Conexion_Triaje(object):
	def __init__(self):
		self.configuracion=configparser.ConfigParser()
		self.configuracion.read('config_Triaje.ini')
	def ejecutar_conn(self):
		servidor=self.configuracion['DEFAULT']['SERVER']
		bd=self.configuracion['DEFAULT']['DATABASE']
		user=self.configuracion['DEFAULT']['USER']
		password=self.configuracion['DEFAULT']['PASSWORD']
		driver='{SQL Server}'					
		self.conn = pyodbc.connect(f"""DRIVER={driver};SERVER={servidor};DATABASE={bd};UID={user};PWD={password}""")		
	def get_cursor(self):
		try:
			self.puntero=self.conn.cursor()
			return self.puntero
		except Exception as e:
			messagebox.showinfo('Notificación','No pudo conectarse al servidor SISGALENPLUS')		
		
	def close_conection(self):		
		self.conn.close()

class Conexion_Externo(object):
	def __init__(self):
		self.configuracion=configparser.ConfigParser()
		self.configuracion.read('config_EXT.ini')
	def ejecutar_conn(self):
		servidor=self.configuracion['DEFAULT']['SERVER']
		bd=self.configuracion['DEFAULT']['DATABASE']
		user=self.configuracion['DEFAULT']['USER']
		password=self.configuracion['DEFAULT']['PASSWORD']
		driver='{SQL Server}'					
		self.conn = pyodbc.connect(f"""DRIVER={driver};SERVER={servidor};DATABASE={bd};UID={user};PWD={password}""")		
	def get_cursor(self):
		try:
			self.puntero=self.conn.cursor()
			return self.puntero
		except Exception as e:
			messagebox.showinfo('Notificación','No pudo conectarse al servidor SISGALENPLUS')		
		
	def close_conection(self):
		self.puntero.close()
		self.conn.close()

