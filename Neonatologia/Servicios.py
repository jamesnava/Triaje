from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Consulta_Galen import queryGalen
from Neonatologia.consultaNeonatologia import Consulta
from tktimepicker import SpinTimePickerModern, SpinTimePickerOld
from tktimepicker import constants
from tkcalendar import DateEntry
from datetime import datetime,date



class Servicio():
	
	def __init__(self,usuario,dni,servicio):
		self.usuario=usuario
		self.servicio=servicio		
		self.dni=dni
		self.obj_Galen=queryGalen()
		self.obj_ConsultaNeo=Consulta()
		self.timeDate=datetime.now().strftime("%H:%M:%S")
	def Frame_Servicios(self,frame,width,height):
		frameM=Frame(frame,width=width,height=height,bg="#828682")
		frameM.place(x=0,y=0)
		frameM.pack_propagate(False)
		letra_leyenda=('Candara',16,'bold italic')	


		label=Label(frameM,text="Pacientes Ingresados",fg="#131D52",bg="#828682",font=('Candara',16,'bold italic'))
		label.grid(row=3,column=2,columnspan=20,pady=10)
		style=ttk.Style()
		style.theme_use("default")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','green')])
		self.table_IngresosRecepcionados=ttk.Treeview(frameM,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_IngresosRecepcionados.heading("#1",text="DNI MADRE")
		self.table_IngresosRecepcionados.column("#1",width=80,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#2",text="DATOS MADRE")
		self.table_IngresosRecepcionados.column("#2",width=250,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#3",text="HCL NACIDO")
		self.table_IngresosRecepcionados.column("#3",width=80,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#4",text="DATOS NACIDO")
		self.table_IngresosRecepcionados.column("#4",width=250,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#5",text="ESTADO INGRESO")
		self.table_IngresosRecepcionados.column("#5",width=100,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#6",text="ID")
		self.table_IngresosRecepcionados.column("#6",width=0,anchor="w",stretch='NO')							
		self.table_IngresosRecepcionados.grid(row=4,column=2,padx=10,pady=2,columnspan=20)
		self.table_IngresosRecepcionados.bind('<<TreeviewSelect>>',self.Event_ItemTable)
		self.llenar_Tabla()

		self.btnIngreso=ttk.Button(frameM,text="Datos de Ingreso",state="disabled")
		self.btnIngreso.grid(row=5,column=9,pady=10)
		self.btnIngreso['command']=self.Top_DatosIngreso

		self.btnDeleteIngreso=ttk.Button(frameM,text="Datos de Eliminar")
		self.btnDeleteIngreso.grid(row=5,column=11,pady=10)
		self.btnDeleteIngreso['command']=self.Eliminar_Ingreso

		label=Label(frameM,text="Pacientes por dar de Alta",fg="#131D52",font=('Candara',16,'bold italic'))
		label.grid(row=6,column=2,columnspan=20,pady=10)
		self.table_PacientesAlta=ttk.Treeview(frameM,columns=('#1','#2','#3','#4','#5','#6','#7'),show='headings')
		self.table_PacientesAlta.heading("#1",text="DNI MADRE")
		self.table_PacientesAlta.column("#1",width=80,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#2",text="DATOS MADRE")
		self.table_PacientesAlta.column("#2",width=250,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#3",text="HCL NACIDO")
		self.table_PacientesAlta.column("#3",width=80,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#4",text="DATOS NACIDO")
		self.table_PacientesAlta.column("#4",width=250,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#5",text="ESTADO EGRESO")
		self.table_PacientesAlta.column("#5",width=100,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#6",text="ID")
		self.table_PacientesAlta.column("#6",width=0,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#7",text="IDDP")
		self.table_PacientesAlta.column("#7",width=0,anchor="w",stretch='NO')						
		self.table_PacientesAlta.grid(row=6,column=2,padx=10,pady=2,columnspan=20)
		self.table_PacientesAlta.bind('<<TreeviewSelect>>',self.Event_ItemTableAlta)
		self.llenar_TablaAlta()

		self.btnAlta=ttk.Button(frameM,text="Alta",state="disabled")
		self.btnAlta.grid(row=7,column=9,pady=10)
		self.btnAlta['command']=self.Top_DatosAlta

		self.btnDeleteAlta=ttk.Button(frameM,text="Datos de Eliminar")
		self.btnDeleteAlta.grid(row=7,column=11,pady=10)
		self.btnDeleteAlta['command']=self.Eliminar_Alta		

	def Eliminar_Alta(self):
		if self.table_PacientesAlta.selection():
			IdIngreso=self.table_PacientesAlta.item(self.table_PacientesAlta.selection()[0],option='values')[5]
			obj=Consulta()
			obj.DeleteItemTable('DATOS_INGRESO','ID_INGRESO',IdIngreso)
			self.obj_ConsultaNeo.update_Tabla('INGRESO','ESTADOI',0,'ID_INGRESO',IdIngreso)
			self.llenar_TablaAlta()
			self.llenar_Tabla()
		else:
			messagebox.showerror("Alert","Seleccione un Item!!")

	def Eliminar_Ingreso(self):
		identificadorDelete=None
		if self.table_IngresosRecepcionados.selection():
			IdIngreso=self.table_IngresosRecepcionados.item(self.table_IngresosRecepcionados.selection()[0],option='values')[5]
			if messagebox.askyesno(title="Confirmar",message="Esta seguro que desea Eliminar"):
				rowsIdPaciente=self.obj_ConsultaNeo.get_codigo('INGRESO','ID_INGRESO',IdIngreso)
				IDDATOSPACIENTE=rowsIdPaciente[0].Id_DP				

				try:
					##eliminar
					obj=Consulta()
					obj.DeleteItemTable('INGRESO','ID_INGRESO',IdIngreso)

					obj=Consulta()
					identificadorDelete=obj.DeleteItemTable('DATOS_PACIENTE','Id_DP',IDDATOSPACIENTE)
					
					if identificadorDelete:					
						self.llenar_Tabla()
					else:
						#consulta la ultima alta... y obtener id Alta y modificar estadoAlta ingreso....
						IdIngresoLast=self.obj_ConsultaNeo.get_LastIdQuery('INGRESO','Id_DP',IDDATOSPACIENTE,'ID_INGRESO')
						idIngre=IdIngresoLast[0].ID_INGRESO
						rowsAlta=self.obj_ConsultaNeo.get_codigo('ALTA','ID_INGRESO',idIngre)
						idAlta=rowsAlta[0].ID_ALTA					
						#ELIMINAR LA ALTA Y ACTUALIZAR LA TABLA INGRESO						
						obj=Consulta()
						obj.DeleteItemTable('ALTA','ID_ALTA',idAlta)
						self.obj_ConsultaNeo.update_Tabla('INGRESO','ESTADOA',0,'ID_INGRESO',idIngre)
						self.llenar_Tabla()
				except Exception as e:
					raise e			

		else:
			messagebox.showerror("Alerta",'Seleccione un Item')


	def Event_ItemTableAlta(self,event):
		if self.table_PacientesAlta.selection():
			#id_Ingreso=self.table_PacientesAlta.item(self.table_PacientesAlta.selection()[0],option='values')[5]
			Estado_Ingreso=self.table_PacientesAlta.item(self.table_PacientesAlta.selection()[0],option='values')[4]
			if  Estado_Ingreso=="No Registrado":
				self.btnAlta.configure(state='normal')
			else:
				self.btnAlta.configure(state='disabled')

	def Event_ItemTable(self,event):
		if self.table_IngresosRecepcionados.selection():
			id_Ingreso=self.table_IngresosRecepcionados.item(self.table_IngresosRecepcionados.selection()[0],option='values')[5]
			Estado_Ingreso=self.table_IngresosRecepcionados.item(self.table_IngresosRecepcionados.selection()[0],option='values')[4]

			if  Estado_Ingreso=="No Registrado":
				self.btnIngreso.configure(state='normal')
			else:
				self.btnIngreso.configure(state='disabled')

	def llenar_Tabla(self):
		self.borrar_tabla(self.table_IngresosRecepcionados)
		#print(self.servicio)
		rows=self.obj_ConsultaNeo.consulta_Ingresos(self.servicio) if self.servicio else []

		for valor in rows:
			rowsDatosMadre=self.obj_Galen.query_datosPaciente(valor.DNI_MADRE_DP)
			rowsDatosNacido=self.obj_Galen.query_PacienteXHCL(valor.HCL_RN_DP)
			estadoIngreso= "Registrado" if valor.ESTADOI==0 else "No Registrado"
			datosnacido=rowsDatosNacido[0].PrimerNombre+" "+rowsDatosNacido[0].ApellidoPaterno+" "+rowsDatosNacido[0].ApellidoMaterno
			self.table_IngresosRecepcionados.insert('','end',values=(valor.DNI_MADRE_DP,rowsDatosMadre[0].PrimerNombre+" "+rowsDatosMadre[0].ApellidoPaterno+" "+rowsDatosMadre[0].ApellidoMaterno,valor.HCL_RN_DP,datosnacido,estadoIngreso,valor.ID_INGRESO))

	def llenar_TablaAlta(self):
		self.borrar_tabla(self.table_PacientesAlta)
		rows=self.obj_ConsultaNeo.consulta_XAlta(self.servicio) if self.servicio else []
	
		for valor in rows:
			rowsDatosMadre=self.obj_Galen.query_datosPaciente(valor.DNI_MADRE_DP)
			rowsDatosNacido=self.obj_Galen.query_PacienteXHCL(valor.HCL_RN_DP)
			estadoEgreso= "Registrado" if valor.ESTADOA==0 else "No Registrado"
			datosnacido=rowsDatosNacido[0].PrimerNombre+" "+rowsDatosNacido[0].ApellidoPaterno+" "+rowsDatosNacido[0].ApellidoMaterno
			self.table_PacientesAlta.insert('','end',values=(valor.DNI_MADRE_DP,rowsDatosMadre[0].PrimerNombre+" "+rowsDatosMadre[0].ApellidoPaterno+" "+rowsDatosMadre[0].ApellidoMaterno,valor.HCL_RN_DP,datosnacido,estadoEgreso,valor.ID_INGRESO,valor.Id_DP))

	def borrar_tabla(self,Tabla):				
		for item in Tabla.get_children():
			Tabla.delete(item)

	def Top_DatosIngreso(self):
		self.TopIngreso=Toplevel()
		self.TopIngreso.title("Datos de Ingreso")
		self.TopIngreso.geometry("500x300")
		self.TopIngreso.iconbitmap('img/ingreso.ico')
		self.TopIngreso.grab_set()
		
		label=Label(self.TopIngreso,text="Fecha")
		label.grid(row=1,column=1,pady=10)
		self.FechaIngreso=DateEntry(self.TopIngreso,selectmode='day',date_pattern='yyyy-MM-dd')
		self.FechaIngreso.grid(row=1,column=2,pady=10)

		label=Label(self.TopIngreso,text="Hora")
		label.grid(row=1,column=3,pady=10,padx=10)
		self.time_Ingreso=SpinTimePickerModern(self.TopIngreso)
		self.time_Ingreso.addAll(constants.HOURS24)
		self.time_Ingreso.setMins(str(self.timeDate).split(":")[1])
		self.time_Ingreso.set24Hrs(str(self.timeDate).split(":")[0])
		self.time_Ingreso.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
		self.time_Ingreso.configure_separator(bg="#404040",fg="#fff")
		self.time_Ingreso.grid(row=1,column=4,padx=10,pady=10)

		label=Label(self.TopIngreso,text="Peso")
		label.grid(row=2,column=1,pady=10)
		self.entry_PesoE=ttk.Spinbox(self.TopIngreso,from_=100,to=4000,increment=0.1)
		self.entry_PesoE.grid(row=2,column=2,pady=10)

		label=Label(self.TopIngreso,text="Medico Resp")
		label.grid(row=2,column=3,pady=10)
		self.entry_MedicoResponsableIngreso=ttk.Entry(self.TopIngreso)
		self.entry_MedicoResponsableIngreso.grid(row=2,column=4,pady=10)
		self.entry_MedicoResponsableIngreso.bind("<Return>",lambda event:self.Search_Personal(event,"DOCTOR"))

		label=Label(self.TopIngreso,text="Enf. Resp")
		label.grid(row=3,column=1,pady=10)
		self.entry_EnfermeraResponsableIngreso=ttk.Entry(self.TopIngreso)
		self.entry_EnfermeraResponsableIngreso.grid(row=3,column=2,pady=10)
		self.entry_EnfermeraResponsableIngreso.bind("<Return>",lambda event:self.Search_Personal(event,"ENFERMERA"))

		label=Label(self.TopIngreso,text="Tecnico Resp")
		label.grid(row=3,column=3,pady=10)
		self.entry_TecnicoResponsableIngreso=ttk.Entry(self.TopIngreso)
		self.entry_TecnicoResponsableIngreso.grid(row=3,column=4,pady=10)

		label=Label(self.TopIngreso,text="Cod DX")
		label.grid(row=4,column=1,pady=10)
		self.entry_CodDX=ttk.Entry(self.TopIngreso)
		self.entry_CodDX.grid(row=4,column=2,pady=10)
		self.entry_CodDX.bind("<Return>",lambda event:self.Search_Personal(event,"DX"))

		label=Label(self.TopIngreso,text="Diagnostico")
		label.grid(row=4,column=3,pady=10)
		self.entry_DX=ttk.Entry(self.TopIngreso)
		self.entry_DX.grid(row=4,column=4,pady=10)

		buttonAdd=ttk.Button(self.TopIngreso,text="Aceptar")
		buttonAdd.grid(row=5,column=2,columnspan=2,pady=10)
		buttonAdd['command']=self.insert_DatosIngreso


	def Search_Personal(self,event,identificador):
		self.personall=None
		if identificador=="DOCTOR":
			self.personall="DOCTOR"
			self.Top_searchPersonal()		
		elif identificador=="ENFERMERA":
			self.personall="ENFERMERA"
			self.Top_searchPersonal()
		elif identificador=="MEDICOA":
			self.personall="MEDICOA"
			self.Top_searchPersonal()
		elif identificador=="ENFERMERAA":
			self.personall="ENFERMERAA"
			self.Top_searchPersonal()
		elif identificador=="DXA":
			self.personall="DXA"
			self.Top_searchPersonal()

		elif identificador=="DX":
			self.personall="DX"
			self.Top_searchPersonal()

	def Top_searchPersonal(self):
		self.TopGeneral=Toplevel()
		self.TopGeneral.title('Datos Personales')
		self.TopGeneral.iconbitmap('img/centro.ico')
		self.TopGeneral.geometry("550x350+350+50")
		self.TopGeneral.focus_set()	
		self.TopGeneral.grab_set()
		self.TopGeneral.resizable(0,0)	

		label_title=Label(self.TopGeneral,text='Buscar')
		label_title.place(x=20,y=20)
		self.Entry_buscar_General=ttk.Entry(self.TopGeneral,width=30)
		self.Entry_buscar_General.focus()
		self.Entry_buscar_General.place(x=80,y=20)
		self.Entry_buscar_General.bind('<Key>',self.buscar_DatosPersonales)		

		#tabla...
		self.table_General=ttk.Treeview(self.TopGeneral,columns=('#1','#2'),show='headings')		
		self.table_General.heading("#1",text="CODIGO")
		self.table_General.column("#1",width=100,anchor="center")
		self.table_General.heading("#2",text="DATOS")
		self.table_General.column("#2",width=400,anchor="center")										
		self.table_General.place(x=10,y=70)
		self.table_General.bind('<<TreeviewSelect>>',self.itemTable_selected)			
		#botones de accion
		self.btn_TPG_Close=ttk.Button(self.TopGeneral,text='Cerrar')
		self.btn_TPG_Close.place(x=280,y=365)
		#self.btn_TPG_Close['command']=lambda :self.TopGeneral.destroy()

	def buscar_DatosPersonales(self,event):		
		if self.personall=="DX" or self.personall=="DXA":			
			parametro=''
			self.borrar_tabla(self.table_General)
			if len(self.Entry_buscar_General.get())!=0:
				parametro=parametro+self.Entry_buscar_General.get()
				rows=self.obj_ConsultaNeo.query_cie10(parametro)
				for valores in rows:
					self.table_General.insert('','end',values=(valores.CODCIE,valores.NOMBRE))

		else:
			self.obj_Galen=queryGalen()
			parametro=''
			self.borrar_tabla(self.table_General)
			if len(self.Entry_buscar_General.get())!=0:
				parametro=parametro+self.Entry_buscar_General.get()
				rows=self.obj_Galen.query_Empleado(parametro)
				for valores in rows:
					self.table_General.insert('','end',values=(valores.DNI,valores.Nombres+" "+valores.ApellidoPaterno+" "+valores.ApellidoMaterno))

	def itemTable_selected(self,event):
		if len(self.table_General.focus())!=0:
			if self.personall=="DOCTOR":				
				self.entry_MedicoResponsableIngreso['state']="normal"
				self.entry_MedicoResponsableIngreso.delete(0,'end')
				self.entry_MedicoResponsableIngreso.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_MedicoResponsableIngreso['state']="readonly"	
				self.TopGeneral.destroy()

			if self.personall=="MEDICOA":				
				self.entry_MedicoResponsableEgreso['state']="normal"
				self.entry_MedicoResponsableEgreso.delete(0,'end')
				self.entry_MedicoResponsableEgreso.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_MedicoResponsableEgreso['state']="readonly"	
				self.TopGeneral.destroy()	

			elif self.personall=="ENFERMERA":
				self.entry_EnfermeraResponsableIngreso['state']="normal"
				self.entry_EnfermeraResponsableIngreso.delete(0,'end')
				self.entry_EnfermeraResponsableIngreso.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_EnfermeraResponsableIngreso['state']="readonly"	
				self.TopGeneral.destroy()

			elif self.personall=="ENFERMERAA":
				self.entry_EnfermeraResponsableEgreso['state']="normal"
				self.entry_EnfermeraResponsableEgreso.delete(0,'end')
				self.entry_EnfermeraResponsableEgreso.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_EnfermeraResponsableEgreso['state']="readonly"	
				self.TopGeneral.destroy()

			elif self.personall=="DXA":
				self.entry_DxAlta['state']="normal"
				self.entry_DxAlta.delete(0,'end')
				self.entry_DxAlta.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_DxAlta['state']="readonly"
				self.TopGeneral.destroy()

			elif self.personall=="DX":
				self.entry_CodDX['state']="normal"
				self.entry_CodDX.delete(0,'end')
				self.entry_CodDX.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_CodDX['state']="readonly"

				self.entry_DX.delete(0,'end')
				self.entry_DX.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[1])
				self.entry_DX['state']="readonly"	
				self.TopGeneral.destroy()

	def insert_DatosIngreso(self):

		fecha=self.FechaIngreso.get_date()
		horaIngreso="{}:{}".format(*self.time_Ingreso.time())
		peso=self.entry_PesoE.get()
		self.entry_MedicoResponsableIngreso.configure(state='normal')
		medico=self.entry_MedicoResponsableIngreso.get().strip()

		self.entry_EnfermeraResponsableIngreso.configure(state='normal')
		enfermera=self.entry_EnfermeraResponsableIngreso.get().strip()

		tecnicaenf=self.entry_TecnicoResponsableIngreso.get()

		self.entry_CodDX.configure(state='normal')
		codigoDX=self.entry_CodDX.get().strip()

		id_Ingreso=self.table_IngresosRecepcionados.item(self.table_IngresosRecepcionados.selection()[0],option='values')[5]

		nro=self.obj_ConsultaNeo.InsertarDatosIngreso(fecha,horaIngreso,peso,medico,enfermera,tecnicaenf,self.usuario,codigoDX,id_Ingreso)
		if nro:
			self.obj_ConsultaNeo.update_Tabla('INGRESO','ESTADOI',1,'ID_INGRESO',id_Ingreso)
			messagebox.showinfo('Notificación','Ser inserto correctamente')
			self.llenar_Tabla()
			self.llenar_TablaAlta()
			self.TopIngreso.destroy()

	def Top_DatosAlta(self):		
		self.idIngresoA=self.table_PacientesAlta.item(self.table_PacientesAlta.selection()[0],option='values')[5]
		self.idDatos_INGRESO=self.table_PacientesAlta.item(self.table_PacientesAlta.selection()[0],option='values')[6]
		self.TopEgreso=Toplevel()
		self.TopEgreso.title("Datos de Ingreso")
		self.TopEgreso.iconbitmap('img/alta.ico')
		self.TopEgreso.geometry("500x380")
		self.TopEgreso.grab_set()
		
		label=Label(self.TopEgreso,text="Fecha")
		label.grid(row=1,column=1,pady=10)
		self.FechaAlta=DateEntry(self.TopEgreso,selectmode='day',date_pattern='yyyy-MM-dd')
		self.FechaAlta.grid(row=1,column=2,pady=10)

		label=Label(self.TopEgreso,text="Hora")
		label.grid(row=1,column=3,pady=10,padx=10)
		self.time_Egreso=SpinTimePickerModern(self.TopEgreso)
		self.time_Egreso.addAll(constants.HOURS24)
		self.time_Egreso.setMins(str(self.timeDate).split(":")[1])
		self.time_Egreso.set24Hrs(str(self.timeDate).split(":")[0])
		self.time_Egreso.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
		self.time_Egreso.configure_separator(bg="#404040",fg="#fff")
		self.time_Egreso.grid(row=1,column=4,padx=10,pady=10)

		label=Label(self.TopEgreso,text="Peso")
		label.grid(row=2,column=1,pady=10)
		self.entry_PesoE=ttk.Spinbox(self.TopEgreso,from_=100,to=4000,increment=0.1)
		self.entry_PesoE.grid(row=2,column=2,pady=10)

		label=Label(self.TopEgreso,text="Medico Resp")
		label.grid(row=2,column=3,pady=10)
		self.entry_MedicoResponsableEgreso=ttk.Entry(self.TopEgreso)
		self.entry_MedicoResponsableEgreso.grid(row=2,column=4,pady=10)
		self.entry_MedicoResponsableEgreso.bind("<Return>",lambda event:self.Search_Personal(event,"MEDICOA"))

		label=Label(self.TopEgreso,text="Enf. Resp")
		label.grid(row=3,column=1,pady=10)
		self.entry_EnfermeraResponsableEgreso=ttk.Entry(self.TopEgreso)
		self.entry_EnfermeraResponsableEgreso.grid(row=3,column=2,pady=10)
		self.entry_EnfermeraResponsableEgreso.bind("<Return>",lambda event:self.Search_Personal(event,"ENFERMERAA"))

		label=Label(self.TopEgreso,text="Tecnico Resp")
		label.grid(row=3,column=3,pady=10)
		self.entry_TecnicoResponsableEgreso=ttk.Entry(self.TopEgreso)
		self.entry_TecnicoResponsableEgreso.grid(row=3,column=4,pady=10)

		label=Label(self.TopEgreso,text="Dias Hospi.")
		label.grid(row=4,column=1,pady=10)
		self.entry_DiasHospitalizado=ttk.Entry(self.TopEgreso)
		self.entry_DiasHospitalizado.grid(row=4,column=2,pady=10)
		self.entry_DiasHospitalizado.bind("<Button-1>",self.event_days)

		label=Label(self.TopEgreso,text="Destino.")
		label.grid(row=4,column=3,pady=10)
		self.ComboDestinoAlta=ttk.Combobox(self.TopEgreso)
		self.ComboDestinoAlta.grid(row=4,column=4,pady=10)
		self.llenar_ComboAlta()

		label=Label(self.TopEgreso,text="Dx Alta.")
		label.grid(row=5,column=1,pady=10)
		self.entry_DxAlta=ttk.Entry(self.TopEgreso)
		self.entry_DxAlta.grid(row=5,column=2,pady=10)
		self.entry_DxAlta.bind("<Return>",lambda event:self.Search_Personal(event,"DXA"))

		label=Label(self.TopEgreso,text="Observacion")
		label.grid(row=5,column=3,pady=10)
		self.entry_Observacion=Text(self.TopEgreso,width=20,height=3)
		self.entry_Observacion.grid(row=5,column=4,pady=10)

		

		buttonAdd=ttk.Button(self.TopEgreso,text="Aceptar")
		buttonAdd.grid(row=7,column=2,columnspan=2,pady=10)
		buttonAdd['command']=self.insert_Alta
	def llenar_ComboAlta(self):
		rows=self.obj_ConsultaNeo.get_Destinos()
		datos=[]
		for val in rows:
			datos.append(str(val.ID_DESTINO)+"-"+val.NOMBRE_DESTINO)
		if len(datos):
			self.ComboDestinoAlta['values']=datos
			self.ComboDestinoAlta.current(0)

	def event_days(self,event):
		
		fecha_alta=str(self.FechaAlta.get_date()).split("-")
		rows=self.obj_ConsultaNeo.get_FechaIngresoPaciente(self.idIngresoA)		
		fechaI=rows[0].FECHA.split("-")				
		fechaAlta=date(int(fecha_alta[0]),int(fecha_alta[1]),int(fecha_alta[2]))
		FechaIngreso=date(int(fechaI[0]),int(fechaI[1]),int(fechaI[2]))
		
		resultado=fechaAlta-FechaIngreso
		self.entry_DiasHospitalizado.delete(0,'end')
		self.entry_DiasHospitalizado.insert('end',resultado.days)

	def insert_Alta(self):
		peso=self.entry_PesoE.get().strip()
		fechaA=self.FechaAlta.get_date()
		self.entry_MedicoResponsableEgreso.configure(state='normal')
		medico=self.entry_MedicoResponsableEgreso.get().strip()
		self.entry_EnfermeraResponsableEgreso.configure(state='normal')
		enfermera=self.entry_EnfermeraResponsableEgreso.get().strip()
		tecEnfermera=self.entry_TecnicoResponsableEgreso.get().strip()
		diasH=self.entry_DiasHospitalizado.get().strip()
		observacion=self.entry_Observacion.get(1.0,'end-1c')
		destino=self.ComboDestinoAlta.get()[:self.ComboDestinoAlta.get().find("-")]
		self.entry_DxAlta.configure(state='normal')
		diagnostico=self.entry_DxAlta.get()
		horaEgreso="{}:{}".format(*self.time_Egreso.time())		

		if not self.ComboDestinoAlta.get()[self.ComboDestinoAlta.get().find("-")+1:]=="SU CASA":
			nro=self.obj_ConsultaNeo.InsertarDatosAlta(peso,fechaA,medico,enfermera,tecEnfermera,diasH,observacion,self.usuario,destino,diagnostico,self.idIngresoA,horaEgreso)
			if nro:
				self.obj_ConsultaNeo.update_Tabla('INGRESO','ESTADOA',1,'ID_INGRESO',self.idIngresoA)
				self.llenar_TablaAlta()
				self.obj_ConsultaNeo.InsertarINGRESO(self.idDatos_INGRESO,destino)
				messagebox.showinfo('Alerta','Successful')
				self.TopEgreso.destroy()
			
		else:
			nro=self.obj_ConsultaNeo.InsertarDatosAlta(peso,fechaA,medico,enfermera,tecEnfermera,diasH,observacion,self.usuario,destino,diagnostico,self.idIngresoA,horaEgreso)
			if nro:
				self.obj_ConsultaNeo.update_Tabla('INGRESO','ESTADOA',1,'ID_INGRESO',self.idIngresoA)
				self.llenar_TablaAlta()
				messagebox.showinfo('Alerta','Successful')
				self.TopEgreso.destroy()





		