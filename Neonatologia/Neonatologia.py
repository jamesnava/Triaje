from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Consulta_Galen import queryGalen
from Neonatologia.consultaNeonatologia import Consulta

class DATOSGENERALES():
	
	def __init__(self,usuario,dni):
		self.usuario=usuario
		self.dni=dni
		self.obj_Galen=queryGalen()
		self.obj_ConsultaNeo=Consulta()
		
	def Llenar_Tabla(self,Tabla,consulta):
		if consulta=="INTERMEDIO":
			self.LimpiarTabla(self.table_Intermedio)

		elif consulta=="UCIN":
			pass
	def LimpiarTabla(self,tabla):				
		for item in tabla.get_children():
			tabla.delete(item)
	def Top_AddPaciente(self):
		self.dniMadre=None
		self.hclRecienN=None
		self.TopDatos=Toplevel()
		self.TopDatos.geometry("700x300")
		self.TopDatos.title("Ingresar Datos")
		self.TopDatos.grab_set()
		label=Label(self.TopDatos,text="DNI MADRE")
		label.grid(row=1,column=1)
		self.entry_DNIMADRE=ttk.Entry(self.TopDatos)
		self.entry_DNIMADRE.grid(row=1,column=2)
		self.entry_DNIMADRE.bind("<Return>",lambda event:self.event_Entry(event,'MADRE') )

		label=Label(self.TopDatos,text="DATOS MADRE ")
		label.grid(row=1,column=3)
		self.entry_DatosMadre=ttk.Entry(self.TopDatos,width=30)
		self.entry_DatosMadre.grid(row=1,column=4)

		
		label=Label(self.TopDatos,text="HCL NACIDO")
		label.grid(row=2,column=1,pady=5)
		self.entry_HCLRN=ttk.Entry(self.TopDatos)
		self.entry_HCLRN.grid(row=2,column=2,pady=5)
		self.entry_HCLRN.bind("<Return>",lambda event:self.event_Entry(event,'NACIDO') )

		label=Label(self.TopDatos,text=" DATOS NACIDO ")
		label.grid(row=2,column=3,pady=5)
		self.entry_DatosRN=ttk.Entry(self.TopDatos,width=30)
		self.entry_DatosRN.grid(row=2,column=4,pady=5)

		label=Label(self.TopDatos,text="EDAD GESTACIONAL")
		label.grid(row=3,column=1,pady=5)
		self.entry_EdadGestacional=ttk.Entry(self.TopDatos)
		self.entry_EdadGestacional.grid(row=3,column=2,pady=5)

		label=Label(self.TopDatos,text="PROCEDENCIA MADRE")
		label.grid(row=3,column=3,pady=5)
		self.entry_ProcedenciaMadre=ttk.Entry(self.TopDatos,width=30)
		self.entry_ProcedenciaMadre.grid(row=3,column=4,pady=5)
		
		label=Label(self.TopDatos,text="TIPO PARTO")
		label.grid(row=4,column=1,pady=5)
		self.comboParto=ttk.Combobox(self.TopDatos,values=['EUTOCICO','DISTOCICO','CESARIA'],width=25)
		self.comboParto.grid(row=4,column=2,pady=5)
		self.comboParto.current(0)

		label=Label(self.TopDatos,text="LUGAR NACI.")
		label.grid(row=4,column=3,pady=5)
		self.combo_LUGARNACI=ttk.Combobox(self.TopDatos,values=['Hospital','Puesto Salud','Centro Salud','Trayectoria','Domicilio'],width=25)
		self.combo_LUGARNACI.grid(row=4,column=4,pady=5)
		self.combo_LUGARNACI.current(0)

		label=Label(self.TopDatos,text="SERVICIO")
		label.grid(row=5,column=1,pady=5)
		self.comboServicioL=ttk.Combobox(self.TopDatos,width=25)
		self.comboServicioL.grid(row=5,column=2,pady=5)
		self.llenar_ServicioL()
		#self.comboServicioL.current(0)


		buttonAdd=ttk.Button(self.TopDatos,text="Guardar")
		buttonAdd.grid(row=6,column=3,pady=5)
		buttonAdd['command']=self.insert_DatosPaciente

	def llenar_ServicioL(self):
		rows=self.obj_ConsultaNeo.get_Destinos()
		datos=[]
		for val in rows:
			datos.append(str(val.ID_DESTINO)+"-"+val.NOMBRE_DESTINO)
		if len(datos):
			self.comboServicioL['values']=datos
			self.comboServicioL.current(0)

	def insert_DatosPaciente(self):
		#recuperando datos
		dnimadre=self.dniMadre
		historiaNacido=self.hclRecienN		
		edadgestacional=self.entry_EdadGestacional.get()
		procedenciaMadre=self.entry_ProcedenciaMadre.get()
		tipoParto=self.comboParto.get()
		lugarNacimiento=self.combo_LUGARNACI.get()
		
		if dnimadre and historiaNacido:
			nro,IdIngreso=self.obj_ConsultaNeo.InsertarDatosGenerales(historiaNacido,dnimadre,edadgestacional,lugarNacimiento,tipoParto,procedenciaMadre)			
			if nro:
				messagebox.showinfo("Notificación","Se insertó correctamente!")
				idDP=int(self.comboServicioL.get()[:self.comboServicioL.get().find("-")])				
				self.obj_ConsultaNeo.InsertarINGRESO(IdIngreso,idDP)
				self.TopDatos.destroy()
				
		else:
			messagebox.showerror("Alerta","llene los campos Obligatorios")
			
	def event_Entry(self,event,manejador):
		
		if manejador=='MADRE':
			dni=self.entry_DNIMADRE.get()
			rows=self.obj_Galen.query_datosPaciente(dni)
			if len(rows)>0:
				self.dniMadre=dni
				nombresmadres=rows[0].PrimerNombre+" "+rows[0].ApellidoPaterno+" "+rows[0].ApellidoMaterno
				self.entry_DatosMadre.delete(0,'end')
				self.entry_DatosMadre.insert("end",nombresmadres)
		else:
			hclRN=self.entry_HCLRN.get()
			rows=self.obj_Galen.query_PacienteXHCL(hclRN)
			if len(rows)>0:
				self.hclRecienN=hclRN
				nombresNacido=rows[0].PrimerNombre+" "+rows[0].ApellidoPaterno+" "+rows[0].ApellidoMaterno
				self.entry_DatosRN.delete(0,'end')
				self.entry_DatosRN.insert("end",nombresNacido)
	

