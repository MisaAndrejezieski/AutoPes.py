"""
Automação de pesquisas com interface Tkinter - versão final com webdriver-manager

Requisitos:
- pip install selenium webdriver-manager requests
"""

import logging
import os
import csv
import threading
import time
import random
import requests
import urllib.parse
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# ---------- Logging configuration ----------
logging.basicConfig(
    filename='automacao_eventos.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ---------- Data (temas e perguntas) ----------
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
    "Who are the leading experts in {tema}?", "How to make money with {tema}?"
]

# ---------- Automacao class ----------
class Automacao:
    def __init__(self, headless=False, cancel_event=None, progress_callback=None):
        """
        headless: se True, roda o Edge em modo headless (sem janela)
        cancel_event: threading.Event para permitir cancelamento
        progress_callback: função (atual, total) para atualizar progresso na GUI
        """
        self.headless = headless
        self.cancel_event = cancel_event or threading.Event()
        self.progress_callback = progress_callback
        self.resultados = []

    def _criar_driver(self):
        """Cria e retorna uma instância do WebDriver do Edge com webdriver-manager."""
        options = Options()
        if self.headless:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--start-maximized')

        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
            driver.set_page_load_timeout(30)
            logging.info("WebDriver do Edge inicializado com sucesso via webdriver-manager.")
            return driver
        except WebDriverException as e:
            logging.exception("Erro ao inicializar o WebDriver do Edge.")
            raise RuntimeError("Falha ao iniciar o Edge WebDriver. Verifique conexão e permissões.") from e

    def gerar_pesquisas_sobre_tema(self, tema, n):
        perguntas = [p.format(tema=tema) for p in perguntas_en]
        if n >= len(perguntas):
            return perguntas[:]
        return random.sample(perguntas, n)

    def salvar_resultados(self):
        file_exists = os.path.isfile('resultados_pesquisas.csv')
        with open('resultados_pesquisas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Tema", "Pergunta", "Status", "Tentativas"])
            for resultado in self.resultados:
                writer.writerow([
                    resultado['timestamp'],
                    resultado['tema'],
                    resultado['pergunta'],
                    resultado['status'],
                    resultado.get('tentativas', '')
                ])

    def verificar_conectividade(self):
        endpoints = ['https://www.google.com', 'https://www.bing.com', 'https://www.duckduckgo.com']
        for url in endpoints:
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    logging.info(f"Conectividade com {url} verificada.")
                    return True
            except requests.RequestException:
                logging.warning(f"Falha ao acessar {url}. Tentando outro...")
        return False

    def realizar_pesquisa(self, driver, pesquisa, max_tentativas=3):
        """
        Realiza a pesquisa usando Selenium (navega diretamente para o Bing).
        Retorna (sucesso: bool, tentativas: int).
        """
        encoded = urllib.parse.quote_plus(pesquisa)
        search_url = f"https://www.bing.com/search?q={encoded}"
        for tentativa in range(1, max_tentativas + 1):
            if self.cancel_event.is_set():
                logging.info("Cancelamento solicitado. Abortando pesquisa.")
                return False, tentativa - 1
            try:
                driver.get(search_url)
                WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
                logging.info(f"Pesquisa realizada com sucesso: {pesquisa} (tentativa {tentativa})")
                return True, tentativa
            except TimeoutException as e:
                logging.warning(f"Timeout na pesquisa '{pesquisa}' (tentativa {tentativa}): {e}")
            except WebDriverException as e:
                logging.error(f"Erro WebDriver na pesquisa '{pesquisa}' (tentativa {tentativa}): {e}")
            time.sleep(2)
        logging.error(f"Falha ao realizar a pesquisa: {pesquisa} após {max_tentativas} tentativas.")
        return False, max_tentativas

    def executar_automacao(self, num_temas=6, num_perguntas=6):
        """Fluxo principal de execução (síncrono)."""
        logging.info("Iniciando verificação de conectividade...")
        if not self.verificar_conectividade():
            logging.error("Sem conectividade com a internet. Abortando.")
            raise RuntimeError("Sem conectividade com a internet.")

        driver = None
        try:
            driver = self._criar_driver()

            total_tasks = num_temas * num_perguntas
            completed = 0

            for _ in range(num_temas):
                if self.cancel_event.is_set():
                    logging.info("Cancelamento solicitado; interrompendo execução.")
                    break
                tema = random.choice(temas_en)
                pesquisas = self.gerar_pesquisas_sobre_tema(tema, num_perguntas)
                for pesquisa in pesquisas:
                    if self.cancel_event.is_set():
                        break
                    sucesso, tentativas = self.realizar_pesquisa(driver, pesquisa)
                    self.resultados.append({
                        'timestamp': datetime.utcnow().isoformat(),
                        'tema': tema,
                        'pergunta': pesquisa,
                        'status': 'Concluída' if sucesso else 'Falha',
                        'tentativas': tentativas
                    })
                    completed += 1
                    if self.progress_callback:
                        try:
                            self.progress_callback(completed, total_tasks)
                        except Exception:
                            logging.exception("Erro ao chamar progress_callback.")
                    time.sleep(1)
            self.salvar_resultados()
            logging.info("Automação finalizada (normal).")
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    logging.exception("Erro ao fechar o WebDriver.")
        return self.resultados

# ---------- Interface Grafica ----------
class InterfaceGrafica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automação de Pesquisa (Selenium + WebDriver Manager)")
        self.root.geometry('640x420')
        self.root.configure(bg='#cfffca')
        self.cancel_event = threading.Event()
        self.thread = None
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 11, 'bold'))
        style.configure('TLabel', font=('Helvetica', 11))
        style.configure('TEntry', font=('Helvetica', 11))

        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Número de Temas:").grid(row=0, column=0, sticky='w')
        self.num_temas_entry = ttk.Entry(frame, width=10)
        self.num_temas_entry.grid(row=0, column=1, pady=6, sticky='w')
        self.num_temas_entry.insert(0, "6")

        ttk.Label(frame, text="Número de Perguntas por Tema:").grid(row=1, column=0, sticky='w')
        self.num_perguntas_entry = ttk.Entry(frame, width=10)
        self.num_perguntas_entry.grid(row=1, column=1, pady=6, sticky='w')
        self.num_perguntas_entry.insert(0, "6")

        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Headless (sem interface)", variable=self.headless_var).grid(row=2, column=0, columnspan=2, sticky='w')

        start_button = ttk.Button(frame, text="Iniciar Automação", command=self.iniciar_automacao_handler)
        start_button.grid(row=3, column=0, pady=12)

        cancel_button = ttk.Button(frame, text="Cancelar", command=self.cancelar_automacao)
        cancel_button.grid(row=3, column=1, pady=12)

        ttk.Button(frame, text="Fechar", command=self.root.quit).grid(row=3, column=2, pady=12)

        ttk.Label(frame, text="Progresso:").grid(row=4, column=0, sticky='w', pady=(8,0))
        self.progress = ttk.Progressbar(frame, orient='horizontal', length=400, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=6)

        self.status_label = ttk.Label(frame, text="Status: Aguardando início")
        self.status_label.grid(row=6, column=0, columnspan=3, sticky='w', pady=(6,0))

    def iniciar_automacao_handler(self):
        try:
            num_temas = int(self.num_temas_entry.get())
            num_perguntas = int(self.num_perguntas_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos para temas e perguntas.")
            return

        self.cancel_event.clear()
        total = num_temas * num_perguntas
        self.progress['maximum'] = total
        self.progress['value'] = 0
        self.status_label.config(text="Status: Inicializando...")

        headless = bool(self.headless_var.get())
        automacao = Automacao(headless=headless, cancel_event=self.cancel_event, progress_callback=self.atualizar_progresso)

        def target():
            try:
                resultados = automacao.executar_automacao(num_temas=num_temas, num_perguntas=num_perguntas)
                if self.cancel_event.is_set():
                    self.status_label.config(text="Status: Cancelado pelo usuário.")
                    logging.info("Execução cancelada pelo usuário.")
                else:
                    self.status_label.config(text="Status: Concluído com sucesso.")
                    logging.info("Execução concluída; resultados salvos.")
                    messagebox.showinfo("Concluído", f"Automação concluída. {len(resultados)} pesquisas processadas.\nResultados em 'resultados_pesquisas.csv'.")
            except RuntimeError as re:
                logging.exception("Erro durante a execução da automação.")
                self.status_label.config(text=f"Status: Erro - {re}")
                messagebox.showerror("Erro", f"Erro: {re}")
            except WebDriverException as we:
                logging.exception("Erro com o WebDriver.")
                self.status_label.config(text=f"Status: Erro ao iniciar o WebDriver.")
                messagebox.showerror("Erro WebDriver", "Falha ao inicializar o WebDriver do Edge.")
            except Exception as e:
                logging.exception("Erro inesperado na thread da automação.")
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
            finally:
                try:
                    self.progress['value'] = self.progress['maximum']
                except Exception:
                    pass

        self.thread = threading.Thread(target=target, daemon=True)
        self.thread.start()
        self.status_label.config(text="Status: Em execução...")

    def atualizar_progresso(self, atual, total):
        def _update():
            self.progress['value'] = atual
            self.status_label.config(text=f"Status: Em execução... ({atual}/{total})")
        self.root.after(0, _update)

    def cancelar_automacao(self):
        if messagebox.askyesno("Cancelar", "Deseja cancelar a automação em execução?"):
            self.cancel_event.set()
            self.status_label.config(text="Status: Cancelamento solicitado...")

    def run(self):
        self.root.mainloop()

# ---------- Main ----------
if __name__ == "__main__":
    app = InterfaceGrafica()
    app.run()
