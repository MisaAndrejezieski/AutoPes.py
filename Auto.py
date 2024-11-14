import time
import pyautogui
import random
import logging
import requests
import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkinter import ttk
import threading
import asyncio
import os

# Configuração de logging
logging.basicConfig(
    filename='automacao_pesquisa.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Lista de temas e perguntas
temas_en = [
    "technology", "health", "education", "sports", "politics", "economy",
    "science", "art", "music", "literature", "history", "geography",
    "philosophy", "psychology", "sociology", "anthropology", "astronomy",
    "biology", "chemistry", "physics", "mathematics", "engineering",
    "medicine", "law", "administration", "marketing", "finance",
    "architecture", "design", "fashion", "gastronomy"
]

perguntas_en = [
    "What is {tema}?", "What are the latest news in {tema}?",
    "How does {tema} impact society?", "What are the main challenges in {tema}?",
    "Who are the leading experts in {tema}?", "How to make money with {tema}",
]

# Função para gerar pesquisas sobre um tema
def gerar_pesquisas_sobre_tema(tema, n):
    return random.sample([p.format(tema=tema) for p in perguntas_en], n)

# Função para abrir o navegador Edge
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
        return False

# Função para realizar uma pesquisa
def realizar_pesquisa(pesquisa):
    try:
        pyautogui.hotkey('ctrl', 't')
        pyautogui.write(pesquisa)
        pyautogui.press('enter')
        time.sleep(10)  # Espera para garantir que a pesquisa tenha sido carregada
        pyautogui.hotkey('ctrl', 'w')
        logging.info(f"Pesquisa realizada: {pesquisa}")
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")

# Função para limpar dados de navegação
def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        logging.info("Dados de navegação e cookies limpos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar dados de navegação: {e}")

# Função para fechar o navegador
def fechar_navegador():
    try:
        pyautogui.hotkey('alt', 'f4')
        logging.info("Navegador fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")

# Função para verificar conectividade
async def verificar_conectividade():
    try:
        endpoints = ['https://www.google.com', 'https://www.bing.com']
        for url in endpoints:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    logging.info(f"Conectividade com {url} verificada.")
                    return True
            except requests.ConnectionError:
                logging.warning(f"Falha ao acessar {url}. Tentando outro...")
        return False
    except requests.RequestException as e:
        logging.error(f"Erro ao verificar conectividade: {e}")
        return False

# Função para exibir o progresso na interface gráfica
def atualizar_progresso(label, valor):
    label.config(text=f"Progresso: {valor}%")
    root.update_idletasks()

# Função principal da automação
async def executar_automacao(num_temas=6, num_perguntas=6, intervalo=10):
    try:
        if await verificar_conectividade():
            if abrir_edge():
                for i in range(num_temas):
                    tema = random.choice(temas_en)
                    pesquisas = gerar_pesquisas_sobre_tema(tema, num_perguntas)
                    for j, pesquisa in enumerate(pesquisas):
                        realizar_pesquisa(pesquisa)
                        # Atualiza o progresso após cada pesquisa
                        atualizar_progresso(label_progresso, (i * num_perguntas + j + 1) * 100 / (num_temas * num_perguntas))
                        time.sleep(intervalo)  # Intervalo entre pesquisas
                    limpar_dados_navegacao()
                fechar_navegador()
                logging.info("Automação concluída com sucesso.")
        else:
            logging.error("Falha na verificação de conectividade com a internet.")
    except Exception as e:
        logging.error(f"Erro ao executar automação: {e}")

# Função para iniciar a automação em segundo plano
def iniciar_automacao_bg(num_temas, num_perguntas, intervalo):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(executar_automacao(num_temas, num_perguntas, intervalo))

# Interface gráfica
def iniciar_interface():
    global root, label_progresso

    root = tk.Tk()
    root.title("Automação de Pesquisa")

    # Caminhos dos arquivos
    icon_path = os.path.join(os.path.dirname(__file__), '22287dragon_98813.ico')
    image_path = os.path.join(os.path.dirname(__file__), '22287dragon_98813.png')

    # Adicionar ícone à barra superior
    root.iconbitmap(icon_path)

    # Configuração de cores e estilos
    root.geometry('500x500')
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

    ttk.Label(root, text="Intervalo entre Pesquisas (segundos):", style='TLabel').pack(pady=10)
    intervalo_pesquisas = ttk.Entry(root, width=20)
    intervalo_pesquisas.pack(pady=5)
    intervalo_pesquisas.insert(0, "10")

    label_conectividade = ttk.Label(root, text="Verificando conectividade...", style='TLabel')
    label_conectividade.pack(pady=10)

    label_progresso = ttk.Label(root, text="Progresso: 0%", style='TLabel')
    label_progresso.pack(pady=10)

    def iniciar_automacao_handler():
        try:
            temas = int(num_temas.get())
            perguntas = int(num_perguntas.get())
            intervalo = int(intervalo_pesquisas.get())
            threading.Thread(target=iniciar_automacao_bg, args=(temas, perguntas, intervalo), daemon=True).start()

            # Atualizar o status da conectividade
            if verificar_conectividade():
                label_conectividade.config(text="Conectividade OK", foreground="green")
            else:
                label_conectividade.config(text="Falha na Conectividade", foreground="red")
            
            messagebox.showinfo("Inicializado", "Automação iniciada em segundo plano.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

    ttk.Button(root, text="Iniciar Automação", command=iniciar_automacao_handler, style='TButton').pack(pady=10)

    # Adicionar botão para fechar o programa
    ttk.Button(root, text="Fechar Programa", command=root.quit, style='Red.TButton').pack(pady=10)

    # Adicionar imagem .png na interface
    img = PhotoImage(file=image_path)
    img_label = tk.Label(root, image=img)
    img_label.pack(pady=10)

    root.mainloop()

# Iniciar a interface gráfica
iniciar_interface()
