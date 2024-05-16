from tkinter import messagebox
#borrar tabla
def borra_Table(tabla):
	for item in table.get_children():
		table.delete(item)
		
def llenar_Table(tabla,rows,lista):
	for val in rows:
		valores=tuple(getattr(val,valor) for valor in lista)
		tabla.insert('','end',values=valores)

def borrar_seleccionado(tabla):
	if tabla.selection():
		itemTable=tabla.selection()[0]
		tabla.delete(itemTable)
	else:
		messagebox.showerror("Error","No se puede quitar, seleccione un  Item!!")

def validarCampos(diccionario):

	for clave,valor in diccionario.items():
		if len(valor)==0:
			messagebox.showerror("Error",f"llenar el campo {clave}")			
			return 0
	return 1

def get_Treeview(tabla,indices):
	rows=[]
	for line in tabla.get_children():
		t=[]
		for i in indices:
			t.append(tabla.item(line)['values'][i])
		rows.append(tuple(t))
	return rows
