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
import csv
import asyncio

# Configuração de logging
logging.basicConfig(
    filename='automacao_eventos.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

logging.basicConfig(
    filename='automacao_erros.log',
    level=logging.ERROR,
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

# Função para salvar os resultados em CSV
def salvar_resultados(resultados):
    try:
        with open('resultados_pesquisas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if os.stat('resultados_pesquisas.csv').st_size == 0:
                writer.writerow(["Tema", "Pergunta", "Status"])
            for resultado in resultados:
                writer.writerow([resultado['tema'], resultado['pergunta'], resultado['status']])
    except Exception as e:
        logging.error(f"Erro ao salvar os resultados: {e}")

# Função de "tentar novamente" com múltiplas tentativas
def tentar_novamente(funcao, max_tentativas=3, *args, **kwargs):
    for tentativa in range(max_tentativas):
        try:
            return funcao(*args, **kwargs)
        except Exception as e:
            logging.error(f"Tentativa {tentativa+1} de {funcao.__name__} falhou: {e}")
            if tentativa + 1 == max_tentativas:
                logging.error(f"Falha ao tentar executar {funcao.__name__} após {max_tentativas} tentativas.")
                raise e
            time.sleep(2)  # Espera entre tentativas

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
        return False

# Função para realizar uma pesquisa
def realizar_pesquisa(pesquisa):
    try:
        pyautogui.hotkey('ctrl', 't')
        pyautogui.write(pesquisa)
        pyautogui.press('enter')
        time.sleep(10)
        pyautogui.hotkey('ctrl', 'w')
        logging.info(f"Pesquisa realizada: {pesquisa}")
        return True
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")
        return False

# Função para limpar dados de navegação e cookies
def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        logging.info("Dados de navegação e cookies limpos com sucesso.")
        return True
    except Exception as e:
        logging.error(f"Erro ao limpar os dados de navegação: {e}")
        return False

# Função para verificar a conectividade com a internet
async def verificar_conectividade():
    try:
        endpoints = ['https://www.google.com', 'https://www.bing.com', 'https://www.duckduckgo.com']
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

# Função para executar a automação
async def executar_automacao(num_temas=6, num_perguntas=6, intervalo=10, root=None):
    resultados = []
    if await verificar_conectividade():
        if abrir_edge():
            for _ in range(num_temas):
                tema = random.choice(temas_en)
                pesquisas = gerar_pesquisas_sobre_tema(tema, num_perguntas)
                for pesquisa in pesquisas:
                    sucesso = False
                    while not sucesso:
                        sucesso = realizar_pesquisa(pesquisa)
                        if not sucesso:
                            logging.error(f"Falha ao realizar a pesquisa: {pesquisa}. Tentando novamente.")
                            time.sleep(intervalo)
                    resultados.append({'tema': tema, 'pergunta': pesquisa, 'status': 'Concluída'})
                    await asyncio.sleep(intervalo)  # Delay entre pesquisas
                limpar_dados_navegacao()
            salvar_resultados(resultados)
            logging.info("Automação concluída com sucesso.")
            if root:
                root.quit()  # Fechar a interface gráfica após a execução
        else:
            logging.error("Falha ao abrir o navegador.")
            if root:
                root.quit()  # Fechar o programa caso falhe ao abrir o navegador
    else:
        logging.error("Falha na verificação de conectividade com a internet.")
        if root:
            root.quit()  # Fechar o programa caso falhe a conectividade

# Função para rodar a automação em segundo plano
def iniciar_automacao_bg(num_temas, num_perguntas, intervalo, root=None):
    asyncio.run(executar_automacao(num_temas, num_perguntas, intervalo, root))

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

    ttk.Label(root, text="Intervalo entre pesquisas (em segundos):", style='TLabel').pack(pady=10)
    intervalo = ttk.Entry(root, width=20)
    intervalo.pack(pady=5)
    intervalo.insert(0, "10")

    def iniciar_automacao_handler():
        try:
            temas = int(num_temas.get())
            perguntas = int(num_perguntas.get())
            intervalo_value = int(intervalo.get())
            if temas < 1 or perguntas < 1 or intervalo_value < 1:
                raise ValueError("Valores devem ser maiores que 0.")
            threading.Thread(target=iniciar_automacao_bg, args=(temas, perguntas, intervalo_value, root), daemon=True).start()
            messagebox.showinfo("Inicializado", "Automação iniciada em segundo plano.")
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

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
