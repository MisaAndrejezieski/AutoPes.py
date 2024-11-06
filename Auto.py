import time
import pyautogui
import random
import logging
import requests
import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkinter import ttk
import threading
import os

# Configuração de logging
logging.basicConfig(
    filename='automacao_pesquisa.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Lista de temas em inglês
temas_en = [
    "technology", "health", "education", "sports", "politics", "economy",
    "science", "art", "music", "literature", "history", "geography",
    "philosophy", "psychology", "sociology", "anthropology", "astronomy",
    "biology", "chemistry", "physics", "mathematics", "engineering",
    "medicine", "law", "administration", "marketing", "finance",
    "architecture", "design", "fashion", "gastronomy"
]

# Lista de perguntas em inglês
perguntas_en = [
    "What is {tema}?", "What are the latest news in {tema}?",
    "How does {tema} impact society?", "What are the main challenges in {tema}?",
    "Who are the leading experts in {tema}?", "How to make money with {tema}",
]

# Função para gerar uma lista de pesquisas aleatórias sobre um tema
def gerar_pesquisas_sobre_tema(tema, n):
    return random.sample([p.format(tema=tema) for p in perguntas_en], n)

# Função para abrir o Edge
def abrir_edge():
    try:
        pyautogui.press('win')
        pyautogui.write('edge')
        pyautogui.press('enter')
        time.sleep(2)
        logging.info("Navegador Edge aberto com sucesso.")
        return True
    except Exception as e:
        logging.error(f"Erro ao abrir o Edge: {e}")
        raise e

# Função para realizar uma pesquisa
def realizar_pesquisa(pesquisa):
    try:
        pyautogui.hotkey('ctrl', 't')
        pyautogui.write(pesquisa)
        pyautogui.press('enter')
        time.sleep(10)
        pyautogui.hotkey('ctrl', 'w')
        logging.info(f"Pesquisa realizada: {pesquisa}")
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")
        raise e

# Função para limpar dados de navegação e cookies
def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        logging.info("Dados de navegação e cookies limpos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar os dados de navegação: {e}")
        raise e

# Função para fechar o navegador
def fechar_navegador():
    try:
        pyautogui.hotkey('alt', 'f4')
        logging.info("Navegador fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")
        raise e

# Função para verificar a conectividade com a internet
def verificar_conectividade():
    try:
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            logging.info("Conectividade com a internet verificada.")
            return True
        else:
            logging.error("Falha na verificação de conectividade com a internet.")
            return False
    except requests.ConnectionError as e:
        logging.error(f"Erro ao verificar a conectividade com a internet: {e}")
        raise e

# Função principal para executar a automação
def executar_automacao(num_temas=6, num_perguntas=6):
    try:
        if verificar_conectividade():
            if abrir_edge():
                for _ in range(num_temas):
                    tema = random.choice(temas_en)
                    pesquisas = gerar_pesquisas_sobre_tema( tema, num_perguntas)
                    for pesquisa in pesquisas:
                        realizar_pesquisa(pesquisa)
                    limpar_dados_navegacao()
                fechar_navegador()
                logging.info("Automação concluída com sucesso.")
            else:
                logging.error("Falha ao abrir o navegador.")
        else:
            logging.error("Falha na verificação de conectividade com a internet.")
    except Exception as e:
        logging.error(f"Erro ao executar a automação: {e}")

# Função para rodar a automação em segundo plano
def iniciar_automacao_bg(num_temas, num_perguntas):
    thread = threading.Thread(target=executar_automacao, args=(num_temas, num_perguntas))
    thread.start()

# Interface gráfica
def iniciar_interface():
    root = tk.Tk()
    root.title("Automação de Pesquisa")

    # Caminhos dos arquivos
    icon_path = os.path.join(os.path.dirname(__file__), '22287dragon_98813.ico')
    image_path = os.path.join(os.path.dirname(__file__), '22287dragon_98813.png')

    # Adicionar ícone à barra superior
    root.iconbitmap(icon_path)

    # Configuração de cores e estilos
    root.geometry('500x400')
    root.configure(bg='#282c34')
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', background='#4CAF50', foreground='#ffffff', font=('Helvetica', 12, 'bold'))
    style.map('TButton', background=[('active', '#56b6c2')])
    style.configure('Red.TButton', background='#f44336', foreground='#ffffff', font=('Helvetica', 12, 'bold'))
    style.map('Red.TButton', background=[('active', '#d32f2f')])
    style.configure('TLabel', background='#282c34', foreground='#61afef', font=('Helvetica', 12))
    style.configure('TEntry', font=('Helvetica', 12), padding=5)

    # Elementos da interface
    ttk.Label(root, text="Número de Temas:", style='TLabel').pack(pady=10)
    num_temas = ttk.Entry(root, width=20)
    num_temas.pack(pady=5)
    num_temas.insert(0, "6")

    ttk.Label(root, text="Número de Perguntas por Tema:", style='TLabel').pack(pady=10)
    num_perguntas = ttk.Entry(root , width=20)
    num_perguntas.pack(pady=5)
    num_perguntas.insert(0, "6")

    def iniciar_automacao():
        try:
            temas = int(num_temas.get())
            perguntas = int(num_perguntas.get())
            iniciar_automacao_bg(temas, perguntas)
            messagebox.showinfo("Inicializado", "Automação iniciada em segundo plano.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

    ttk.Button(root, text="Iniciar Automação", command=iniciar_automacao, style='TButton').pack(pady=10)

    # Adicionar botão para fechar o programa
    ttk.Button(root, text="Fechar Programa", command=root.quit, style='Red.TButton').pack(pady=10)

    # Adicionar imagem .png na interface
    img = PhotoImage(file=image_path)
    img_label = tk.Label(root, image=img)
    img_label.pack(pady=10)

    root.mainloop()

# Iniciar a interface gráfica
iniciar_interface()
