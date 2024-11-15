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
import speedtest  # Correção na importação do módulo correto

# Configuração de logging
logging.basicConfig(
    filename='automacao_eventos.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Log de erros específicos
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
    with open('resultados_pesquisas.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.stat('resultados_pesquisas.csv').st_size == 0:
            writer.writerow(["Tema", "Pergunta", "Status"])
        for resultado in resultados:
            writer.writerow([resultado['tema'], resultado['pergunta'], resultado['status']])

# Função para fechar o navegador Edge
def fechar_edge():
    try:
        pyautogui.hotkey('ctrl', 'w')  # Fecha a aba atual do navegador
        time.sleep(1)  # Aguarda um pouco
        logging.info("Navegador Edge fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o Edge: {e}")

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

# Função para medir a velocidade de internet
def medir_velocidade_internet():
    st = speedtest.Speedtest()  # Usando o método correto do speedtest-cli
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convertendo para Mbps
    upload_speed = st.upload() / 1_000_000  # Convertendo para Mbps
    ping = st.results.ping
    logging.info(f"Velocidade de download: {download_speed:.2f} Mbps, upload: {upload_speed:.2f} Mbps, ping: {ping} ms.")
    return download_speed, upload_speed

# Função para executar a automação
async def executar_automacao(num_temas=6, num_perguntas=6):
    resultados = []
    download_speed, _ = medir_velocidade_internet()  # Medindo a velocidade de download

    intervalo = max(10, 60 / download_speed)  # Ajusta o intervalo de acordo com a velocidade de download

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
        fechar_edge()  # Fechar o navegador após a execução
    else:
        logging.error("Falha ao abrir o navegador.")

# Função para rodar a automação em segundo plano
def iniciar_automacao_bg(num_temas, num_perguntas):
    asyncio.run(executar_automacao(num_temas, num_perguntas))

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
    ttk.Label(root, text="Número de Temas:").pack(pady=5)
    num_temas_entry = ttk.Entry(root)
    num_temas_entry.pack(pady=5)

    ttk.Label(root, text="Número de Perguntas:").pack(pady=5)
    num_perguntas_entry = ttk.Entry(root)
    num_perguntas_entry.pack(pady=5)

    # Exibir a velocidade da internet
    ttk.Label(root, text="Velocidade da Internet:").pack(pady=5)
    velocidade_label = ttk.Label(root, text="Calculando...", font=('Helvetica', 12))
    velocidade_label.pack(pady=5)

    def atualizar_velocidade():
        download_speed, _ = medir_velocidade_internet()
        velocidade_label.config(text=f"Velocidade: {download_speed:.2f} Mbps")
        root.after(5000, atualizar_velocidade)  # Atualiza a cada 5 segundos

    # Iniciar a atualização da velocidade
    atualizar_velocidade()

    # Função de iniciar a automação
    def iniciar_automacao_handler():
        try:
            num_temas = int(num_temas_entry.get())
            num_perguntas = int(num_perguntas_entry.get())
            threading.Thread(target=iniciar_automacao_bg, args=(num_temas, num_perguntas)).start()
            messagebox.showinfo("Sucesso", "Automação iniciada com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos!")

    # Botões
    ttk.Button(root, text="Iniciar Automação", command=iniciar_automacao_handler).pack(pady=20)
    ttk.Button(root, text="Fechar", style='Red.TButton', command=root.quit).pack(pady=5)

    root.mainloop()

# Iniciar a interface gráfica
iniciar_interface()
