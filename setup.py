from cx_Freeze import setup,Executable

setup(
	name="Sistema de produccion Hospitalaria",
	version="1.7",
	description="Sistema de produccion hospitalaria",
	executables=[Executable("main.py")]
	)