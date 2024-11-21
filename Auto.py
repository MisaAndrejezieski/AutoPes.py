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

class Automacao:
    def __init__(self):
        self.resultados = []

    def gerar_pesquisas_sobre_tema(self, tema, n):
        return random.sample([p.format(tema=tema) for p in perguntas_en], n)

    def salvar_resultados(self):
        file_exists = os.path.isfile('resultados_pesquisas.csv')
        with open('resultados_pesquisas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Tema", "Pergunta", "Status"])
            for resultado in self.resultados:
                writer.writerow([resultado['tema'], resultado['pergunta'], resultado['status']])

    async def verificar_conectividade(self):
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

    async def executar_automacao(self, num_temas=6, num_perguntas=6):
        if await self.verificar_conectividade():
            if self.abrir_edge():
                for _ in range(num_temas):
                    tema = random.choice(temas_en)
                    pesquisas = self.gerar_pesquisas_sobre_tema(tema, num_perguntas)
                    for pesquisa in pesquisas:
                        sucesso = await self.realizar_pesquisa(pesquisa)
                        self.resultados.append({'tema': tema, 'pergunta': pesquisa, 'status': 'Concluída' if sucesso else 'Falha'})
                        await asyncio.sleep(5)
                self.salvar_resultados()
                logging.info("Automação concluída com sucesso.")
            else:
                logging.error("Falha ao abrir o navegador.")
        else:
            logging.error("Falha na verificação de conectividade com a internet.")

    def abrir_edge(self):
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

    async def realizar_pesquisa(self, pesquisa):
        for tentativa in range(3):  # Tentar até 3 vezes
            try:
                pyautogui.hotkey('ctrl', 't')
                pyautogui.write(pesquisa)
                pyautogui.press('enter')
                time.sleep(10)
                pyautogui.hotkey('ctrl', 'w')
                logging.info(f"Pesquisa realizada: {pesquisa}")
                return True
            except Exception as e:
                logging.error(f"Tentativa {tentativa + 1} de realizar a pesquisa falhou: {e}")
                if tentativa == 2:
                    logging.error(f"Falha ao realizar a pesquisa: {pesquisa} após 3 tentativas.")
                await asyncio.sleep(5)  # Espera antes de tentar novamente
        return False

class InterfaceGrafica:
    def __init__(self, automacao):
        self.automacao = automacao
        self.root = tk.Tk()
        self.root.title("Automação de Pesquisa")
        self.root.geometry('600x500')
        self.root.configure(bg='#cfffca')
        self.setup_ui()

    def setup_ui(self):
        # Estilos
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#A7D8D7', foreground='#2E4053', font=('Helvetica', 12, 'bold'))
        style.map('TButton', background=[('active', '#80C7C6')])
        style.configure('Red.TButton', background='#F28C8C', foreground='#2E4053', font=('Helvetica', 12, 'bold'))
        style.map('Red.TButton', background=[('active', '#F76C6C')])
        style.configure('TLabel', background='#F3F4F6', foreground='#2E4053', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12), padding=5)

        # Elementos da interface
        ttk.Label(self.root, text="Número de Temas:", style='TLabel').pack(pady=10)
        self.num_temas_entry = ttk.Entry(self.root, width=20)
        self.num_temas_entry.pack(pady=5)
        self.num_temas_entry.insert(0, "6")

        ttk.Label(self.root, text="Número de Perguntas por Tema:", style='TLabel').pack(pady=10)
        self.num_perguntas_entry = ttk.Entry(self.root, width=20)
        self.num_perguntas_entry.pack(pady=5)
        self.num_perguntas_entry.insert(0, "6")

        # Botão para iniciar a automação
        start_button = ttk.Button(self.root, text="Iniciar Automação", command=self.iniciar_automacao_handler)
        start_button.pack(pady=20)

        # Botão para fechar a aplicação
        close_button = ttk.Button(self.root, text="Fechar", command=self.root.quit, style='Red.TButton')
        close_button.pack(pady=10)

    def iniciar_automacao_handler(self):
        try:
            num_temas = int(self.num_temas_entry.get())
            num_perguntas = int(self.num_perguntas_entry.get())
            threading.Thread(target=self.run_automacao, args=(num_temas, num_perguntas)).start()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos.")

    def run_automacao(self, num_temas, num_perguntas):
        asyncio.run(self.automacao.executar_automacao(num_temas, num_perguntas))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    automacao = Automacao()
    interface = InterfaceGrafica(automacao)
    interface.run()
   