from cx_Freeze import setup, Executable

setup(
    name="MiAplicacion",
    version="0.1",
    description="Una breve descripción de la aplicación",
    executables=[Executable("main.py",base="Win32GUI",icon="desktop.ico")],
)