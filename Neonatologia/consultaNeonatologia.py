import conect_bd
from tkinter import messagebox
import pyodbc
class Consulta(object):

	def __init__(self):
		self.obj_conectar=conect_bd.Conexion_Triaje()
		self.obj_conectar.ejecutar_conn()
		self.cursor=self.obj_conectar.get_cursor()

	def get_id(self,Tabla,idd):		
		try:
			rows=[]
			sql=f"""SELECT MAX({idd}) AS ID FROM {Tabla}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def InsertarDatosGenerales(self,HCLRN,DNIMADRE,EDADGESTA,LUGARNACIMIENTO,TIPOPARTO,PROCEDENCIA):

		rowsId=self.get_id('DATOS_PACIENTE','Id_DP')
		nro=0
		
		if not rowsId[0].ID==None:
			nro=rowsId[0].ID+1
		else:
			nro=1
		
		sql=f"""INSERT INTO DATOS_PACIENTE VALUES({nro},'{HCLRN}','{DNIMADRE}','{EDADGESTA}','{LUGARNACIMIENTO}','{TIPOPARTO}','{PROCEDENCIA}')"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount,nro

	def InsertarINGRESO(self,Id_DP,Id_DESTINO):
		rowsId=self.get_id('INGRESO','ID_INGRESO')
		nro=0		
		if not rowsId[0].ID==None:
			nro=rowsId[0].ID+1
		else:
			nro=1
		
		sql=f"""INSERT INTO INGRESO VALUES({nro},{Id_DP},{Id_DESTINO},0,0)"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount


	def get_Destinos(self):
		rows=[]
		sql="SELECT * FROM DESTINO"
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	def get_codigo(self,Tabla,columna,nombre):		
		try:
			rows=[]
			sql=f"""SELECT *  FROM {Tabla} WHERE {columna}='{nombre}'"""

			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_Ingresos(self,servicio):
		rows=[]
		sql=f"""SELECT * FROM INGRESO AS INGRE INNER JOIN DATOS_PACIENTE AS DP 
		ON INGRE.Id_DP=DP.Id_DP AND INGRE.ESTADOI=0 AND INGRE.ID_DESTINO={servicio}"""
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	def consulta_XAlta(self,servicio):
		rows=[]
		sql=f"""SELECT * FROM INGRESO AS INGRE INNER JOIN DATOS_PACIENTE AS DP 
		ON INGRE.Id_DP=DP.Id_DP AND (INGRE.ESTADOA=0 AND INGRE.ESTADOI=1) AND INGRE.ID_DESTINO={servicio}"""
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	def query_cie10(self,descrip):
		rows=[]
		sql=f"""SELECT * FROM CIE WHERE NOMBRE LIKE '%{descrip}%'"""
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	def InsertarDatosIngreso(self,fecha,hora,peso,medico,enfermera,tecenfermera,usuario,dx,idingreso):
		rowsId=self.get_id('DATOS_INGRESO','Id_DATOSINGRESO')
		nro=0		
		if not rowsId[0].ID==None:
			nro=rowsId[0].ID+1
		else:
			nro=1
		
		sql=f"""INSERT INTO DATOS_INGRESO VALUES({nro},'{fecha}','{hora}',{peso},'{medico}','{enfermera}','{tecenfermera}','{usuario}','{dx}',{idingreso})"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount

	def update_Tabla(self,tabla,columna,valor,columnaCondicion,valorCondicion):
		sql=f"""UPDATE {tabla} SET {columna}={valor} WHERE {columnaCondicion}={valorCondicion}"""
		self.cursor.execute(sql)
		self.cursor.commit()

	def get_FechaIngresoPaciente(self,IdIngreso):
		rows=[]
		sql=f"""SELECT TOP 1 FECHA FROM DATOS_INGRESO WHERE ID_INGRESO={IdIngreso} ORDER BY ID_INGRESO DESC"""
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	def InsertarDatosAlta(self,peso,fechaalta,medico,enfermera,tecenfermera,diasH,observacion,usuario,destino,dx,idingreso,hora):
		rowsId=self.get_id('ALTA','ID_ALTA')
		nro=0		
		if not rowsId[0].ID==None:
			nro=rowsId[0].ID+1
		else:
			nro=1
		
		sql=f"""INSERT INTO ALTA VALUES({nro},{peso},'{fechaalta}','{medico}','{enfermera}','{tecenfermera}',{diasH},
		'{observacion}','{usuario}',{destino},'{dx}',{idingreso},'{hora}')"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount

	def DeleteItemTable(self,Table,columnCondition,valueCondition):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			sql=f"""DELETE FROM {Table} WHERE {columnCondition}={valueCondition}"""
			cursor.execute(sql)
			cursor.commit()
			return self.cursor.rowcount
		except pyodbc.Error as e:			
			return None
		finally:
			obj_conectar.close_conection()
		

	def get_LastIdQuery(self,tabla,Paramcolumna,Paramvalor,OutputColumn):
		rows=[]
		sql=f"""SELECT TOP 1 * FROM {tabla} WHERE {Paramcolumna}={Paramvalor} ORDER BY {OutputColumn} DESC"""
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows


