import tkinter as tk
from tkinter import filedialog
import hashlib
import tkinter.scrolledtext as scrolledtext
import pyperclip
import os
import datetime
from math import ceil
from moviepy.editor import VideoFileClip
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.wavpack import WavPack
from mutagen.aiff import AIFF
from mutagen.oggopus import OggOpus
from mutagen.ac3 import AC3
from mutagen.apev2 import APEv2
from mutagen.tak import TAK
from mutagen.wave import WAVE as WAV




def obter_duração_audio(file_path):
    formatos_suportados = [MP3, FLAC, OggVorbis, WAV, WavPack, AIFF, OggOpus, APEv2, WavPack, TAK, AC3, OggOpus]

    for audio_format in formatos_suportados:
        try:
            audio = audio_format(file_path)
            duracao_segundos_audio = audio.info.length
            comprimento_audio = formatar_comprimento(duracao_segundos_audio)
            return comprimento_audio
        except Exception as e:
            # Ignora erros e tenta o próximo formato
            pass

    return None

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
    Abre uma caixa de diálogo para selecionar vários arquivos, calcula o hash para cada arquivo
    e adiciona o resultado na área de texto sem apagar os hashes já calculados.
    """
    lista_de_arquivos = filedialog.askopenfilenames(title="Selecionar arquivos")
    for nome_arquivo in lista_de_arquivos:
        hash = calcular_hash(nome_arquivo)
        if hash:

            #Variaveis para obter os metadados dos arquivos
                get_name = os.path.basename(nome_arquivo)
                get_size = os.path.getsize(nome_arquivo)
                get_lastmodified = os.path.getmtime(nome_arquivo)
                get_lastmodified = datetime.datetime.fromtimestamp(get_lastmodified)
                get_lastmodified = get_lastmodified.strftime("%Y-%m-%d %H:%M:%S")

                extensoes_audio = ['mp3', 'wav', 'flac', 'aac', 'm4a', 'ogg', 'wma', 'alac', 'aiff', 'pcm', 'au', 'mid', 'midi', 'mp2', 
                                   'mpa', 'mpc', 'ape', 'mac', 'ra', 'rm', 'sln', 'tta', 'aac', 'ac3', 'dts', 'eac3', 'opus', 'pcm', 'wv']
                
                extensoe_video = ["mp4", 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'mpeg', 'mpg', '3gp', 'm4v', 'vob', 'ts', 'mts', 'm2ts', 'asf', '.264']
                

                #verificar se o arquivo é um vídeo
                if nome_arquivo.lower().endswith(tuple(extensoe_video)):
                    try:
                        clip = VideoFileClip(nome_arquivo)
                        duracao_segundos = clip.duration
                        comprimento_video = formatar_comprimento(duracao_segundos)
                        resultado_text.config(state=tk.NORMAL)
                        resultado_text.insert(tk.END, f'Nome do arquivo: {get_name}, Tamanho: {ceil(get_size/(1024))} KB, Modificado em: {get_lastmodified}, Duração: {comprimento_video} e Hash (SHA 256) {hash.upper()}\n')
                        resultado_text.config(state=tk.DISABLED)
                    except Exception:
                        resultado_text.config(state=tk.NORMAL)
                        resultado_text.insert(tk.END, f'Nome do arquivo: {get_name}, Tamanho: {ceil(get_size/(1024))} KB, Modificado em: {get_lastmodified} e Hash (SHA 256) {hash.upper()}\n')
                        resultado_text.config(state=tk.DISABLED)


                elif nome_arquivo.lower().endswith(tuple(extensoes_audio)):
                    comprimento_audio = obter_duração_audio(nome_arquivo)

                    if comprimento_audio is not None:
                        resultado_text.config(state=tk.NORMAL)
                        resultado_text.insert(tk.END, f'Nome do arquivo: {get_name}, Tamanho: {ceil(get_size/(1024))} KB, Modificado em: {get_lastmodified}, Duração: {comprimento_audio} e Hash (SHA 256) {hash.upper()}\n')
                        resultado_text.config(state=tk.DISABLED)
                    else:
                        print("Erro ao obter duração do áudio.")


                #Se for arquivo ou foto, mostrar o arquivo
                else:
                    resultado_text.config(state=tk.NORMAL)
                    resultado_text.insert(tk.END, f'Nome do arquivo: {get_name}, Tamanho: {ceil(get_size/(1024))} KB, Modificado em: {get_lastmodified} e Hash (SHA 256) {hash.upper()}\n')
                    resultado_text.config(state=tk.DISABLED)



def verificar_unidade(hour, min, sec):
    if sec != 0:
        return '%02d' % (hour) +' Horas ' +'%02d' % (min) +' Minutos e ' '%02d' % (sec) +' Segundos'

# Função para formatar o comprimento do arquivo
def formatar_comprimento(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    return verificar_unidade(hour, min, sec)

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

