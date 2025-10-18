import os
import time
import requests
from tkinter import messagebox, ttk
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException

# ======================
# CONFIGURAÇÃO DO DRIVER
# ======================

def abrir_navegador():
    """Inicializa o navegador Microsoft Edge usando o driver local."""
    try:
        driver_path = os.path.join(os.getcwd(), "drivers", "msedgedriver.exe")
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"Driver Edge não encontrado em: {driver_path}")

        options = Options()
        options.add_argument("--start-maximized")
        # Caso queira rodar sem abrir a janela:
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")

        service = Service(driver_path)
        driver = webdriver.Edge(service=service, options=options)
        return driver
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao abrir o Edge:\n{e}")
        return None


# ======================
# FUNÇÕES PRINCIPAIS
# ======================

def verificar_conexao():
    """Verifica se há conexão com a internet."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def iniciar_automacao():
    """Função principal que é chamada ao clicar no botão Iniciar."""
    if not verificar_conexao():
        messagebox.showerror("Erro", "Sem conexão com a internet.")
        return

    driver = abrir_navegador()
    if not driver:
        return

    try:
        # Exemplo de navegação - substitua pelo site desejado
        driver.get("https://www.bing.com")

        time.sleep(3)

        # Exemplo de interação
        caixa_busca = driver.find_element("name", "q")
        caixa_busca.send_keys("Selenium WebDriver Edge Python")
        caixa_busca.submit()

        time.sleep(5)
        messagebox.showinfo("Sucesso", "Automação concluída com sucesso!")

    except NoSuchElementException as e:
        messagebox.showerror("Erro", f"Elemento não encontrado:\n{e}")
    except WebDriverException as e:
        messagebox.showerror("Erro no WebDriver", f"Ocorreu um erro:\n{e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado:\n{e}")
    finally:
        driver.quit()


# ======================
# INTERFACE GRÁFICA (Tkinter)
# ======================

def criar_interface():
    """Cria a janela principal da aplicação."""
    janela = tk.Tk()
    janela.title("AutoPes - Automação Edge")
    janela.geometry("400x250")
    janela.resizable(False, False)

    estilo = ttk.Style()
    estilo.configure("TButton", font=("Segoe UI", 11))
    estilo.configure("TLabel", font=("Segoe UI", 11))

    frame = ttk.Frame(janela, padding=20)
    frame.pack(expand=True, fill="both")

    label = ttk.Label(frame, text="Clique para iniciar a automação:")
    label.pack(pady=10)

    botao_iniciar = ttk.Button(frame, text="Iniciar Automação", command=iniciar_automacao)
    botao_iniciar.pack(pady=10)

    botao_sair = ttk.Button(frame, text="Sair", command=janela.destroy)
    botao_sair.pack(pady=10)

    janela.mainloop()


# ======================
# EXECUÇÃO PRINCIPAL
# ======================

if __name__ == "__main__":
    criar_interface()
