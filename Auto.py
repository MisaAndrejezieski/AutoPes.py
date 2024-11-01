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
    "biology", "chemistry", "physics", "mathematics", "engineering", "medicine",
    "law", "administration", "marketing", "finance", "architecture",
    "design", "fashion", "gastronomy"
]

# Lista de perguntas em inglês
perguntas_en = [
    "What is {tema}?", "What are the latest news in {tema}?", "How does {tema} impact society?",
    "What are the main challenges in {tema}?", "Who are the leading experts in {tema}?", "how to make money with {tema}",
]

# Funções de automação (não alteradas)

# Função principal para executar a automação
def executar_automacao(num_temas=6, num_perguntas=6):
    # (Código não alterado)

# Função para rodar a automação em segundo plano
def iniciar_automacao_bg(num_temas, num_perguntas):
    # (Código não alterado)

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
    style.configure('TLabel', background='#282c34', foreground='#61afef', font=('Helvetica', 10))
    style.configure('TEntry', font=('Helvetica', 10))

    # Elementos da interface
    ttk.Label(root, text="Número de Temas:", style='TLabel').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    num_temas = ttk.Entry(root)
    num_temas.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    num_temas.insert(0, "1")

    ttk.Label(root, text="Número de Perguntas por Tema:", style='TLabel').grid(row=1, column=0, padx=10, pady=10, sticky='e')
    num_perguntas = ttk.Entry(root)
    num_perguntas.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    num_perguntas.insert(0, "1")

    def iniciar_automacao():
        try:
            temas = int(num_temas.get())
            perguntas = int(num_perguntas.get())
            iniciar_automacao_bg(temas, perguntas)
            messagebox .showinfo("Inicializado", "Automação iniciada em segundo plano.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

    ttk.Button(root, text="Iniciar Automação", command=iniciar_automacao, style='TButton').grid(row=2, column=0, columnspan=2, pady=20)

    # Adicionar botão para fechar o programa
    ttk.Button(root, text="Fechar Programa", command=root.quit, style='Red.TButton').grid(row=3, column=0, columnspan=2, pady=10)

    # Adicionar imagem .png na interface
    img = PhotoImage(file=image_path)
    img_label = tk.Label(root, image=img)
    img_label.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

# Iniciar a interface gráfica
iniciar_interface()
