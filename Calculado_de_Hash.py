import tkinter as tk
from tkinter import filedialog
import hashlib
import tkinter.scrolledtext as scrolledtext
import pyperclip

# Função para calcular o hash de um arquivo
def calcular_hash(nome_arquivo, algoritmo='sha256'):
    """
    Calcula o hash de um arquivo utilizando um algoritmo de hash especificado.

    Args:
        nome_arquivo (str): O nome do arquivo a ser processado.
        algoritmo (str): O algoritmo de hash a ser utilizado (padrão é 'sha256').

    Returns:
        str: O hash calculado em formato hexadecimal.
    """
    try:
        with open(nome_arquivo, 'rb') as arquivo:
            conteudo = arquivo.read()
            hash_obj = hashlib.new(algoritmo)
            hash_obj.update(conteudo)
            hash_digest = hash_obj.hexdigest()
            return hash_digest
    except FileNotFoundError:
        return None

# Função para calcular hashes para vários arquivos
def calcular_hashes_para_varios_arquivos():
    """
    Abre uma caixa de diálogo para selecionar vários arquivos, calcula o hash para cada arquivo e exibe o resultado na área de texto.
    """
    lista_de_arquivos = filedialog.askopenfilenames(title="Selecionar arquivos")
    resultado_text.config(state=tk.NORMAL)
    resultado_text.delete(1.0, tk.END)  # Limpa o resultado anterior
    for nome_arquivo in lista_de_arquivos:
        hash = calcular_hash(nome_arquivo)
        if hash:
            resultado_text.insert(tk.END, f"Hash calculado para:\n{hash}\n{nome_arquivo}")
    resultado_text.config(state=tk.DISABLED)

# Função para copiar todos os hashes para a área de transferência
def copiar_hashes():
    """
    Copia todos os hashes exibidos na área de texto para a área de transferência.
    """
    texto = resultado_text.get(1.0, tk.END)
    pyperclip.copy(texto)

# Função para apagar todos os hashes da área de texto
def apagar_hashes():
    """
    Apaga todos os hashes exibidos na área de texto.
    """
    resultado_text.config(state=tk.NORMAL)
    resultado_text.delete(1.0, tk.END)
    resultado_text.config(state=tk.DISABLED)

# Configuração da janela
janela = tk.Tk()
janela.title("Calculadora de Hash")
janela.geometry("400x540")

# Botão para calcular hashes
calcular_button = tk.Button(janela, text="Calcular Hash para Arquivos", command=calcular_hashes_para_varios_arquivos)
calcular_button.pack(pady=10)

# Área de texto para exibir resultados
resultado_text = scrolledtext.ScrolledText(janela, wrap=tk.WORD, state=tk.DISABLED)
resultado_text.pack(fill=tk.BOTH, expand=True)

# Botão para copiar todos os hashes
copiar_button = tk.Button(janela, text="Copiar Todos os Hashes", command=copiar_hashes)
copiar_button.pack(pady=10)

# Botão para apagar todos os hashes
apagar_button = tk.Button(janela, text="Apagar Todos os Hashes", command=apagar_hashes)
apagar_button.pack(pady=10)

# Iniciar a interface gráfica
janela.mainloop()
