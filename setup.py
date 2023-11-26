import sys
from cx_Freeze import setup, Executable



# script Python principal
script = "main.py"

# Criar um executável
base = None
if sys.platform == "win32":
    base = "Win32GUI"  #"Win32GUI" para aplicação GUI no Windows

exe = Executable(
    script=script,
    base=base,
    icon="C:\\Users\\Victor\\Documents\\Faculdade\\Simple_Hash_Calculation\\Icon\\wp.ico", #Hashtag 2 icon by Icons8
)

# Configurações para a criação do executável
build_exe_options = {
    "packages": ["hashlib", "tkinter", "pyperclip", "os", "moviepy", "pydub", "datetime",],  # Lista de pacotes usados
    "excludes": [],
    "include_files": [],
}

setup(
    name="CalculadoraDeHash",
    version="1.3",
    description="Simples calculadora de hash que utiliza o método sha256",
    options={"build_exe": build_exe_options},
    executables=[exe]
)