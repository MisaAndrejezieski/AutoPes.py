import time
import pyautogui
import random
import logging
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importa ttk para estilos modernos
from PIL import Image, ImageTk  # Importa PIL para trabalhar com imagens

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
    "What are the main challenges in {tema}?", "Who are the leading experts in {tema}?", "how to make money with {tema}"
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
        with open('automacao_pesquisa.log', 'a') as log_file:
            log_file.write(f"Pesquisa realizada: {pesquisa}\n")
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")

# Função para limpar dados de navegação e cookies
def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        logging.info("Dados de navegação limpos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar os dados de navegação: {e}")

# Função para fechar o navegador
def fechar_navegador():
    try:
        pyautogui.hotkey('alt', 'f4')
        logging.info("Navegador fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")

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
        return False

# Função para agendar a automação
def agendar_automacao(hora, minuto):
    agora = datetime.datetime.now()
    horario_agendado = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)

    if horario_agendado < agora:
        horario_agendado += datetime.timedelta(days=1)

    tempo_espera = (horario_agendado - agora).total_seconds()
    scheduler.enter(tempo_espera, 1, executar_automacao)
    logging.info(f"Automação agendada para: {horario_agendado}")

# Função para criar a interface gráfica
def criar_interface_grafica():
    scheduler = sched.scheduler(time.time, time.sleep)

    def executar_automacao():
        if not verificar_conectividade():
            messagebox.showerror("Erro", "Não foi possível verificar a conectividade com a internet.")
            return
        
        pyautogui.PAUSE = 0.5
        num_temas = int(temas_var.get())
        num_perguntas = int(perguntas_var.get())
        
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
    
    def executar_automacao_agendada():
        hora = int(entry_hora.get())
        minuto = int(entry_minuto.get())
        agendar_automacao(hora, minuto)
        scheduler.run(blocking=False)

    def fechar_programa():
        root.destroy()
    
    # Criação da janela principal
    root = tk.Tk()
    root.title("Automação de Pesquisas")
    root.geometry("400x500")
    root.configure(bg='#2E4053')  # Fundo azul escuro

    # Adiciona o ícone do programa
    root.iconbitmap('22287dragon_98813.ico')

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), background='#2E4053', foreground='white')
    style.configure("TButton", font=("Helvetica", 12), background='#AED6F1', foreground='black')
    style.configure("TEntry", font=("Helvetica", 12))

    # Carregar e exibir imagem
    image = Image.open('22287dragon_98813.png')
    photo = ImageTk.PhotoImage(image)
    label_image = tk.Label(root, image=photo, bg='#2E4053')
    label_image.image = photo
    label_image.pack(pady=10)

    # Criação dos widgets
    label_temas = ttk.Label(root, text="Número de Temas:")
    label_temas.pack(pady=10)
    temas_var = tk.StringVar(value='6')
    entry_temas = ttk.Entry(root, textvariable=temas_var)
    entry_temas.pack(pady=10)

    label_perguntas = ttk.Label(root, text="Número de Perguntas por Tema:")
    label_perguntas.pack(pady=10)
    perguntas_var = tk.StringVar(value='6')
    entry_perguntas = ttk.Entry(root, textvariable=perguntas_var)
    entry_perguntas.pack(pady=10)

    # Widgets de agendamento
    label_hora = ttk.Label(root, text="Hora de Início:")
    label_hora.pack(pady=5)
    entry_hora = ttk.Entry(root)
    entry_hora.pack(pady=5)
    
    label_minuto = ttk.Label(root, text="Minuto de Início:")
    label_minuto.pack(pady=5)
    entry_minuto = ttk.Entry(root)
    entry_minuto.pack(pady=5)

    button_agendar = ttk.Button(root, text="Agendar Automação", command=executar_automacao_agendada)
    button_agendar.pack(pady=10)

    button_iniciar = ttk.Button(root, text="Iniciar Automação", command=executar_automacao)
    button_iniciar.pack(pady=10)
    
    button_fechar = ttk.Button(root, text="Fechar Programa", command=fechar_programa)
    button_fechar.pack(pady=10)

    # Iniciar o loop da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    criar_interface_grafica()

