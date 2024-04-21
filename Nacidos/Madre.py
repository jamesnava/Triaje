
from tkinter import *
from tkinter import ttk,messagebox
from Consulta_Galen import queryGalen
from Nacidos.consultaN import Consulta
from tktimepicker import SpinTimePickerModern, SpinTimePickerOld
from tktimepicker import constants
from Consulta_Triaje import queryTriaje
from tkcalendar import DateEntry
from datetime import datetime
from Util import util

class MadreN(object):

	def __init__(self,frame,width,height):		
		self.obj_consultaN=Consulta()
		self.obj_ConsultaTriaje=queryTriaje()
		self.frameMadre=frame
		self.width=width
		self.height=height

		self.timeDate=datetime.now().strftime("%H:%M:%S")			
		self.btnHistorialphoto=PhotoImage(file ="img/flecha.png")
	def Frame_Madre(self,iduser):
		self.iduser=iduser
		style=ttk.Style()
		style.theme_use("alt")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','#146AAE')])

		frameM=Frame(self.frameMadre,width=self.width,height=self.height,bg="#828682")
		frameM.place(x=0,y=0)
		frameM.pack_propagate(False)
		letra_leyenda=('Candara',16,'bold italic')
		

		button=ttk.Button(frameM,text="Insertar")
		button.grid(row=1,column=2,pady=10,padx=10)
		button.configure(command=self.Top_InsertarMadre)
		
		buttonHistorial=Label(frameM,image=self.btnHistorialphoto,cursor='hand2',bg='#828682')
		buttonHistorial.bind("<Button-1>",self.HistorialAIRN)
		buttonHistorial.grid(row=1,column=3,pady=10,padx=10)
		
		self.table_Madres=ttk.Treeview(frameM,columns=('#1','#2','#3','#4','#5'),show='headings')
		self.table_Madres.heading("#1",text="Item")
		self.table_Madres.column("#1",width=30,anchor="w",stretch='NO')
		self.table_Madres.heading("#2",text="DNI")
		self.table_Madres.column("#2",width=100,anchor="w",stretch='NO')
		self.table_Madres.heading("#3",text="NOMBRES")
		self.table_Madres.column("#3",width=500,anchor="w",stretch='NO')
		self.table_Madres.heading("#4",text="Estado Parto")
		self.table_Madres.column("#4",width=200,anchor="w",stretch='NO')
		self.table_Madres.heading("#5",text="Estado Nacimiento")
		self.table_Madres.column("#5",width=200,anchor="w",stretch='NO')					
		self.table_Madres.grid(row=3,column=2,padx=10,pady=2,columnspan=20)
		self.table_Madres.bind('<<TreeviewSelect>>',self.Selection_Table)
		self.llenar_TMadre()
		#self.table_editar.bind("<Double-Button-1>",self.top_EditarCie) 
		
		self.buttonPARTO=ttk.Button(frameM,text="Insertar PARTO",cursor="hand2")
		self.buttonPARTO.grid(row=6,column=6,pady=5)
		self.buttonPARTO["command"]=self.TopParto

		self.buttonAIRN=ttk.Button(frameM,text="Insertar AIRN",cursor="hand2")
		self.buttonAIRN.grid(row=6,column=8,pady=5)
		self.buttonAIRN['command']=self.insert_TOPAIRN

		
		Eliminar=ttk.Button(frameM,text="Eliminar",cursor="hand2")
		Eliminar["command"]=self.eliminarMadre
		Eliminar.grid(row=6,column=10,pady=5)

		label=Label(frameM,text="REGISTRO POR INGRESAR RESPONSABLES DE ATENCION",bg="#828682",font=('Candara',16,'bold italic'),fg="#000")
		label.grid(row=7,column=1,columnspan=20,pady=20,padx=10)

		#tabla airn
		self.table_Airn=ttk.Treeview(frameM,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_Airn.heading("#1",text="ITEM")
		self.table_Airn.column("#1",width=30,anchor="w",stretch='NO')
		self.table_Airn.heading("#2",text="DATOS MADRE")
		self.table_Airn.column("#2",width=300,anchor="w",stretch='NO')
		self.table_Airn.heading("#3",text="DATOS NACIDO")
		self.table_Airn.column("#3",width=300,anchor="w",stretch='NO')
		self.table_Airn.heading("#4",text="CNV")
		self.table_Airn.column("#4",width=200,anchor="w",stretch='NO')
		self.table_Airn.heading("#5",text="HCL NACIDO")
		self.table_Airn.column("#5",width=200,anchor="w",stretch='NO')
		self.table_Airn.heading("#6",text="AIR")
		self.table_Airn.column("#6",width=0,anchor="w",stretch='NO')						
		self.table_Airn.grid(row=8,column=2,padx=10,pady=2,columnspan=20)

		self.llenar_MadreNacido()
		self.table_Airn.bind("<Double-1>",self.Top_ResponsableAtencion)

		
		Eliminar=ttk.Button(frameM,text="Eliminar",cursor="hand2")
		#Eliminar["command"]=self.eliminarMadre
		Eliminar.grid(row=9,column=8,pady=5)

		#self.table_Airn.bind('<<TreeviewSelect>>',self.Selection_Table)
	def eliminarMadre(self):
		if self.table_Madres.selection():
			valor=self.table_Madres.item(self.table_Madres.selection()[0],option="value")[0]
			if self.obj_consultaN.deleteMadre(valor):
				messagebox.showinfo("Alerta","Se eliminó correctamente!")
				self.llenar_TMadre()
			else:
				messagebox.showerror("Error","No pudo Eliminarse")
		else:
			messagebox.showerror("Alerta","Seleccione un Item")
	def Top_InsertarMadre(self):
		self.TopMadre=Toplevel()
		self.TopMadre.title("Ingresar Datos")
		self.TopMadre.geometry("750x250")
		self.TopMadre.resizable(0,0)
		self.TopMadre.title("Insertar Datos")
		self.TopMadre.grab_set()

		label=Label(self.TopMadre,text="Dni")
		label.grid(row=2,column=1,pady=5)
		self.Dni_Madre=ttk.Entry(self.TopMadre)
		self.Dni_Madre.grid(row=2,column=2,pady=5)
		self.Dni_Madre.bind("<Return>",self.eventSearchMadre)

		label=Label(self.TopMadre,text="Datos P.")
		label.grid(row=2,column=3,padx=5,pady=5)
		self.NombreApellido=ttk.Entry(self.TopMadre,width=50)
		self.NombreApellido.grid(row=2,column=4,pady=5,columnspan=7)
		self.NombreApellido["state"]="readonly"

		label=Label(self.TopMadre,text="Grupo Factor")
		label.grid(row=3,column=1,pady=5)
		self.GrupoF=ttk.Entry(self.TopMadre)
		self.GrupoF.grid(row=3,column=2,pady=5)

		label=Label(self.TopMadre,text="RPM")
		label.grid(row=3,column=3,padx=5,pady=5)
		self.RPM=ttk.Entry(self.TopMadre)
		self.RPM.grid(row=3,column=4,pady=5)
		self.RPM.bind("<KeyRelease>",lambda event:self.EntryRPMValidar(event,self.RPM))
		self.checkIntegra=BooleanVar()
		check=ttk.Checkbutton(self.TopMadre,text="Íntegra",variable=self.checkIntegra)
		check.grid(row=3,column=5,pady=5)
		check.configure(command=self.validaRPM)

		label=Label(self.TopMadre,text="HTA")
		label.grid(row=3,column=6,padx=5,pady=5)
		self.HTA=ttk.Combobox(self.TopMadre,values=['SI','NO'])
		self.HTA.grid(row=3,column=7,pady=5)
		self.HTA.current(0)

		label=Label(self.TopMadre,text="ITU3_TRIMESTRE")
		label.grid(row=4,column=1,pady=5)
		self.ITU3=ttk.Combobox(self.TopMadre,values=['SI','NO'])
		self.ITU3.grid(row=4,column=2,pady=5)
		self.ITU3.current(0)

		label=Label(self.TopMadre,text="DOSIS ITU")
		label.grid(row=4,column=3,padx=5,pady=5)
		self.DITU=ttk.Entry(self.TopMadre)
		self.DITU.grid(row=4,column=4,pady=5)

		label=Label(self.TopMadre,text="CPN")
		label.grid(row=4,column=6,padx=5,pady=5)
		self.cpn=ttk.Entry(self.TopMadre)
		self.cpn.grid(row=4,column=7,pady=5)

		label=Label(self.TopMadre,text="Observacion")
		label.grid(row=5,column=1,pady=5)
		self.observacionM=ttk.Entry(self.TopMadre,width=50)
		self.observacionM.grid(row=5,column=2,pady=5,columnspan=4)

		buttonAdd=ttk.Button(self.TopMadre,text="Agregar")
		buttonAdd.grid(row=6,column=3,pady=5)
		buttonAdd["command"]=self.insertMadre

		buttonAdd=ttk.Button(self.TopMadre,text="Cancelar")
		buttonAdd.grid(row=6,column=5,pady=5)

	def validaRPM(self):
		if self.checkIntegra.get():
			self.RPM.configure(state='disabled')
		else:
			self.RPM.configure(state='normal')
			self.RPM.delete(0,"end")
			
	def EntryRPMValidar(self,event,entry):
		param=""
		param=param+entry.get()
		
		if len(param)==2:				
			entry.insert("end",":")

		if len(param)>5:
			entry.delete(6,"end")
			if not (param[:2].isdigit() and param[3:].isdigit()):
				messagebox.showerror('Alerta',"Solo se Acepta Valores Numericos")
				entry.delete(0,'end')


	def eventSearchMadre(self,event):
		dni=self.Dni_Madre.get()
		obj_Paciente=queryGalen()
		row=obj_Paciente.query_Paciente(dni)
		self.NombreApellido['state']='normal'
		self.NombreApellido.delete(0,"end")
		if len(row):
			self.NombreApellido.insert("end",row[0].PrimerNombre+" "+row[0].ApellidoPaterno+" "+row[0].ApellidoMaterno)

	def insertMadre(self):
		dni=self.Dni_Madre.get()
		grupo=self.GrupoF.get()
		rpm=None
		if self.checkIntegra.get():
			rpm="INTEGRA"
		else:
			rpm=self.RPM.get()
		
		hta=self.HTA.get()
		itu3=self.ITU3.get()
		ditu=self.DITU.get()
		datose=self.NombreApellido.get()
		cpn=self.cpn.get()
		observacion=self.observacionM.get()

		if self.NombreApellido.get():
			nro=self.obj_consultaN.insertarMadre(dni,grupo,rpm,hta,itu3,ditu,cpn,observacion)

			if nro:
				messagebox.showinfo("Alerta","Se insertó correctamente!!")
				self.TopMadre.destroy()
				self.llenar_TMadre()

			else:
				messagebox.showerror("Alerta","No se pudo insertar!!")
		else:
			messagebox.showerror("Error!!","Ingrese el DNI y presiona ENTER!!")

	def llenar_MadreNacido(self):
		self.borrarTabla(self.table_Airn)
		rows=self.obj_consultaN.consulta_TablaALL()
		obj_Paciente=queryGalen()
		for val in rows:
			rowGMadre=obj_Paciente.query_Paciente(val.MADRE)
			rowGNacido=obj_Paciente.query_PacienteXHCL(val.NACIDO)				
			self.table_Airn.insert("","end",values=(val.IDMADRE,rowGMadre[0].PrimerNombre+" "+rowGMadre[0].ApellidoPaterno+" "+rowGMadre[0].ApellidoMaterno,rowGNacido[0].PrimerNombre+" "+rowGNacido[0].ApellidoPaterno+" "+rowGNacido[0].ApellidoMaterno,val.CNV,val.HCL,val.Id_AIR))
	

	def llenar_TMadre(self):
		self.borrarTabla(self.table_Madres)
		rows=self.obj_consultaN.consulta_Tabla('MADRE','estadoAIRN','estadoPARTO',0,0)
		obj_Paciente=queryGalen()
		for val in rows:
			rowG=obj_Paciente.query_Paciente(val.DNI)
			airnE="No Registrado" if val.estadoAIRN==0 else "Registrado"
			partoE="No Registrado" if val.estadoPARTO==0 else "Registrado"			
			self.table_Madres.insert("","end",values=(val.IDMADRE,val.DNI,rowG[0].PrimerNombre+" "+rowG[0].ApellidoPaterno+" "+rowG[0].ApellidoMaterno,partoE,airnE))

	def Selection_Table(self,event):
		if self.table_Madres.selection():
			partoValor=self.table_Madres.item(self.table_Madres.selection()[0])['values'][3]
			nacimiento=self.table_Madres.item(self.table_Madres.selection()[0])['values'][4]
			if partoValor=='Registrado':
				self.buttonPARTO['state']='disabled'
			else:
				self.buttonPARTO['state']='normal'

			if nacimiento=='Registrado':
				self.buttonAIRN['state']='disabled'
			else:
				self.buttonAIRN['state']='normal'

	def borrarTabla(self,tabla):		
		for item in tabla.get_children():
			tabla.delete(item)

	def TopParto(self):
		if self.table_Madres.selection():
			self.id_madre=self.table_Madres.item(self.table_Madres.selection()[0])['values'][0]
			self.WindowsParto=Toplevel()
			self.WindowsParto.title("Ingresar datos del Parto")
			self.WindowsParto.geometry("700x300")
			self.WindowsParto.resizable(0,0)
			self.WindowsParto.grab_set()

			label=Label(self.WindowsParto,text="DATOS DE INGRESO DEL PARTO",font=('Arial',13,'bold'))
			label.grid(row=0,column=0,columnspan=4,padx=10)

			label=Label(self.WindowsParto,text="Hora I. SO",font=('Arial',10,'bold'))
			label.grid(row=1,column=0,pady=10)
			self.time_Ingreso=SpinTimePickerModern(self.WindowsParto)
			self.time_Ingreso.addAll(constants.HOURS24)			
			self.time_Ingreso.setMins(str(self.timeDate).split(":")[1])
			self.time_Ingreso.set24Hrs(str(self.timeDate).split(":")[0])
			self.time_Ingreso.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
			self.time_Ingreso.configure_separator(bg="#404040",fg="#fff")
			self.time_Ingreso.grid(row=1,column=1,padx=10,pady=10)
			

			label=Label(self.WindowsParto,text="Hora Nacimiento",font=('Arial',10,'bold'))
			label.grid(row=1,column=3,pady=10)
			self.time_Egreso=SpinTimePickerModern(self.WindowsParto)
			self.time_Egreso.addAll(constants.HOURS24)
			self.time_Egreso.setMins(str(self.timeDate).split(":")[1])
			self.time_Egreso.set24Hrs(str(self.timeDate).split(":")[0])
			self.time_Egreso.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
			self.time_Egreso.configure_separator(bg="#404040",fg="#fff")
			self.time_Egreso.grid(row=1,column=4,padx=10,pady=10)
			

			self.checkIngresoSala=BooleanVar()
			check=Checkbutton(self.WindowsParto,text="",variable=self.checkIngresoSala,font=("Times", 16))
			check.grid(row=1,column=5)
			check.configure(command=self.EventoCheckValidacionFecha)

			self.labelNotificacion=Label(self.WindowsParto,text="Sala de Operaciones",fg="green")
			self.labelNotificacion.grid(row=1,column=6)


			label=Label(self.WindowsParto,text="H.I.S. PARTOS",font=('Arial',10,'bold'))
			label.grid(row=2,column=0,pady=10)
			self.time_IPartos=SpinTimePickerModern(self.WindowsParto)
			self.time_IPartos.addAll(constants.HOURS24)
			self.time_IPartos.setMins(str(self.timeDate).split(":")[1])
			self.time_IPartos.set24Hrs(str(self.timeDate).split(":")[0])
			self.time_IPartos.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
			self.time_IPartos.configure_separator(bg="#404040",fg="#fff")
			self.time_IPartos.grid(row=2,column=1,padx=10,pady=10)

			label=Label(self.WindowsParto,text="Tipo Parto: ",font=('Arial',10,'bold'))
			label.grid(row=2,column=3,pady=10)
			self.combo_tipoP=ttk.Combobox(self.WindowsParto,values=['EUTOCICO','FORCEPS','CESARIA ELECTIVA','CESARIA EMERGENCIA','PODALICO'],state='readonly')
			self.combo_tipoP.grid(row=2,column=4,pady=10)
			self.combo_tipoP.current(0)

			label=Label(self.WindowsParto,text="EE.SS ORIGEN: ",font=('Arial',10,'bold'))
			label.grid(row=3,column=0,pady=10)
			self.entry_Procedencia=ttk.Entry(self.WindowsParto,width=40)
			self.entry_Procedencia.grid(row=3,column=1,columnspan=3)

			label=Label(self.WindowsParto,text="Motivo Cesaria",font=('Arial',10,'bold'))
			label.grid(row=3,column=4,pady=10)
			self.entry_Cesaria=ttk.Entry(self.WindowsParto,width=30)
			self.entry_Cesaria.grid(row=3,column=5,columnspan=2)


			button_Add=ttk.Button(self.WindowsParto,text="Guardar")
			button_Add.grid(row=4,column=1,pady=10)
			button_Add['command']=self.insertParto

			button_Cancel=ttk.Button(self.WindowsParto,text="Cancelar")
			button_Cancel.grid(row=4,column=3,pady=10)
			button_Cancel["command"]=self.WindowsParto.destroy
		else:
			messagebox.showinfo("Alerta!","Seleccione un Item!!")

	def EventoCheckValidacionFecha(self):
		if self.checkIngresoSala.get():
			self.labelNotificacion.configure(text="Sala de partos",fg="red")
			self.entry_Cesaria.configure(state="disabled")
		else:
			self.labelNotificacion.configure(text="Sala de Operaciones",fg="green")
			self.entry_Cesaria.configure(state="normal")


	def insertParto(self):		
		procedencia=self.entry_Procedencia.get()
		tipoP=self.combo_tipoP.get()
		cesaria=""

		if self.checkIngresoSala.get():
			horaISO="NO"
			#horaESO="NO"			
			horaIPartos="{}:{}".format(*self.time_IPartos.time())
		else:
			horaISO="{}:{}".format(*self.time_Ingreso.time())
			
			cesaria=self.entry_Cesaria.get()
			horaIPartos="NO"

		HoraNaciemiento="{}:{}".format(*self.time_Egreso.time())
		##insertar....
		#print(procedencia,self.id_madre,horaISO,horaESO,horaIPartos,tipoP)

		numero=self.obj_consultaN.insertParto(procedencia,self.id_madre,horaISO,HoraNaciemiento,horaIPartos,tipoP,cesaria)
		
		if numero:
			self.obj_consultaN.Update_Tabla('MADRE','estadoPARTO',1,'IDMADRE',self.id_madre)
			messagebox.showinfo("Alerta!!","Se insertó correctamente!")
			self.WindowsParto.destroy()
			self.llenar_TMadre()
			self.llenar_MadreNacido()
		else:
			messagebox.showerror("Alerta","No se pudo Insertar")

	def Top_ResponsableAtencion(self,event):
		self.idA=self.table_Airn.item(self.table_Airn.selection()[0])['values'][5]
		self.Atencion_Windows=Toplevel()
		self.Atencion_Windows.title("Ingresar Responsables")
		self.Atencion_Windows.geometry("600x300")
		self.Atencion_Windows.grab_set()
		
		label=Label(self.Atencion_Windows,text="Resp. Medico: ",font=('Arial',10,'bold'))
		label.grid(row=1,column=1,pady=10)
		self.Entry_Medico=ttk.Entry(self.Atencion_Windows,state='readonly')
		self.Entry_Medico.grid(row=1,column=2,pady=10)
		self.Entry_Medico.bind("<Return>",lambda event:self.Search_Personal(event,"DOCTOR"))

		label=Label(self.Atencion_Windows,text="Resp. Obstetra: ",font=('Arial',10,'bold'))
		label.grid(row=1,column=3,pady=10,padx=10)
		self.Entry_Obstetra=ttk.Entry(self.Atencion_Windows,state='readonly')
		self.Entry_Obstetra.grid(row=1,column=4,pady=10)
		self.Entry_Obstetra.bind("<Return>",lambda event:self.Search_Personal(event,"OBSTETRA"))

		label=Label(self.Atencion_Windows,text="Resp. Enfermera: ",font=('Arial',10,'bold'))
		label.grid(row=2,column=1,pady=10)
		self.Entry_Enfermera=ttk.Entry(self.Atencion_Windows,state="readonly")
		self.Entry_Enfermera.grid(row=2,column=2,pady=10)
		self.Entry_Enfermera.bind("<Return>",lambda event:self.Search_Personal(event,"ENFERMERA"))

		label=Label(self.Atencion_Windows,text="Tec. Enfermera: ",font=('Arial',10,'bold'))
		label.grid(row=2,column=3,pady=10,padx=10)
		self.Entry_TecEnfermera=ttk.Entry(self.Atencion_Windows)
		self.Entry_TecEnfermera.grid(row=2,column=4,pady=10)

		AddButton=ttk.Button(self.Atencion_Windows,text="Agregar")
		AddButton.grid(row=3,column=2,pady=10)
		AddButton.configure(command=self.Insert_ResponsableAtencion)


		CloseButton=ttk.Button(self.Atencion_Windows,text="Cerrar")
		CloseButton.grid(row=3,column=4,pady=10)
		CloseButton.configure(command=self.Atencion_Windows.destroy)
	
	def Insert_ResponsableAtencion(self):
		self.Entry_Medico['state']='normal'
		medico=self.Entry_Medico.get().strip() if len(self.Entry_Medico.get()) else None
		self.Entry_Obstetra['state']='normal'
		obstetra=self.Entry_Obstetra.get().strip()
		self.Entry_Enfermera['state']='normal'
		enfermera=self.Entry_Enfermera.get().strip()
		tecnicaE=self.Entry_TecEnfermera.get().strip()

		datos=[enfermera,medico,obstetra]
		
		if len(datos)==3:			
			nro=self.obj_consultaN.Insert_RESATENCION(datos,tecnicaE,self.idA)
			if nro:
				self.obj_consultaN.Update_Tabla('AIR','estado',1,'Id_AIR',self.idA)
				messagebox.showinfo('Alerta','Se insertó correctamente!!')
				self.Atencion_Windows.destroy()
				self.llenar_MadreNacido()
			else:
				messagebox.showerror('Alerta','No pudo Insertarse')
				self.Atencion_Windows.destroy()
		else:
			messagebox.showerror('Alerta','Llene los campos Obligatorios')
	

	def Search_Personal(self,event,identificador):
		self.personall=None
		if identificador=="DOCTOR":
			self.personall="DOCTOR"
			self.Top_searchPersonal()
		elif identificador=="OBSTETRA":
			self.personall="OBSTETRA"
			self.Top_searchPersonal()
		elif identificador=="ENFERMERA":
			self.personall="ENFERMERA"
			self.Top_searchPersonal()
		elif identificador=="MEDICOA":
			self.personall="MEDICOA"
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
		self.table_General.heading("#1",text="DNI")
		self.table_General.column("#1",width=100,anchor="center")
		self.table_General.heading("#2",text="Nombres")
		self.table_General.column("#2",width=400,anchor="center")										
		self.table_General.place(x=10,y=70)
		self.table_General.bind('<<TreeviewSelect>>',self.itemTable_selected)			
		#botones de accion
		self.btn_TPG_Close=ttk.Button(self.TopGeneral,text='Cerrar')
		self.btn_TPG_Close.place(x=280,y=365)
		self.btn_TPG_Close['command']=lambda :self.TopGeneral.destroy()


	def buscar_DatosPersonales(self,event):
		obj_Galen=queryGalen()
		parametro=''
		self.borrarTabla(self.table_General)
		if len(self.Entry_buscar_General.get())!=0:
			parametro=parametro+self.Entry_buscar_General.get()
			rows=obj_Galen.query_Empleado(parametro)
			for valores in rows:
				self.table_General.insert('','end',values=(valores.DNI,valores.Nombres+" "+valores.ApellidoPaterno+" "+valores.ApellidoMaterno))

	def itemTable_selected(self,event):
		if len(self.table_General.focus())!=0:
			if self.personall=="DOCTOR":				
				self.Entry_Medico['state']="normal"
				self.Entry_Medico.delete(0,'end')
				self.Entry_Medico.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.Entry_Medico['state']="readonly"	
				self.TopGeneral.destroy()

			elif self.personall=="OBSTETRA":
				self.Entry_Obstetra['state']="normal"
				self.Entry_Obstetra.delete(0,'end')
				self.Entry_Obstetra.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.Entry_Obstetra['state']="readonly"	
				self.TopGeneral.destroy()

			elif self.personall=="MEDICOA":
				self.AEntry_MedicoA['state']="normal"
				self.AEntry_MedicoA.delete(0,'end')
				self.AEntry_MedicoA.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.AEntry_MedicoA['state']="readonly"	
				self.TopGeneral.destroy()
			else:
				self.Entry_Enfermera['state']="normal"
				self.Entry_Enfermera.delete(0,'end')
				self.Entry_Enfermera.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.Entry_Enfermera['state']="readonly"	
				self.TopGeneral.destroy()

	def insert_TOPAIRN(self):
		self.hcl=None		
		if self.table_Madres.selection():
			self.id_mad=self.table_Madres.item(self.table_Madres.selection()[0],option='values')[0]
			self.TopAIRN=Toplevel()
			self.TopAIRN.geometry("1400x700")
			self.TopAIRN.resizable(0,0)
			self.TopAIRN.title("Ingresar Datos")
			self.TopAIRN.configure(bg="#273C6A")
			self.TopAIRN.grab_set()

			label=Label(self.TopAIRN,text="HCL: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=1,column=1,pady=10)
			self.AEntry_HCL=ttk.Entry(self.TopAIRN,width=20)
			self.AEntry_HCL.grid(row=1,column=2,pady=10)
			#self.AEntry_HCL.configure(state='readonly')
			self.AEntry_HCL.bind("<Return>",self.searchAIRN)

			label=Label(self.TopAIRN,text="Datos: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=1,column=3,pady=10)
			self.AEntry_Datos=ttk.Entry(self.TopAIRN,state="readonly",width=50)
			self.AEntry_Datos.grid(row=1,column=4,columnspan=6,pady=10)

			label=Label(self.TopAIRN,text="CNV: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=2,column=1,pady=10)
			self.AEntry_CNV=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_CNV.grid(row=2,column=2,pady=10)

			label=Label(self.TopAIRN,text="Pinzam(min): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=2,column=3,pady=10)
			self.AEntry_PINZAMIENTO=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_PINZAMIENTO.grid(row=2,column=4,pady=10)
			self.AEntry_PINZAMIENTO.bind("<KeyRelease>",lambda event:self.validarDigit(event,self.AEntry_PINZAMIENTO))
			

			label=Label(self.TopAIRN,text="Cont. Precoz: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=2,column=5,pady=10)
			self.AEntry_CONTACTPRECOZ=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_CONTACTPRECOZ.grid(row=2,column=6,pady=10)

			self.checkContactoP=BooleanVar()
			check=Checkbutton(self.TopAIRN,text="APEGO",variable=self.checkContactoP,bg="#273C6A",fg="#fff")
			check.grid(row=2,column=7)
			check.configure(command=lambda :self.EventoCheck(self.checkContactoP,self.AEntry_CONTACTPRECOZ))

			label=Label(self.TopAIRN,text="LME(hh:mm): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=2,column=8,pady=10)
			self.AEntry_LME=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_LME.bind("<KeyRelease>",lambda event:self.EntryRPMValidar(event,self.AEntry_LME))
			self.AEntry_LME.grid(row=2,column=9,pady=10)

			label=Label(self.TopAIRN,text="PAPACANGURO.: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=2,column=10,pady=10)
			self.ACOMBO_PAPACANGURO=ttk.Combobox(self.TopAIRN,width=15,values=['SI','NO'],state="readonly")
			self.ACOMBO_PAPACANGURO.current(0)
			self.ACOMBO_PAPACANGURO.grid(row=2,column=11,pady=10)

			label=Label(self.TopAIRN,text="PESO(grs): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=3,column=1,pady=10)
			self.AEntry_PESO=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_PESO.grid(row=3,column=2,pady=10)
			self.AEntry_PESO.bind("<KeyRelease>",lambda event:self.validarDecimales(event,self.AEntry_PESO) )

			label=Label(self.TopAIRN,text="TALLA(cm): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=3,column=3,pady=10)
			self.AEntry_TALLA=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_TALLA.grid(row=3,column=4,pady=10)
			self.AEntry_TALLA.bind("<KeyRelease>",lambda event:self.validarDecimales(event,self.AEntry_TALLA) )

			label=Label(self.TopAIRN,text="PC : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=3,column=5,pady=10)
			self.AEntry_PC=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_PC.grid(row=3,column=6,pady=10)
			self.AEntry_PC.bind("<KeyRelease>",lambda event:self.validarDecimales(event,self.AEntry_PC) )

			label=Label(self.TopAIRN,text="PT : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=3,column=7,pady=10)
			self.AEntry_PT=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_PT.grid(row=3,column=8,pady=10)
			self.AEntry_PT.bind("<KeyRelease>",lambda event:self.validarDecimales(event,self.AEntry_PT) )

			label=Label(self.TopAIRN,text="PA : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=3,column=9,pady=10)
			self.AEntry_PA=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_PA.grid(row=3,column=10,pady=10)
			self.AEntry_PA.bind("<KeyRelease>",lambda event:self.validarDecimales(event,self.AEntry_PA) )

			label=Label(self.TopAIRN,text="PB: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=4,column=1,pady=10)
			self.AEntry_PB=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_PB.grid(row=4,column=2,pady=10)
			self.AEntry_PB.bind("<KeyRelease>",lambda event:self.validarDecimales(event,self.AEntry_PB))

			label=Label(self.TopAIRN,text="EXFI: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=4,column=3,pady=10)
			self.AEntry_EXFI=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_EXFI.grid(row=4,column=4,pady=10)
			self.AEntry_EXFI.bind("<KeyRelease>",lambda event:self.validarDigit(event,self.AEntry_EXFI))


			label=Label(self.TopAIRN,text="FUR: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=4,column=5,pady=10)
			self.AEntry_FUR=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_FUR.grid(row=4,column=6,pady=10)
			self.AEntry_FUR.bind("<KeyRelease>",lambda event:self.validarDigit(event,self.AEntry_FUR))

			label=Label(self.TopAIRN,text="APGAR 1 : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=4,column=7,pady=10)
			self.AEntry_APGAR1=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_APGAR1.grid(row=4,column=8,pady=10)
			self.AEntry_APGAR1.bind("<KeyRelease>",lambda event:self.validarDigit(event,self.AEntry_APGAR1))

			label=Label(self.TopAIRN,text="APGAR 5 : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=4,column=9,pady=10)
			self.AEntry_APGAR5=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_APGAR5.grid(row=4,column=10,pady=10)
			self.AEntry_APGAR5.bind("<KeyRelease>",lambda event:self.validarDigit(event,self.AEntry_APGAR5))

			label=Label(self.TopAIRN,text="APGAR 10: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=5,column=1,pady=10)
			self.AEntry_APGAR10=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_APGAR10.grid(row=5,column=2,pady=10)
			self.AEntry_APGAR10.bind("<KeyRelease>",lambda event:self.validarDigit(event,self.AEntry_APGAR10))

			label=Label(self.TopAIRN,text="TEMPERATURA: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=5,column=3,pady=10)
			self.AEntry_TEMPERATURA=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_TEMPERATURA.grid(row=5,column=4,pady=10)
			self.AEntry_TEMPERATURA.bind("<KeyRelease>",lambda event:self.validarDecimales(event,self.AEntry_TEMPERATURA) )
		

			label=Label(self.TopAIRN,text="PROF. OCULAR: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=5,column=5,pady=10)
			self.ACOMBO_OCULAR=ttk.Combobox(self.TopAIRN,width=15,values=['SI','NO'],state="readonly")
			self.ACOMBO_OCULAR.current(0)
			self.ACOMBO_OCULAR.grid(row=5,column=6,pady=10)

			label=Label(self.TopAIRN,text="VIT.K: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=5,column=7,pady=10)
			self.ACOMBO_VIT=ttk.Combobox(self.TopAIRN,width=15,values=['SI','NO'],state="readonly")
			self.ACOMBO_VIT.current(0)
			self.ACOMBO_VIT.grid(row=5,column=8,pady=10)

			label=Label(self.TopAIRN,text="Clasif. NUTRICIONAL:",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=5,column=9,pady=10)
			self.ACOMBO_NUTRICIONAL=ttk.Combobox(self.TopAIRN,width=15,values=['AEG','PEG','GEG'],state="readonly")
			self.ACOMBO_NUTRICIONAL.current(0)
			self.ACOMBO_NUTRICIONAL.grid(row=5,column=10,pady=10)

			label=Label(self.TopAIRN,text="ASFIXIA:",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=6,column=1,pady=10)
			self.ACOMBO_ASFIXIA=ttk.Combobox(self.TopAIRN,width=15,values=['NO','LEV','MOD','SEV'],state="readonly")
			self.ACOMBO_ASFIXIA.current(0)
			self.ACOMBO_ASFIXIA.grid(row=6,column=2,pady=10)

			label=Label(self.TopAIRN,text="COLOR AMNIOTICO: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=6,column=3,pady=10)
			self.AEntry_AMNIOTICO=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_AMNIOTICO.grid(row=6,column=4,pady=10)

			label=Label(self.TopAIRN,text="T. KRISTELLER(min): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=6,column=5,pady=10)
			self.AEntry_KRISTELLER=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_KRISTELLER.grid(row=6,column=6,pady=10)
			self.AEntry_KRISTELLER.bind("<KeyRelease>",lambda event:self.validarDigit(event,self.AEntry_KRISTELLER))
			self.AEntry_KRISTELLER.bind("<FocusIn>",lambda event:self.on_entry_click(event,self.AEntry_KRISTELLER))
			self.AEntry_KRISTELLER.bind("<FocusOut>",lambda event:self.leave_entry_click(event,self.AEntry_KRISTELLER))

			label=Label(self.TopAIRN,text="MECONIO: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=6,column=7,pady=10)
			self.ACOMBO_MECONICO=ttk.Combobox(self.TopAIRN,width=15,values=['SI','NO'],state="readonly")
			self.ACOMBO_MECONICO.current(0)
			self.ACOMBO_MECONICO.grid(row=6,column=8,pady=10)

			label=Label(self.TopAIRN,text="ORINA: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=6,column=9,pady=10)
			self.ACOMBO_ORINA=ttk.Combobox(self.TopAIRN,width=15,values=['SI','NO'],state="readonly")
			self.ACOMBO_ORINA.current(0)
			self.ACOMBO_ORINA.grid(row=6,column=10,pady=10)

			label=Label(self.TopAIRN,text="GRUPO FACTOR:",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=7,column=1,pady=10)
			self.AEntry_GRUPOF=ttk.Entry(self.TopAIRN,width=15)
			self.AEntry_GRUPOF.grid(row=7,column=2,pady=10)
			

			label=Label(self.TopAIRN,text="DESTINO RN:",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=7,column=3,pady=10)
			self.AEntry_DESTINORN=ttk.Entry(self.TopAIRN,width=20)
			self.AEntry_DESTINORN.grid(row=7,column=4,pady=10)
			#self.AEntry_DESTINORN.bind("<Return>",self.Top_searchServicios)

			label=Label(self.TopAIRN,text="OBSERVACION RN:",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=7,column=5,pady=10)
			self.AEntry_OBSERVACION=ttk.Entry(self.TopAIRN,width=25)
			self.AEntry_OBSERVACION.grid(row=7,column=6,pady=10,columnspan=2)			


			label=Label(self.TopAIRN,text="Hora E.AIRN",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=7,column=9,pady=10)
			self.time_EgresoAIRN=SpinTimePickerModern(self.TopAIRN)
			self.time_EgresoAIRN.addAll(constants.HOURS24)
			self.time_EgresoAIRN.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
			self.time_EgresoAIRN.configure_separator(bg="#404040",fg="#fff")
			self.time_EgresoAIRN.grid(row=7,column=10,pady=10)

			self.estadoInterconsulta=BooleanVar()
			checkInterconsulta=Checkbutton(self.TopAIRN,text="Interconsulta",bg="#273C6A",fg="#9DC2A7",font=('Arial',10,'bold'),variable=self.estadoInterconsulta)
			
			checkInterconsulta.grid(row=8,column=1)

			label=Label(self.TopAIRN,text="MED RESPONSABLE",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
			label.grid(row=8,column=2,pady=10)
			self.AEntry_MedicoInterconsulta=ttk.Entry(self.TopAIRN,state='disabled')
			self.AEntry_MedicoInterconsulta.grid(row=8,column=3,pady=10,columnspan=2)
			checkInterconsulta.configure(command=lambda:self.EventoCheckInter(self.estadoInterconsulta,self.AEntry_MedicoInterconsulta))

			self.estadoHospitalizado=BooleanVar()
			check=Checkbutton(self.TopAIRN,text="Hospitalizado",bg="#273C6A",fg="#9DC2A7",font=('Arial',10,'bold'),variable=self.estadoHospitalizado)
			check.configure(command=lambda:self.EventoCheckHospitalizados(self.estadoHospitalizado))
			check.grid(row=9,column=5)

			style = ttk.Style()
			style.configure("btnAdd.TButton",background="#9A4419",font=("Helvetica", 12))

			self.ButtonAddCIE=ttk.Button(self.TopAIRN,text="Agregar DX",style="btnAdd.TButton",cursor="hand2",state="disabled")
			self.ButtonAddCIE.grid(row=10,column=4,pady=10)
			self.ButtonAddCIE['command']=self.Top_searchCie
			
			style = ttk.Style()
			style.configure("btnClose.TButton",background="red",font=("Helvetica", 12))
			self.ButtonEliminaCIE=ttk.Button(self.TopAIRN,text="Quitar Dx",style="btnClose.TButton",cursor="hand2",state="disabled")
			self.ButtonEliminaCIE.grid(row=10,column=6,pady=10)
			self.ButtonEliminaCIE['command']=lambda :self.eliminarSeleccionTable(self.table_DX)

			self.table_DX=ttk.Treeview(self.TopAIRN,columns=('#1','#2'),show='headings',height=5)
			self.table_DX.heading("#1",text="CODIGO CIE")
			self.table_DX.column("#1",width=100,anchor="w",stretch='NO')
			self.table_DX.heading("#2",text="DESCRIPCION")
			self.table_DX.column("#2",width=400,anchor="w",stretch='NO')								
			self.table_DX.grid(row=11,column=1,padx=10,pady=2,columnspan=20)


			style = ttk.Style()
			style.configure("btnAcept.TButton",background="green",font=("Helvetica", 12))

			ButtonAddAIRN=ttk.Button(self.TopAIRN,text="Agregar",style="btnAcept.TButton",cursor="hand2")
			ButtonAddAIRN.grid(row=12,column=4,pady=10)
			ButtonAddAIRN['command']=self.insertAIRN

			style = ttk.Style()
			style.configure("btnClose.TButton",background="red",font=("Helvetica", 12))
			ButtonCloseAIRN=ttk.Button(self.TopAIRN,text="Cerrar",style="btnClose.TButton",cursor="hand2")
			ButtonCloseAIRN.grid(row=12,column=6,pady=10)
			ButtonCloseAIRN['command']=self.TopAIRN.destroy


		else:
			messagebox.showerror("Alerta","Seleccione un Item!")

	def EventoCheck(self,check,entry):
		if check.get():
			entry.configure(state="disabled")
		else:
			entry.configure(state="normal")

	def EventoCheckInter(self,check,entry):
		if check.get():
			entry.configure(state="normal")
		else:
			entry.configure(state="disabled")

	def EventoCheckHospitalizados(self,check):
		
		if check.get():			
			self.ButtonAddCIE.configure(state='normal')
			self.ButtonEliminaCIE.configure(state='normal')
		else:
			self.ButtonAddCIE.configure(state='disabled')
			self.ButtonEliminaCIE.configure(state='disabled')
	def validarDecimales(self,event,entry):
		param=""
		param=param+entry.get()

		if param.find(".")<len(param)-1:
			try:
				float(param)
				entry.delete(0,"end")
				entry.insert("end",param)
			except Exception as e:
				entry.delete(0,"end")
				messagebox.showerror("Alerta","Entrada Incorrecta!!")

	def validarDigit(self,event,entry):
		param=""
		param=param+entry.get()
		if not param.isdigit():
			messagebox.showerror("Alerta","Solo se Acepta valores numericos")
			entry.delete(0,"end")

	def searchAIRN(self,event):
		hc=self.AEntry_HCL.get()
		objGalen=queryGalen()
		rows=objGalen.query_PacienteXHCL(hc)
		if len(rows)>0:
			self.AEntry_Datos['state']='normal'
			self.AEntry_Datos.delete(0,'end')
			self.AEntry_Datos.insert('end',rows[0].PrimerNombre+" "+rows[0].ApellidoPaterno+" "+rows[0].ApellidoMaterno)
			self.hcl=rows[0].NroHistoriaClinica
			self.Fecha_NacimientoRN=rows[0].FechaNacimiento
		else:
			messagebox.showerror("Error","Datos no encontrados!!")
			self.AEntry_HCL.delete(0,'end')
	#placeholder personalizado
	def on_entry_click(self,event,entry):
		entry.delete(0,"end")
	def leave_entry_click(self,event,entry):
		if entry.get()=="":
			entry.insert(0,"en minutos")

	def Top_searchCie(self):
		self.TopCIE=Toplevel()
		self.TopCIE.title('Diagnosticos')
		self.TopCIE.geometry("720x400+350+50")
		#self.TopCIE.focus_set()	
		self.TopCIE.grab_set()
		self.TopCIE.resizable(0,0)	
		#self.TopCIE.iconbitmap('image/diagnostico.ico')

		label_title=Label(self.TopCIE,text='Buscar')
		label_title.place(x=20,y=20)
		self.Entry_buscar_General=ttk.Entry(self.TopCIE,width=30)
		self.Entry_buscar_General.focus()
		self.Entry_buscar_General.place(x=80,y=20)
		self.Entry_buscar_General.bind('<Key>',self.buscar_cie)		

		#tabla...
		self.table_CIE=ttk.Treeview(self.TopCIE,columns=('#1','#2'),show='headings')		
		self.table_CIE.heading("#1",text="CODIGO")
		self.table_CIE.column("#1",width=80,anchor="center")
		self.table_CIE.heading("#2",text="CIE")
		self.table_CIE.column("#2",width=200,anchor="center")										
		self.table_CIE.place(x=10,y=70,width=700,height=290)
		self.table_CIE.bind('<<TreeviewSelect>>',self.itemTable_SelectedCIE)

	def buscar_cie(self,event):		
		self.borrarTabla(self.table_CIE)
		parametro=''		
		if len(self.Entry_buscar_General.get())!=0:			
			parametro=parametro+self.Entry_buscar_General.get()
			obj_query=queryTriaje()
			rows=obj_query.query_cie10(parametro)			
			for valores in rows:
				self.table_CIE.insert('','end',values=(valores.CODCIE,valores.NOMBRE))

	def itemTable_SelectedCIE(self,event):
		if len(self.table_CIE.focus())!=0:
			codigo=self.table_CIE.item(self.table_CIE.selection()[0],option='values')[0]
			descripcion=self.table_CIE.item(self.table_CIE.selection()[0],option='values')[1]
			valorbool=False
			for item in self.table_DX.get_children():
				if self.table_DX.item(item,'values')[0]==codigo:
					valorbool=True
			if not valorbool:
				self.table_DX.insert('',"end",values=(codigo,descripcion))	
				self.TopCIE.destroy()
			else:
				messagebox.showerror("Alerta","El diagnostico ya Existe!!")	

	def eliminarSeleccionTable(self,table):
		seleccion=self.table_DX.focus()
		if seleccion:
			self.table_DX.delete(seleccion)

	def insertAIRN(self):
		datos=[]
		datos.append(self.AEntry_HCL.get())
		datos.append(self.AEntry_CNV.get())
		datos.append(self.AEntry_PINZAMIENTO.get() if self.AEntry_PINZAMIENTO.get() else "null")

		if self.checkContactoP.get():
			datos.append("APEGO")
		else:			
			datos.append(self.AEntry_CONTACTPRECOZ.get())
		

		datos.append(self.AEntry_LME.get())
		datos.append(self.ACOMBO_PAPACANGURO.get())
		datos.append(self.AEntry_PESO.get())
		datos.append(self.AEntry_TALLA.get())
		datos.append(self.AEntry_PC.get())
		datos.append(self.AEntry_PT.get())
		datos.append(self.AEntry_PA.get())
		datos.append(self.AEntry_PB.get())
		datos.append(self.AEntry_EXFI.get())
		datos.append(self.AEntry_FUR.get())
		datos.append(self.AEntry_APGAR1.get())
		datos.append(self.AEntry_APGAR5.get())
		datos.append(self.AEntry_APGAR10.get() if len(self.AEntry_APGAR10.get())>0 else -1)
		datos.append(self.AEntry_TEMPERATURA.get())
		datos.append(self.ACOMBO_OCULAR.get())
		datos.append(self.ACOMBO_VIT.get())
		datos.append(self.ACOMBO_NUTRICIONAL.get())
		datos.append(self.AEntry_AMNIOTICO.get())
		datos.append(self.AEntry_KRISTELLER.get())
		datos.append(self.ACOMBO_MECONICO.get())
		datos.append(self.ACOMBO_ORINA.get())
		datos.append(self.ACOMBO_ASFIXIA.get())
		datos.append(self.AEntry_DESTINORN.get())
		datos.append(self.AEntry_OBSERVACION.get() if self.AEntry_OBSERVACION.get() else "null")
		#datos.append(self.AEntry_DX.get())
		idmadre=self.table_Madres.item(self.table_Madres.selection()[0],option="values")[0]

		datos.append(self.AEntry_GRUPOF.get())
		#datos.append(idmadre)
		datos.append(self.id_mad)
		horaEAIRN="{}:{}".format(*self.time_EgresoAIRN.time())	
		datos.append(horaEAIRN)
		datos.append(1 if self.estadoHospitalizado.get() else 0)
		datos.append(1 if self.estadoInterconsulta.get() else 0)
		self.AEntry_MedicoInterconsulta.configure(state='normal')
		datos.append(" " if len(self.AEntry_MedicoInterconsulta.get())<1 else self.AEntry_MedicoInterconsulta.get())		
		#datos.append
		self.AEntry_Datos['state']='normal'
		if len(self.AEntry_Datos.get())>0:						
			if len(datos)==34:
				fecha=str(self.Fecha_NacimientoRN)[:10]
				if len(self.table_DX.get_children()) or not self.estadoHospitalizado.get():
					#print("entra")
					numero,codigoAIR=self.obj_consultaN.Insert_AIRN(datos,fecha,self.iduser)
					numero=1
					if numero:
						self.obj_consultaN.Update_Tabla('MADRE','estadoAIRN',1,'IDMADRE',self.id_mad)
						for item in self.table_DX.get_children():
							codigo=self.table_DX.item(item,'values')[0]
							#print(codigoAIR,codigo)
							self.obj_consultaN.insertarDxAIR(codigo,codigoAIR)
						messagebox.showinfo("Alerta","Se insertó correctamente!")
						self.TopAIRN.destroy()
						self.llenar_MadreNacido()
						self.llenar_TMadre()
					else:
						messagebox.showerror("Alerta","no se pudo insertar!")
				else:
					messagebox.showerror("Alerta","Ingrese por lo menos un diagnostico!!")
			else:
				messagebox.showerror("Alerta","Ingrese todo los campos")
		else:
			messagebox.showerror('Alerta!','Ingrese una Historia válida')

	#ALOJAMIENTO
	def Frame_Alojamiento(self,frame,width,height):
		frameM=Frame(frame,width=width,height=height,bg="#828682")
		frameM.place(x=0,y=0)
		frameM.pack_propagate(False)

		buttonHistorial=Label(frameM,image=self.btnHistorialphoto,cursor='hand2',bg='#828682')
		buttonHistorial.bind("<Button-1>",self.HistorialAlojamiento)
		buttonHistorial.grid(row=1,column=3,pady=10,padx=10)

		letra_leyenda=('Candara',16,'bold italic')
		label=Label(frameM,text="Datos por ingresar pacientes de alojamiento",bg="#828682",font=letra_leyenda)
		label.grid(row=0,column=1,pady=10,columnspan=20)
		style=ttk.Style()
		style.theme_use("default")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','green')])

		self.table_Alojamiento=ttk.Treeview(frameM,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_Alojamiento.heading("#1",text="Item")
		self.table_Alojamiento.column("#1",width=30,anchor="w",stretch='NO')
		self.table_Alojamiento.heading("#2",text="DNI MADRE")
		self.table_Alojamiento.column("#2",width=100,anchor="w",stretch='NO')
		self.table_Alojamiento.heading("#3",text="DATOS MADRE")
		self.table_Alojamiento.column("#3",width=500,anchor="w",stretch='NO')
		self.table_Alojamiento.heading("#4",text="DATOS NACIDO")
		self.table_Alojamiento.column("#4",width=200,anchor="w",stretch='NO')
		self.table_Alojamiento.heading("#5",text="HCL NACIDO")
		self.table_Alojamiento.column("#5",width=200,anchor="w",stretch='NO')
		self.table_Alojamiento.heading("#6",text="Fecha Nac. RN")
		self.table_Alojamiento.column("#6",width=200,anchor="w",stretch='NO')						
		self.table_Alojamiento.grid(row=3,column=2,padx=10,pady=2,columnspan=20)
		#self.table_Alojamiento.bind('<<TreeviewSelect>>',self.Selection_Table)
		self.llenar_TAlojamiento()
		self.table_Alojamiento.bind("<Double-Button-1>",self.top_Alojamiento) 
		
	def llenar_TAlojamiento(self):
		self.borrarTabla(self.table_Alojamiento)
		rows=self.obj_consultaN.ConsultaIngresaAlojamiento()
		obj_Paciente=queryGalen()
		for val in rows:
			rowG=obj_Paciente.query_Paciente(val.DNI)
			rowsNacido=obj_Paciente.query_PacienteXHCL(val.HCL)						
			self.table_Alojamiento.insert("","end",values=(val.Id_AIR,val.DNI,rowG[0].PrimerNombre+" "+rowG[0].ApellidoPaterno+" "+rowG[0].ApellidoMaterno,rowsNacido[0].PrimerNombre+" "+rowsNacido[0].ApellidoPaterno+" "+rowsNacido[0].ApellidoMaterno,val.HCL,rowsNacido[0].FechaNacimiento))

	def top_Alojamiento(self,event):
		self.top_Alojamiento=Toplevel()
		self.top_Alojamiento.geometry("600x450")
		self.top_Alojamiento.title("Ingresar datos")
		self.top_Alojamiento.grab_set()
		self.top_Alojamiento.resizable(0,0)

		label=Label(self.top_Alojamiento,text="Fecha Alta: ",font=('Arial',10,'bold'))
		label.grid(row=1,column=1,pady=10)	
		self.fechaAltaA=DateEntry(self.top_Alojamiento,selectmode='day',date_pattern='yyyy-MM-dd')
		self.fechaAltaA.grid(row=1,column=2,pady=10,padx=10)
		#self.fechaHasta.bind("<<DateEntrySelected>>",lambda event:self.event_Combo(event,0))

		label=Label(self.top_Alojamiento,text="ALTA: ",font=('Arial',10,'bold'))
		label.grid(row=1,column=3,pady=10)
		self.ACOMBO_AltaA=ttk.Combobox(self.top_Alojamiento,width=15,values=['SI','NO'])
		self.ACOMBO_AltaA.current(0)
		self.ACOMBO_AltaA.grid(row=1,column=4,pady=10)

		label=Label(self.top_Alojamiento,text="Fecha Tamizaje: ",font=('Arial',10,'bold'))
		label.grid(row=2,column=1,pady=10)	
		self.fechaTamizajeA=DateEntry(self.top_Alojamiento,selectmode='day',date_pattern='yyyy-MM-dd')
		self.fechaTamizajeA.grid(row=2,column=2,pady=10,padx=10)

		label=Label(self.top_Alojamiento,text="Hemoglobina: ",font=('Arial',10,'bold'))
		label.grid(row=2,column=3,pady=10)
		self.AEntry_HemoglobinaA=ttk.Entry(self.top_Alojamiento,width=15)
		self.AEntry_HemoglobinaA.bind("<KeyRelease>",lambda event:self.validarDecimales(event,self.AEntry_HemoglobinaA))
		self.AEntry_HemoglobinaA.grid(row=2,column=4,pady=10)

		label=Label(self.top_Alojamiento,text="Resp. Medico: ",font=('Arial',10,'bold'))
		label.grid(row=3,column=1,pady=10)
		self.AEntry_MedicoA=ttk.Entry(self.top_Alojamiento,width=15,state="readonly")
		self.AEntry_MedicoA.grid(row=3,column=2,pady=10)
		self.AEntry_MedicoA.bind("<Return>",lambda event:self.Search_Personal(event,"MEDICOA"))
		
		label=Label(self.top_Alojamiento,text="Observacion: ",font=('Arial',10,'bold'))
		label.grid(row=3,column=3,pady=10)
		self.AEntry_ObservacionA=ttk.Entry(self.top_Alojamiento,width=15)
		self.AEntry_ObservacionA.grid(row=3,column=4,pady=10)

		self.checkTransferenciaFromAlojamiento=BooleanVar()

		check=Checkbutton(self.top_Alojamiento,text="Transferir",variable=self.checkTransferenciaFromAlojamiento)
		check.grid(row=4,column=2,columnspan=2)
		check['command']=self.validarCheckAlojamiento

		self.marcoTransferencia=LabelFrame(self.top_Alojamiento,text="Datos de Transferencia",fg="blue",padx=10,pady=10)
		self.marcoTransferencia.grid(row=5,column=0,columnspan=6)

		label=Label(self.marcoTransferencia,text="Servicio ",font=('Arial',10,'bold'))
		label.grid(row=1,column=1,pady=10)
		self.comboServicioAlojamiento=ttk.Combobox(self.marcoTransferencia,state="disabled")
		self.comboServicioAlojamiento.grid(row=1,column=2,pady=10,padx=10)
		
		label=Label(self.marcoTransferencia,text="Edada Gest. ",font=('Arial',10,'bold'))
		label.grid(row=1,column=3,pady=10)
		self.entry_EdadGestacionalAlojamiento=ttk.Entry(self.marcoTransferencia)
		self.entry_EdadGestacionalAlojamiento.grid(row=1,column=4)

		label=Label(self.marcoTransferencia,text="Procedencia Madre ",font=('Arial',10,'bold'))
		label.grid(row=2,column=1,pady=10)
		self.entry_ProcendenciaMadre=ttk.Entry(self.marcoTransferencia)
		self.entry_ProcendenciaMadre.grid(row=2,column=2)

		label=Label(self.marcoTransferencia,text="Lugar Nac. ",font=('Arial',10,'bold'))
		label.grid(row=2,column=3,pady=10)
		self.comboLugarNacAlojamiento=ttk.Combobox(self.marcoTransferencia,values=['Hospital','Puesto Salud','Centro Salud','Trayectoria','Domicilio'])
		self.comboLugarNacAlojamiento.grid(row=2,column=4,pady=10,padx=10)
		self.comboLugarNacAlojamiento.current(0)

		btnAdd=ttk.Button(self.top_Alojamiento,text="Agregar")
		btnAdd.grid(row=6,column=2,pady=10,padx=10)
		btnAdd['command']=self.insert_Alojamiento

		btnCancelar=ttk.Button(self.top_Alojamiento,text='Cancelar')
		btnCancelar['command']=self.top_Alojamiento.destroy
		btnCancelar.grid(row=6,column=3,pady=10,padx=10)

	def llenarAlojamientoServicio(self):
		from Neonatologia.consultaNeonatologia import Consulta
		obj_ConsultaNeo=Consulta()
		rows=obj_ConsultaNeo.get_Destinos()
		datos=[]
		for val in rows:
			datos.append(str(val.ID_DESTINO)+"-"+val.NOMBRE_DESTINO)
		if len(datos):
			self.comboServicioAlojamiento['values']=datos
			self.comboServicioAlojamiento.current(0)

	def validarCheckAlojamiento(self):
		
		if  self.checkTransferenciaFromAlojamiento.get():
			self.comboServicioAlojamiento.configure(state='readonly')
			self.llenarAlojamientoServicio()
			self.AEntry_ObservacionA.configure(state='disabled')
			self.marcoTransferencia.configure(text="Se considera los datos dentro del marco",fg="green")
		else:
			self.AEntry_ObservacionA.configure(state='normal')
			self.comboServicioAlojamiento.configure(state='disabled')
			self.marcoTransferencia.configure(text="No se considera los datos dentro del marco",fg="red")

	def insert_Alojamiento(self):

		Id_AIR=self.table_Alojamiento.item(self.table_Alojamiento.selection()[0],option='values')[0]
		fechaAlta=self.fechaAltaA.get_date()
		alta=self.ACOMBO_AltaA.get()
		fecha_tamizaje=self.fechaAltaA.get_date()
		hemoglobina=self.AEntry_HemoglobinaA.get()
		self.AEntry_MedicoA.configure(state="normal")
		medicoA=self.AEntry_MedicoA.get()

		observacion=self.comboServicioAlojamiento.get()[:1] if self.checkTransferenciaFromAlojamiento.get() else self.AEntry_ObservacionA.get()

		datos=[fechaAlta,alta,fecha_tamizaje,hemoglobina,medicoA,observacion,Id_AIR]

		if len(datos)==7:
			nro=self.obj_consultaN.insert_Alojamiento(datos)
			if nro:
				self.obj_consultaN.Update_Tabla('AIR','estadoAlojamiento',1,'Id_AIR',Id_AIR)

				if self.checkTransferenciaFromAlojamiento.get():
					from Neonatologia.consultaNeonatologia import Consulta
					rows=self.obj_consultaN.consulta_datosAir(Id_AIR)
					HCLRN=rows[0].HCL
					DNIMADRE=rows[0].DNI
					edadGestacional=self.entry_EdadGestacionalAlojamiento.get()
					LugarNacimiento=self.comboLugarNacAlojamiento.get()
					tipo_parto=rows[0].tipo_Parto
					procedenciaMadre=self.entry_ProcendenciaMadre.get()

					obj_neo=Consulta()
					nro,idIngreso=obj_neo.InsertarDatosGenerales(HCLRN,DNIMADRE,edadGestacional,LugarNacimiento,tipo_parto,procedenciaMadre)
					destino=self.comboServicioAlojamiento.get()[:1]

					if nro:
						obj_neo.InsertarINGRESO(idIngreso,destino)

				messagebox.showinfo("Alerta","Se inserto correctamente")
				self.top_Alojamiento.destroy()
				self.llenar_TAlojamiento()
			else:
				messagebox.showerror("Alerta","No pudo Ingresar!!")
		else:
			messagebox.showinfo("Notificación","Ingrese todos los campos")

	def HistorialAIRN(self,event):		

		frameHistorial=Frame(self.frameMadre,width=self.width,height=self.height,bg='#828682')
		frameHistorial.place(x=0,y=0)
		frameHistorial.grid_propagate(False)


		self.menuObservacion=Menu(frameHistorial,tearoff=0)
		self.menuObservacion.add_command(label="Ingresa Observacion",command=self.insertObservacionAirn)
		self.menuObservacion.add_command(label="Salir de Observacion",command=self.Update_Observacion)

		label=Label(frameHistorial,text="Historial de los ultimos Ingresos",bg="#828682",fg="#fff",font=("Helvetica", "16"))
		label.grid(row=2,column=1,columnspan=10)

		label=Label(frameHistorial,text="Buscar Hcl NACIDO: ",font=('Helvetica',"14"),bg='#828682')
		label.grid(row=3,column=2,pady=10)
		entry_searchHistorialAIRN=ttk.Entry(frameHistorial)
		entry_searchHistorialAIRN.grid(row=3,column=3,pady=10)
		entry_searchHistorialAIRN.bind("<KeyRelease>",lambda event:self.searchHistorialAIRN(event,entry_searchHistorialAIRN))

		self.table_HistorialAIRN=ttk.Treeview(frameHistorial,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_HistorialAIRN.heading("#1",text="Item")
		self.table_HistorialAIRN.column("#1",width=30,anchor="w",stretch='NO')
		self.table_HistorialAIRN.heading("#2",text="DNI MADRE")
		self.table_HistorialAIRN.column("#2",width=100,anchor="w",stretch='NO')
		self.table_HistorialAIRN.heading("#3",text="DATOS MADRE")
		self.table_HistorialAIRN.column("#3",width=400,anchor="w",stretch='NO')
		self.table_HistorialAIRN.heading("#4",text="DATOS NACIDO")
		self.table_HistorialAIRN.column("#4",width=300,anchor="w",stretch='NO')
		self.table_HistorialAIRN.heading("#5",text="HCL NACIDO")
		self.table_HistorialAIRN.column("#5",width=200,anchor="w",stretch='NO')
		self.table_HistorialAIRN.heading("#6",text="Fecha Nac. RN")
		self.table_HistorialAIRN.column("#6",width=200,anchor="w",stretch='NO')						
		self.table_HistorialAIRN.grid(row=4,column=0,padx=10,pady=2,columnspan=10)
		self.table_HistorialAIRN.bind("<Button-3>",self.EventMenuAirn)
		self.llenarTablaHistorialAIRN()

	def EventMenuAirn(self,event):
		item=self.table_HistorialAIRN.identify_row(event.y)
		self.table_HistorialAIRN.selection_set(item)
		self.menuObservacion.post(event.x_root,event.y_root)

	def insertObservacionAirn(self):
		if self.table_HistorialAIRN.selection():
			idAirn=self.table_HistorialAIRN.item(self.table_HistorialAIRN.selection())["values"][0]
			
			rowsid=self.obj_consultaN.get_idTable("OBSERVACIONAIRN","Id_AIR",idAirn,"id_obs")
			
			if not rowsid:
				self.top_ObsAirn=Toplevel()
				self.top_ObsAirn.geometry("430x320")
				self.top_ObsAirn.title("Ingresar datos")
				self.top_ObsAirn.grab_set()
				self.top_ObsAirn.resizable(0,0)

				self.table_DxObservacion=ttk.Treeview(self.top_ObsAirn,columns=('#1','#2','#3'),show='headings')
				self.table_DxObservacion.heading("#1",text="CODCIE")
				self.table_DxObservacion.column("#1",width=80,anchor="w",stretch='NO')
				self.table_DxObservacion.heading("#2",text="Descripcion")
				self.table_DxObservacion.column("#2",width=250,anchor="w",stretch='NO')
				self.table_DxObservacion.heading("#3",text="Tipo Dx")
				self.table_DxObservacion.column("#3",width=70,anchor="w",stretch='NO')	
				self.table_DxObservacion.bind("<Button-3>",self.EventMenuObservacion)						
				self.table_DxObservacion.grid(row=2,column=0,padx=10,pady=2,columnspan=10)

				btn=Button(self.top_ObsAirn,text='Guardar')
				btn.configure(command=self.save_ObservacionAirn)
				btn.grid(row=3,column=2)

				btncancelar=Button(self.top_ObsAirn,text='Cancelar')
				btncancelar.configure(command=self.top_ObsAirn.destroy)
				btncancelar.grid(row=3,column=3)

				self.menuObservacionDX=Menu(self.top_ObsAirn,tearoff=0)
				self.menuObservacionDX.add_command(label="Agregar Dx",command=self.top_DxObservacionAdd)
				self.menuObservacionDX.add_command(label="Quitar",command=lambda:util.borrar_seleccionado(self.table_DxObservacion))
			else:
				messagebox.showerror("Error","Ya cuenta con un registro!!")
		else:
			messagebox.showerror("Alerta","Seleccione un Item")
	def Update_Observacion(self):
		if self.table_HistorialAIRN.selection():
			idAirn=self.table_HistorialAIRN.item(self.table_HistorialAIRN.selection())["values"][0]
			rowsid=self.obj_consultaN.get_idTable("OBSERVACIONAIRN","Id_AIR",idAirn,"id_obs")			
			if rowsid:
				alta=self.obj_consultaN.get_idTable("OBSERVACIONAIRN","Id_AIR",idAirn,"ESTADO")				
				
				if not alta[0].ESTADO:
					idobservacion=rowsid[0].id_obs				
					nro=self.obj_consultaN.AltaObservacion(1,idobservacion)
					if nro:
						messagebox.showinfo('Notificación','Se actualizó correctamente')
					else:
						messagebox.showerror('Error','No se pudo actualizar')
				else:
					messagebox.showerror("Error","Ya tiene el registro de Alta")
			else:
				messagebox.showerror("Error","No se puede dar de alta, el paciente no ingresó")
		else:
			messagebox.showerror("Error","Seleccione un Item!!")

	def save_ObservacionAirn(self):
		idAirn=self.table_HistorialAIRN.item(self.table_HistorialAIRN.selection())["values"][0]
		
		from datetime import datetime
		get_idMax=self.obj_consultaN.get_id("OBSERVACIONAIRN","id_obs")
		nro=1 if get_idMax[0].ID==None else get_idMax[0].ID+1
		
		
		estado=0
		nro=self.obj_consultaN.Insert_AIRNObservacion([nro,idAirn,0,0])

		for child in self.table_DxObservacion.get_children():

			get_idMaxDx=self.obj_consultaN.get_id("DXOBSERVACIONAIRN","Id_DxObs")
			nrdx=1 if get_idMaxDx[0].ID==None else get_idMaxDx[0].ID+1
			CODCIE=self.table_DxObservacion.item(child)["values"][0]
			descripcion=self.table_DxObservacion.item(child)["values"][1]
			tipo=self.table_DxObservacion.item(child)["values"][2]
			self.obj_consultaN.Insert_AIRNObservacionDX([nrdx,CODCIE,descripcion,tipo,nro])

		self.top_ObsAirn.destroy()
		messagebox.showinfo("Notificación",'exitoso')

	def EventMenuObservacion(self,event):
		item=self.table_DxObservacion.identify_row(event.y)
		self.table_DxObservacion.selection_set(item)
		self.menuObservacionDX.post(event.x_root,event.y_root)

	def top_DxObservacionAdd(self):
		self.top_AddDx=Toplevel()
		self.top_AddDx.title("Buscar Diagnostico")
		self.top_AddDx.iconbitmap('img/buscar.ico')
		self.top_AddDx.geometry("600x100")
		self.top_AddDx.resizable(0,0)
		self.top_AddDx.grab_set()

		#itemTable=self.table_datos.selection()[0]
		#id_diagnostico=self.table_datos.item(self.table_datos.selection()[0])['values'][0]
	

		label=Label(self.top_AddDx,text="CIE")
		label.grid(row=1,column=1)
		self.cie_entryEditar=ttk.Entry(self.top_AddDx,width=15)
		self.cie_entryEditar.bind("<Return>",self.fill_DXv2)
		self.cie_entryEditar.grid(row=1,column=2)

		label=Label(self.top_AddDx,text="Descripcion")
		label.grid(row=1,column=3)
		self.Descripcion_entryEditar=ttk.Entry(self.top_AddDx,width=30)
		self.Descripcion_entryEditar.grid(row=1,column=4)

		label=Label(self.top_AddDx,text="Tipo")
		label.grid(row=1,column=5)
		self.Tipo_entryEditar=ttk.Combobox(self.top_AddDx,width=15,values=["P","D","R"])
		self.Tipo_entryEditar.current(0)
		self.Tipo_entryEditar.grid(row=1,column=6)		

		button_GrabarDX=ttk.Button(self.top_AddDx,text="Aceptar")
		button_GrabarDX["command"]=self.InsertTableObsDX
		button_GrabarDX.grid(row=2,column=4,pady=5)

	def InsertTableObsDX(self):
		cie=self.cie_entryEditar.get()
		descripcion=self.Descripcion_entryEditar.get()
		tipo=self.Tipo_entryEditar.get()
		rows=[cie,descripcion,tipo]
		self.table_DxObservacion.insert("","end",values=rows)
		self.top_AddDx.destroy()
		#util.llenar_Table(self.table_DxObservacion,rows,["cie","descripcion","tipo"])

	def fill_DXv2(self,event):
		param=self.cie_entryEditar.get()
		rows=self.obj_ConsultaTriaje.query_cie10Param(param)

		try:
			self.Descripcion_entryEditar.delete(0,'end')
			self.Descripcion_entryEditar.insert(0,rows[0].NOMBRE)
		except Exception as e:
			messagebox.showerror("Alerta","Datos no Encontrados")			
			self.top_EditarC.destroy()
			self.Top_Editar.grab_set()

	def fillTableObservacion(self):
		pass
	def llenarTablaHistorialAIRN(self):
		rows=self.obj_consultaN.consulta_DigitadosAIRN()
		obj_Paciente=queryGalen()
		for val in rows:
			rowsMadre=obj_Paciente.query_Paciente(val.DNI)
			rowsNacido=obj_Paciente.query_PacienteXHCL(val.HCL)

			self.table_HistorialAIRN.insert("","end",values=(val.Id_AIR,val.DNI,rowsMadre[0].PrimerNombre+" "+rowsMadre[0].ApellidoPaterno+" "+rowsMadre[0].ApellidoMaterno,rowsNacido[0].PrimerNombre+" "+rowsNacido[0].ApellidoPaterno+" "+rowsNacido[0].ApellidoMaterno,val.HCL,rowsNacido[0].FechaNacimiento))
	
	def searchHistorialAIRN(self,event,entry):
		param=""
		param=param+entry.get()
		self.borrar_tabla(self.table_HistorialAIRN)
		rows=self.obj_consultaN.consulta_DigitadosAIRNLike(param)
		obj_Paciente=queryGalen()

		for val in rows:
			rowsMadre=obj_Paciente.query_Paciente(val.DNI)
			rowsNacido=obj_Paciente.query_PacienteXHCL(val.HCL)
			self.table_HistorialAIRN.insert("","end",values=("ID",val.DNI,rowsMadre[0].PrimerNombre+" "+rowsMadre[0].ApellidoPaterno+" "+rowsMadre[0].ApellidoMaterno,rowsNacido[0].PrimerNombre+" "+rowsNacido[0].ApellidoPaterno+" "+rowsNacido[0].ApellidoMaterno,val.HCL,rowsNacido[0].FechaNacimiento))

	def borrar_tabla(self,Tabla):				
		for item in Tabla.get_children():
			Tabla.delete(item)

	def HistorialAlojamiento(self,event):
		frameHistorialAlojamiento=Frame(self.frameMadre,width=self.width,height=self.height,bg='#828682')
		frameHistorialAlojamiento.place(x=0,y=0)
		frameHistorialAlojamiento.grid_propagate(False)

		label=Label(frameHistorialAlojamiento,text="Historial de los ultimos Ingresos",bg="#828682",fg="#fff",font=("Helvetica", "16"))
		label.grid(row=2,column=1,columnspan=10)

		label=Label(frameHistorialAlojamiento,text="Buscar Hcl NACIDO: ",font=('Helvetica',"14"),bg='#828682')
		label.grid(row=3,column=2,pady=10)
		entry_searchHistorialAIRN=ttk.Entry(frameHistorialAlojamiento)
		entry_searchHistorialAIRN.grid(row=3,column=3,pady=10)
		entry_searchHistorialAIRN.bind("<KeyRelease>",lambda event:self.searchHistorialAlojamiento(event,entry_searchHistorialAIRN))

		self.table_HistorialAlojamiento=ttk.Treeview(frameHistorialAlojamiento,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_HistorialAlojamiento.heading("#1",text="Item")
		self.table_HistorialAlojamiento.column("#1",width=30,anchor="w",stretch='NO')
		self.table_HistorialAlojamiento.heading("#2",text="DNI MADRE")
		self.table_HistorialAlojamiento.column("#2",width=100,anchor="w",stretch='NO')
		self.table_HistorialAlojamiento.heading("#3",text="DATOS MADRE")
		self.table_HistorialAlojamiento.column("#3",width=400,anchor="w",stretch='NO')
		self.table_HistorialAlojamiento.heading("#4",text="DATOS NACIDO")
		self.table_HistorialAlojamiento.column("#4",width=300,anchor="w",stretch='NO')
		self.table_HistorialAlojamiento.heading("#5",text="HCL NACIDO")
		self.table_HistorialAlojamiento.column("#5",width=200,anchor="w",stretch='NO')
		self.table_HistorialAlojamiento.heading("#6",text="Fecha Nac. RN")
		self.table_HistorialAlojamiento.column("#6",width=200,anchor="w",stretch='NO')						
		self.table_HistorialAlojamiento.grid(row=4,column=0,padx=10,pady=2,columnspan=10)
		self.llenarTablaHistorialAlojamiento()

	def llenarTablaHistorialAlojamiento(self):
		rows=self.obj_consultaN.consulta_DigitadosAlojamiento()
		obj_Paciente=queryGalen()
		for val in rows:
			rowsMadre=obj_Paciente.query_Paciente(val.DNI)
			rowsNacido=obj_Paciente.query_PacienteXHCL(val.HCL)
			self.table_HistorialAlojamiento.insert("","end",values=("ID",val.DNI,rowsMadre[0].PrimerNombre+" "+rowsMadre[0].ApellidoPaterno+" "+rowsMadre[0].ApellidoMaterno,rowsNacido[0].PrimerNombre+" "+rowsNacido[0].ApellidoPaterno+" "+rowsNacido[0].ApellidoMaterno,val.HCL,rowsNacido[0].FechaNacimiento))
	

	def searchHistorialAlojamiento(self,event,entry):
		param=""
		param=param+entry.get()
		self.borrar_tabla(self.table_HistorialAlojamiento)
		rows=self.obj_consultaN.consulta_DigitadosAlojamientoLike(param)
		obj_Paciente=queryGalen()

		for val in rows:
			rowsMadre=obj_Paciente.query_Paciente(val.DNI)
			rowsNacido=obj_Paciente.query_PacienteXHCL(val.HCL)
			self.table_HistorialAlojamiento.insert("","end",values=("ID",val.DNI,rowsMadre[0].PrimerNombre+" "+rowsMadre[0].ApellidoPaterno+" "+rowsMadre[0].ApellidoMaterno,rowsNacido[0].PrimerNombre+" "+rowsNacido[0].ApellidoPaterno+" "+rowsNacido[0].ApellidoMaterno,val.HCL,rowsNacido[0].FechaNacimiento))


