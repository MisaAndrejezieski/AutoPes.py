# ------------------------------------------------------------
# AutoPes.py — Automação de Pesquisas com Interface Gráfica
# Autor: Misael Andrejezieski
# ------------------------------------------------------------
# Este programa realiza pesquisas automáticas no Microsoft Edge
# sobre temas variados, salvando os resultados em CSV e logs.
# Possui interface Tkinter e fecha o navegador ao final.
# ------------------------------------------------------------

import time
import pyautogui
import random
import logging
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import os
import csv
import asyncio

# ------------------------------------------------------------
# CONFIGURAÇÃO DE LOGS
# ------------------------------------------------------------
# Cria um arquivo de log "automacao_eventos.log" com os detalhes
# das execuções, erros e status do programa.
logging.basicConfig(
    filename='automacao_eventos.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ------------------------------------------------------------
# LISTAS DE TEMAS E PERGUNTAS
# ------------------------------------------------------------
# Cada tema será usado para gerar perguntas dinâmicas em inglês.
temas_en = [
    "technology", "health", "education", "sports", "politics", "economy",
    "science", "art", "music", "literature", "history", "geography",
    "philosophy", "psychology", "sociology", "anthropology", "astronomy",
    "biology", "chemistry", "physics", "mathematics", "engineering",
    "medicine", "law", "administration", "marketing", "finance",
    "architecture", "design", "fashion", "gastronomy"
]

perguntas_en = [
    "What is {tema}?", 
    "What are the latest news in {tema}?",
    "How does {tema} impact society?", 
    "What are the main challenges in {tema}?",
    "Who are the leading experts in {tema}?", 
    "How to make money with {tema}"
]


# ============================================================
# CLASSE: Automacao
# ------------------------------------------------------------
# Responsável por toda a lógica de execução da automação:
# - Abrir Edge
# - Fazer pesquisas
# - Salvar resultados
# - Fechar navegador
# ============================================================
class Automacao:
    def __init__(self):
        self.resultados = []

    # --------------------------------------------------------
    # Gera perguntas aleatórias a partir de um tema
    # --------------------------------------------------------
    def gerar_pesquisas_sobre_tema(self, tema, n):
        return random.sample([p.format(tema=tema) for p in perguntas_en], n)

    # --------------------------------------------------------
    # Salva resultados das pesquisas em CSV
    # --------------------------------------------------------
    def salvar_resultados(self):
        file_exists = os.path.isfile('resultados_pesquisas.csv')
        with open('resultados_pesquisas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Tema", "Pergunta", "Status"])
            for resultado in self.resultados:
                writer.writerow([resultado['tema'], resultado['pergunta'], resultado['status']])

    # --------------------------------------------------------
    # Testa a conectividade com a internet antes de iniciar
    # --------------------------------------------------------
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

    # --------------------------------------------------------
    # Função principal que executa toda a automação
    # --------------------------------------------------------
    async def executar_automacao(self, num_temas=1, num_perguntas=1):
        # Verifica se há internet
        if await self.verificar_conectividade():
            # Tenta abrir o Edge
            if self.abrir_edge():
                try:
                    # Executa as pesquisas
                    for _ in range(num_temas):
                        tema = random.choice(temas_en)
                        pesquisas = self.gerar_pesquisas_sobre_tema(tema, num_perguntas)
                        for pesquisa in pesquisas:
                            sucesso = await self.realizar_pesquisa(pesquisa)
                            self.resultados.append({
                                'tema': tema,
                                'pergunta': pesquisa,
                                'status': 'Concluída' if sucesso else 'Falha'
                            })
                            await asyncio.sleep(5)
                    # Salva no CSV após todas as pesquisas
                    self.salvar_resultados()
                    logging.info("Automação concluída com sucesso.")
                finally:
                    # Garante que o navegador será fechado no fim
                    self.fechar_edge()
            else:
                logging.error("Falha ao abrir o navegador.")
        else:
            logging.error("Falha na verificação de conectividade com a internet.")

    # --------------------------------------------------------
    # Abre o navegador Microsoft Edge
    # --------------------------------------------------------
    def abrir_edge(self):
        try:
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write('edge')
            pyautogui.press('enter')
            time.sleep(3)
            logging.info("Navegador Edge aberto com sucesso.")
            return True
        except Exception as e:
            logging.error(f"Erro ao abrir o Edge: {e}")
            return False

    # --------------------------------------------------------
    # Realiza uma pesquisa, repetindo até 3 tentativas se falhar
    # --------------------------------------------------------
    async def realizar_pesquisa(self, pesquisa):
        for tentativa in range(3):
            try:
                pyautogui.hotkey('ctrl', 't')      # abre nova aba
                pyautogui.write(pesquisa)           # digita a pesquisa
                pyautogui.press('enter')            # executa
                time.sleep(10)                      # aguarda carregamento
                pyautogui.hotkey('ctrl', 'w')       # fecha aba
                logging.info(f"Pesquisa realizada: {pesquisa}")
                return True
            except Exception as e:
                logging.error(f"Tentativa {tentativa + 1} falhou: {e}")
                if tentativa == 2:
                    logging.error(f"Falha após 3 tentativas: {pesquisa}")
                await asyncio.sleep(5)
        return False

    # --------------------------------------------------------
    # Fecha todas as janelas do Microsoft Edge
    # --------------------------------------------------------
    def fechar_edge(self):
        try:
            os.system("taskkill /IM msedge.exe /F")
            logging.info("Microsoft Edge fechado automaticamente.")
        except Exception as e:
            logging.error(f"Erro ao tentar fechar o Edge: {e}")


# ============================================================
# CLASSE: InterfaceGrafica
# ------------------------------------------------------------
# Define a interface Tkinter do programa (botões, campos e layout)
# ============================================================
class InterfaceGrafica:
    def __init__(self, automacao):
        self.automacao = automacao
        self.root = tk.Tk()
        self.root.title("Automação de Pesquisa")
        self.root.geometry('600x500')
        self.root.configure(bg='#cfffca')

        # Define o ícone da janela (opcional)
        icon_path = "Luffys_flag.ico"
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                logging.warning(f"Não foi possível aplicar o ícone: {e}")

        self.setup_ui()

    # --------------------------------------------------------
    # Configura o layout da interface (labels, botões, inputs)
    # --------------------------------------------------------
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Estilo dos botões
        style.configure('TButton', background='#A7D8D7', foreground='#2E4053', font=('Helvetica', 12, 'bold'))
        style.map('TButton', background=[('active', '#80C7C6')])
        style.configure('Red.TButton', background='#F28C8C', foreground='#2E4053', font=('Helvetica', 12, 'bold'))
        style.map('Red.TButton', background=[('active', '#F76C6C')])

        # Estilos de texto
        style.configure('TLabel', background='#F3F4F6', foreground='#2E4053', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12), padding=5)

        # Campo número de temas
        ttk.Label(self.root, text="Número de Temas:", style='TLabel').pack(pady=10)
        self.num_temas_entry = ttk.Entry(self.root, width=20)
        self.num_temas_entry.pack(pady=5)
        self.num_temas_entry.insert(0, "6")

        # Campo número de perguntas por tema
        ttk.Label(self.root, text="Número de Perguntas por Tema:", style='TLabel').pack(pady=10)
        self.num_perguntas_entry = ttk.Entry(self.root, width=20)
        self.num_perguntas_entry.pack(pady=5)
        self.num_perguntas_entry.insert(0, "6")

        # Botão para iniciar automação
        start_button = ttk.Button(self.root, text="Iniciar Automação", command=self.iniciar_automacao_handler)
        start_button.pack(pady=20)

        # Botão para fechar o app
        close_button = ttk.Button(self.root, text="Fechar", command=self.root.quit, style='Red.TButton')
        close_button.pack(pady=10)

    # --------------------------------------------------------
    # Captura os valores e inicia a automação em nova thread
    # --------------------------------------------------------
    def iniciar_automacao_handler(self):
        try:
            num_temas = int(self.num_temas_entry.get())
            num_perguntas = int(self.num_perguntas_entry.get())
            threading.Thread(target=self.run_automacao, args=(num_temas, num_perguntas)).start()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos.")

    # --------------------------------------------------------
    # Executa a automação de forma assíncrona
    # --------------------------------------------------------
    def run_automacao(self, num_temas, num_perguntas):
        asyncio.run(self.automacao.executar_automacao(num_temas, num_perguntas))

    # --------------------------------------------------------
    # Inicia o loop principal da interface
    # --------------------------------------------------------
    def run(self):
        self.root.mainloop()


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================
if __name__ == "__main__":
    automacao = Automacao()
    interface = InterfaceGrafica(automacao)
    interface.run()
