import time
import pyautogui
import random
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração de logging
logging.basicConfig(filename='automacao_pesquisa.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

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
    "What are the main challenges in {tema}?", "Who are the leading experts in {tema}?",
    # Adicione mais perguntas aqui até ter 200
]

# Função para gerar uma lista de pesquisas aleatórias sobre um tema
def gerar_pesquisas_sobre_tema(tema, n):
    return random.sample([p.format(tema=tema) for p in perguntas_en], n)

# Função para abrir o navegador usando Selenium
def abrir_navegador():
    try:
        driver = webdriver.Edge()  # Inicializa o navegador Edge
        driver.maximize_window()  # Maximiza a janela do navegador
        logging.info("Navegador Edge aberto com sucesso.")
        return driver
    except Exception as e:
        logging.error(f"Erro ao abrir o Edge: {e}")
        pyautogui.alert(f"Erro ao abrir o Edge: {e}")
        return None

# Função para realizar uma pesquisa usando Selenium
def realizar_pesquisa(driver, pesquisa):
    try:
        driver.get("https://www.google.com")  # Abre o Google
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )  # Espera até que a caixa de pesquisa esteja presente
        search_box.send_keys(pesquisa)  # Digita a pesquisa na caixa de pesquisa
        search_box.submit()  # Submete a pesquisa
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )  # Espera até que os resultados da pesquisa estejam presentes
        logging.info(f"Pesquisa realizada: {pesquisa}")
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")
        pyautogui.alert(f"Erro ao realizar a pesquisa: {e}")

# Função para limpar dados de navegação e cookies usando PyAutoGUI
def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)  # Tempo para abrir a janela de limpeza de dados
        pyautogui.press('enter')  # Confirmar a limpeza dos dados
        time.sleep(2)  # Tempo para concluir a limpeza
        pyautogui.alert("Dados de navegação e cookies limpos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar os dados de navegação: {e}")
        pyautogui.alert(f"Erro ao limpar os dados de navegação: {e}")

# Função para fechar o navegador usando Selenium
def fechar_navegador(driver):
    try:
        driver.quit()  # Fecha o navegador
        logging.info("Navegador fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")
        pyautogui.alert(f"Erro ao fechar o navegador: {e}")

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
        pyautogui.alert(f"Erro ao verificar a conectividade com a internet: {e}")
        return False

# Função principal para executar a automação
def executar_automacao(num_temas=6, num_perguntas=5):
    while True:
        # Perguntar ao usuário se deseja realizar a pesquisa
        resposta = pyautogui.confirm('Você deseja realizar a pesquisa?', buttons=['Sim', 'Não'])
        
        if resposta == 'Sim':
            # Alerta inicial
            pyautogui.alert('O código de automação de pesquisa no Edge vai começar....')
            pyautogui.PAUSE = 0.5  # Define um pequeno intervalo entre as ações do PyAutoGUI

            # Verificar conectividade com a internet
            if verificar_conectividade():
                for _ in range(num_temas):  # Repete o processo para o número de temas especificado
                    tema = random.choice(temas_en)  # Escolhe um tema aleatoriamente
                    pesquisas = gerar_pesquisas_sobre_tema(tema, num_perguntas)  # Gera uma lista de pesquisas sobre o tema
                    
                    driver = abrir_navegador()  # Tenta abrir o navegador Edge
                    if driver:
                        for pesquisa in pesquisas:  # Realiza cada pesquisa gerada
                            realizar_pesquisa(driver, pesquisa)
                        
                        limpar_dados_navegacao()  # Limpa os dados de navegação e cookies
                        fechar_navegador(driver)  # Fecha o navegador
                    else:
                        pyautogui.alert("Não foi possível abrir o navegador Edge.")
            else:
                pyautogui.alert("Não foi possível verificar a conectividade com a internet.")
            
            # Perguntar se deseja realizar outra pesquisa
            nova_pesquisa = pyautogui.confirm('Você deseja realizar outra pesquisa?', buttons=['Sim', 'Não'])
            if nova_pesquisa == 'Não':
                break  # Sai do loop se o usuário não quiser realizar outra pesquisa
        else:
            pyautogui.alert("O programa está fechando.")  # Exibe um alerta indicando que o programa está fechando
            logging.info("O usuário optou por não realizar a pesquisa. O programa está fechando.")  # Registra no log que o programa está fechando
            break  # Sai do loop

# Executar a automação com parâmetros configuráveis
executar_automacao(num_temas=6, num_perguntas=5)  # Executa a automação com 6 temas e 5 perguntas por tema
