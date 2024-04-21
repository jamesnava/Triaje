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