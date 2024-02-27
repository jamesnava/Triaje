import conect_bd
from tkinter import messagebox
class Consulta(object):

	def __init__(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		self.cursor=obj_conectar.get_cursor()
	
	def insertarMadre(self,dni,grupof,rpm,hta,itu3,dosis):
		nro=0
		IdM=self.get_id('MADRE','IDMADRE')
		nro=IdM[0].ID		
		if nro==None:
			nro=1
		else:
			nro=nro+1
		
		sql=f"""INSERT INTO MADRE VALUES({nro},'{dni}','{grupof}','{rpm}','{hta}','{itu3}','{dosis}',0,0)"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount
	def deleteMadre(self,idMadre):
		try:
			sql=f"""DELETE FROM MADRE WHERE IDMADRE={idMadre}"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			messagebox.showerror("Error",e)
		
		
	def insertParto(self,procedencia,idmadre,hiso,heso,hisp,tipoP):
		nro=0
		IdP=self.get_id('PARTO','ID_PARTO')
		nro=IdP[0].ID
		if nro==None:
			nro=1
		else:
			nro=nro+1

		#print(nro,procedencia,idmadre,hiso,heso,hisp,tipoP)
		try:
			sql=f"""INSERT INTO PARTO VALUES({nro},'{procedencia}',{idmadre},'{hiso}','{heso}','{hisp}','{tipoP}')"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			messagebox.showerror("Notificación",f"Error {e}")
		

	def get_id(self,Tabla,idd):
		
		try:
			rows=[]
			sql=f"""SELECT MAX({idd}) AS ID FROM {Tabla}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_Tabla(self,Tabla,condicion1,condicion2,valor1,valor2):
		try:
			rows=[]
			sql=f"""SELECT * FROM {Tabla} WHERE {condicion1}={valor1} OR {condicion2}={valor2}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_TablaALL(self):
		try:
			rows=[]
			sql=f"""SELECT A.Id_AIR,M.IDMADRE,M.DNI AS MADRE,A.HCL AS NACIDO,A.CNV,A.HCL FROM MADRE AS M INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE AND M.estadoPARTO=1 AND M.estadoAIRN=1 AND A.estado=0"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)	

	def Update_Tabla(self,Tabla,variable,valorVariable,condicion,valor):
		sql=f"""UPDATE {Tabla} SET {variable}={valorVariable} WHERE {condicion}={valor}"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount

	def Insert_AIRN(self,datos,fechaN,iduser):
		nro=0
		IdAirn=self.get_id('AIR','Id_AIR')
		nro=IdAirn[0].ID
		if nro==None:
			nro=1
		else:
			nro=nro+1
		try:

			sql=f"""INSERT INTO AIR VALUES({nro},'{datos[0]}','{datos[1]}','{datos[2]}','{datos[3]}','{datos[4]}','{datos[5]}',{datos[6]},{datos[7]},
			{datos[8]},{datos[9]},{datos[10]},{datos[11]},{datos[12]},{datos[13]},{datos[14]},{datos[15]},{datos[16]},{datos[17]},'{datos[18]}','{datos[19]}',
			'{datos[20]}','{datos[21]}','{datos[22]}','{datos[23]}','{datos[24]}','{datos[25]}','{datos[26]}','{datos[27]}','{datos[28]}','{datos[29]}','{datos[30]}',0,'{fechaN}',0,{iduser},{datos[31]})"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount,nro
		except Exception as e:
			messagebox.showerror("Error",f"No se pudo insertar {e} \n se requiere llenar todos los campos!!")

	def insertarDxAIR(self,codcie,idair):
		try:
			sql=f"""INSERT INTO DXAIRN VALUES('{codcie}',{idair})"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			messagebox.showerror("Error",f"No se pudo insertar {e}")		

	def Insert_RESATENCION(self,datos,tecnicaE,air):
		nro=0
		IdRes=self.get_id('RES_ATENCION','ID_RESPONSABLE')
		nro=IdRes[0].ID

		if nro==None:
			nro=1
		else:
			nro=nro+1
		
		try:
			sql=f"""INSERT INTO RES_ATENCION VALUES({nro},'{datos[0]}','{tecnicaE}','{datos[1]}','{datos[2]}',{air})"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			messagebox.showerror('Error',e)		

	def ConsultaIngresaAlojamiento(self):
		try:
			rows=[]
			sql=f"""SELECT M.DNI,A.HCL,A.Id_AIR FROM AIR AS A INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE  AND A.estado=1 AND A.estadoAlojamiento=0"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)
			
	def insert_Alojamiento(self,datos):
		nro=0
		IdRes=self.get_id('ALOJAMIENTO','ID_ALOJAMIENTO')
		nro=IdRes[0].ID
		if nro==None:
			nro=1
		else:
			nro=nro+1
		sql=f"""INSERT INTO ALOJAMIENTO VALUES({nro},'{datos[0]}','{datos[1]}','{datos[2]}','{datos[3]}','{datos[4]}','{datos[5]}',{datos[6]})"""		
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount


	def Report_General(self,desde,hasta):
		rows=[]
		sql=f"""SELECT * FROM ALOJAMIENTO AS AL INNER JOIN AIR AS A ON AL.Id_AIR=A.Id_AIR INNER JOIN MADRE
		 AS M ON M.IDMADRE=A.IDMADRE INNER JOIN PARTO AS PA ON PA.IDMADRE=M.IDMADRE AND AL.FECHA_ALTA BETWEEN '{desde}' AND '{hasta}' """
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	def consulta_datosAir(self,id_air):
		try:
			rows=[]
			sql=f"""SELECT * FROM AIR AS A INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE INNER JOIN PARTO AS P ON M.IDMADRE=P.IDMADRE AND A.Id_AIR={id_air}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_DigitadosAIRN(self):
		try:
			rows=[]
			sql=f"""SELECT TOP 50 M.DNI,M.GRUPO_FACTOR,A.HCL FROM MADRE AS 
			M INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE AND M.estadoAIRN=1 AND M.estadoPARTO=1 AND A.estado=1 """
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_DigitadosAIRNLike(self,hcl):
		try:
			rows=[]
			sql=f"""SELECT  M.DNI,M.GRUPO_FACTOR,A.HCL FROM MADRE AS 
			M INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE AND M.estadoAIRN=1 AND M.estadoPARTO=1 AND A.estado=1 AND A.HCL LIKE '{hcl}%'"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_DigitadosAlojamiento(self):
		try:
			rows=[]
			sql=f"""SELECT M.DNI,A.HCL FROM AIR AS A INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE AND A.estadoAlojamiento=1"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_DigitadosAlojamientoLike(self,hcl):
		try:
			rows=[]
			sql=f"""SELECT M.DNI,A.HCL FROM AIR AS A INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE AND A.estadoAlojamiento=1 AND A.HCL LIKE '{hcl}%'"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)
		