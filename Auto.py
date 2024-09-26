import time
import pyautogui
import random
import logging
import requests

# Configuração de logging
logging.basicConfig(filename='automacao_pesquisa.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Lista de possíveis temas para as pesquisas
themes = [
    "technology", "health", "education", "sports", "politics", "economy", 
    "science", "art", "music", "literature", "history", "geography", 
    "philosophy", "psychology", "sociology", "anthropology", "astronomy", 
    "biology", "chemistry", "physics", "mathematics", "engineering", "medicine", 
    "law", "administration", "marketing", "finance", "architecture", 
    "design", "fashion", "gastronomy"
]

# Função para gerar uma lista de pesquisas aleatórias sobre um tema
def generate_searches_about_theme(theme, n):
    questions = [
        f"What is {theme}?",
        f"What are the latest news in {theme}?",
        f"How does {theme} impact society?",
        f"What are the main challenges in {theme}?",
        f"Who are the leading experts in {theme}?"
    ]
    return questions[:n]

# Função para abrir o Edge
def open_edge():
    try:
        pyautogui.press('win')
        pyautogui.write('edge')
        pyautogui.press('enter')
        time.sleep(2)  # Aumentar o tempo para garantir que o navegador abra
        logging.info("Edge browser opened successfully.")
        return True
    except Exception as e:
        logging.error(f"Error opening Edge: {e}")
        pyautogui.alert(f"Error opening Edge: {e}")
        return False

# Função para realizar uma pesquisa
def perform_search(search):
    try:
        pyautogui.hotkey('ctrl', 't')  # Abrir uma nova aba
        pyautogui.write(search)
        pyautogui.press('enter')
        time.sleep(10)  # Tempo para carregar a página e permanecer nela
        pyautogui.hotkey('ctrl', 'w')  # Fechar a aba após a pesquisa
        logging.info(f"Search performed: {search}")
    except Exception as e:
        logging.error(f"Error performing search: {e}")
        pyautogui.alert(f"Error performing search: {e}")

# Função para limpar dados de navegação e cookies
def clear_browsing_data():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)  # Tempo para abrir a janela de limpeza de dados
        pyautogui.press('enter')  # Confirmar a limpeza dos dados
        time.sleep(2)  # Tempo para concluir a limpeza
        pyautogui.alert("Browsing data and cookies cleared successfully.")
    except Exception as e:
        logging.error(f"Error clearing browsing data: {e}")
        pyautogui.alert(f"Error clearing browsing data: {e}")

# Função para fechar o navegador
def close_browser():
    try:
        pyautogui.hotkey('alt', 'f4')
        logging.info("Browser closed successfully.")
    except Exception as e:
        logging.error(f"Error closing browser: {e}")
        pyautogui.alert(f"Error closing browser: {e}")

# Função para verificar a conectividade com a internet
def check_connectivity():
    try:
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            logging.info("Internet connectivity verified.")
            return True
        else:
            logging.error("Failed to verify internet connectivity.")
            return False
    except requests.ConnectionError as e:
        logging.error(f"Error verifying internet connectivity: {e}")
        pyautogui.alert(f"Error verifying internet connectivity: {e}")
        return False

# Função principal para executar a automação
def execute_automation(num_themes=7, num_searches=5):
    # Perguntar ao usuário se deseja realizar a pesquisa
    response = pyautogui.confirm('Do you want to perform the search?', buttons=['Yes', 'No'])
    
    if response == 'Yes':
        # Alerta inicial
        pyautogui.alert('The search automation code in Edge will start now....')
        pyautogui.PAUSE = 0.5

        # Verificar conectividade com a internet
        if check_connectivity():
            # Abrindo o Edge uma vez
            if open_edge():
                # Iniciando o laço de repetição para os temas diferentes
                for _ in range(num_themes):
                    theme = random.choice(themes)
                    searches = generate_searches_about_theme(theme, num_searches)
                    
                    for search in searches:
                        perform_search(search)
                
                # Limpar dados de navegação e cookies
                clear_browsing_data()
                
                # Fechar o navegador
                close_browser()
            else:
                pyautogui.alert("Could not open Edge browser.")
        else:
            pyautogui.alert("Could not verify internet connectivity.")
    else:
        pyautogui.alert("The program is closing.")
        logging.info("User opted not to perform the search. The program is closing.")

# Executar a automação com parâmetros configuráveis
execute_automation(num_themes=7, num_searches=5)
