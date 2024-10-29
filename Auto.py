import time
import pyautogui
import random
import logging
import requests
import tkinter as tk
from tkinter import messagebox

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
        messagebox.showerror("Erro", f"Erro ao abrir o Edge: {e}")
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
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")
        messagebox.showerror("Erro", f"Erro ao realizar a pesquisa: {e}")

# Função para limpar dados de navegação e cookies
def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        messagebox.showinfo("Sucesso", "Dados de navegação e cookies limpos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar os dados de navegação: {e}")
        messagebox.showerror("Erro", f"Erro ao limpar os dados de navegação: {e}")

# Função para fechar o navegador
def fechar_navegador():
    try:
        pyautogui.hotkey('alt', 'f4')
        logging.info("Navegador fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")
        messagebox.showerror("Erro", f"Erro ao fechar o navegador: {e}")

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
        messagebox.showerror("Erro", f"Erro ao verificar a conectividade com a internet: {e}")
        return False

# Função principal para executar a automação
def executar_automacao(num_temas=6, num_perguntas=6):
    if verificar_conectividade():
        for _ in range(num_temas):
            tema = random.choice(temas_en)
            pesquisas = gerar_pesquisas_sobre_tema(tema, num_perguntas)
            
            if abrir_edge():
                for pesquisa in pesquisas:
                    realizar_pesquisa(pesquisa)
                
                limpar_dados_navegacao()
                fechar_navegador()
            else:
                messagebox.showerror("Erro", "Não foi possível abrir o navegador Edge.")
    else:
        messagebox.showerror("Erro", "Não foi possível verificar a conectividade com a internet.")

# Interface gráfica
def iniciar_interface():
    root = tk.Tk()
    root.title("Automação de Pesquisa")
    
    tk.Label(root, text="Número de Temas:").grid(row=0, column=0, padx=10, pady=10)
    num_temas = tk.Entry(root)
    num_temas.grid(row=0, column=1, padx=10, pady=10)
    num_temas.insert(0, "6")
    
    tk.Label(root, text="Número de Perguntas por Tema:").grid(row=1, column=0, padx=10, pady=10)
    num_perguntas = tk.Entry(root)
    num_perguntas.grid(row=1, column=1, padx=10, pady=10)
    num_perguntas.insert(0, "6")
    
    def iniciar_automacao():
        try:
            temas = int(num_temas.get())
            perguntas = int(num_perguntas.get())
            executar_automacao(temas, perguntas)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
    
    tk.Button(root, text="Iniciar Automação", command=iniciar_automacao).grid(row=2, column=0, columnspan=2, pady=20)
    
    root.mainloop()

# Iniciar a interface gráfica
iniciar_interface()
