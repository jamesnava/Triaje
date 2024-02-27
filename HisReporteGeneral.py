from tkinter import *
from tkinter import ttk,filedialog
from tkinter import messagebox
from tkcalendar import DateEntry
from Consulta_Galen import queryGalen
from reporte import Reporte


class ReporteHis(object):
	def __init__(self,dni):
		self.dni_user=dni
	def Frame_Reporte(self,frame,ancho,alto):
		frame.grid_propagate(False)
		letra=('Arial',18,'bold')
		label=Label(frame,text="Desde: ",font=letra,bg="#828682")
		label.grid(row=0,column=0,pady=10,padx=10)
		self.fechaDesde=DateEntry(frame,selectmode='day',date_pattern='yyyy-MM-dd')
		self.fechaDesde.grid(row=0,column=1,pady=10,padx=10)
		self.fechaDesde.bind("<<DateEntrySelected>>",lambda event:self.event_Combo(event,0))

		label=Label(frame,text="Hasta: ",font=letra,bg="#828682")
		label.grid(row=0,column=2,pady=10,padx=10)
		self.fechaHasta=DateEntry(frame,selectmode='day',date_pattern='yyyy-MM-dd')
		self.fechaHasta.grid(row=0,column=3,pady=10,padx=10)
		self.fechaHasta.bind("<<DateEntrySelected>>",lambda event:self.event_Combo(event,0))

		label=Label(frame,text="Medico: ",font=letra,bg="#828682")
		label.grid(row=0,column=4,pady=10,padx=10)
		self.medico=ttk.Entry(frame)
		self.medico.bind("<Return>",self.Top_searchMedico)
		self.medico.grid(row=0,column=5)

		label=Label(frame,text="Servicio",font=letra,bg="#828682")
		label.grid(row=0,column=6,pady=10,padx=10)
		self.comboServicio=ttk.Combobox(frame)
		self.comboServicio.grid(row=0,column=7,pady=10,padx=10)
		self.llenar_Lista()
		self.comboServicio.bind("<<ComboboxSelected>>",lambda event:self.event_Combo(event,1))

		self.btn_GenerarR=ttk.Button(frame,text="Generar Reporte",state="disabled")
		self.btn_GenerarR.grid(row=2,column=4,pady=10)
		self.btn_GenerarR["command"]=self.Generar_Reporte

	def Top_searchMedico(self,event):
		self.TopCIE=Toplevel()
		self.TopCIE.title('Medicos')		
		self.TopCIE.geometry("720x400+350+50")			
		self.TopCIE.grab_set()
		self.TopCIE.resizable(0,0)	
		#self.TopCIE.iconbitmap('image/diagnostico.ico')

		label_title=Label(self.TopCIE,text='Buscar')
		label_title.place(x=20,y=20)
		self.Entry_buscar_General=ttk.Entry(self.TopCIE,width=30)
		self.Entry_buscar_General.focus()
		self.Entry_buscar_General.place(x=80,y=20)
		self.Entry_buscar_General.bind('<Key>',self.buscar_paciente)		

		#tabla...
		self.table_CIE=ttk.Treeview(self.TopCIE,columns=('#1','#2'),show='headings')		
		self.table_CIE.heading("#1",text="DNI")
		self.table_CIE.column("#1",width=80,anchor="center")
		self.table_CIE.heading("#2",text="NOMBRES")
		self.table_CIE.column("#2",width=200,anchor="center")										
		self.table_CIE.place(x=10,y=70,width=700,height=290)
		self.table_CIE.bind('<<TreeviewSelect>>',self.itemTable_selected)

	def buscar_paciente(self,event):
		obj_ConsultaGalen=queryGalen()
		self.borrar_tabla()
		parametro=''		
		if len(self.Entry_buscar_General.get())!=0:
			parametro=parametro+self.Entry_buscar_General.get()
			rows=obj_ConsultaGalen.query_Empleado(parametro)
			for valores in rows:
				self.table_CIE.insert('','end',values=(valores.DNI,valores.Nombres+" "+valores.ApellidoPaterno+" "+valores.ApellidoMaterno))

	def borrar_tabla(self):
		for item in self.table_CIE.get_children():
			self.table_CIE.delete(item)

	def itemTable_selected(self,event):
		if len(self.table_CIE.focus())!=0:
			self.medico.delete(0,'end')			
			dni=self.table_CIE.item(self.table_CIE.selection()[0],option='values')[0].strip()
			self.medico.insert(0,dni)
			#self.medico.insert(0,self.table_CIE.item(self.table_CIE.selection()[0],option='values')[0])			
		self.TopCIE.destroy()

	def llenar_Lista(self):
		obj_Galen=queryGalen()
		datos=[]
		rows=obj_Galen.query_EspecialidadesExterno()
		for val in rows:
			datos.append(str(val.IdEspecialidad)+"_"+val.Nombre)

		self.comboServicio["values"]=datos
		self.comboServicio.current(0)

	def event_Combo(self,event,nro):

		if nro==1:
			self.btn_GenerarR.configure(state="normal")
		else:
			self.btn_GenerarR.configure(state="disabled")

	def Generar_Reporte(self):
		
		file_Address=filedialog.asksaveasfile(mode="w",defaultextension=".xlsx")
		idespecialidad=self.comboServicio.get()[:self.comboServicio.get().find("_")]
		fechaI=self.fechaDesde.get_date()
		fechaF=self.fechaHasta.get_date()		
		obj_reporte=Reporte()
		obj_reporte.Genera_RDatosGeneral(self.medico.get(),file_Address,fechaI,fechaF,idespecialidad)

		
		


