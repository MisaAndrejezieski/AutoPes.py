import time
import pyautogui
import random
import requests

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
]

# Função para gerar uma lista de pesquisas aleatórias sobre um tema
def gerar_pesquisas_sobre_tema(tema, n):
    n = min(n, len(perguntas_en))  # Garante que n não seja maior que o número de perguntas disponíveis
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
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")

# Função para limpar dados de navegação e cookies
def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        logging.info("Dados de navegação e cookies limpos com sucesso.")
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

# Função principal para executar a automação
def executar_automacao(num_temas=6, num_perguntas=5):
    pyautogui.alert("A automação de pesquisa no Edge está começando...")
    logging.info("O código de automação de pesquisa no Edge vai começar....")

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
                logging.error("Não foi possível abrir o navegador Edge.")
    else:
        logging.error("Não foi possível verificar a conectividade com a internet.")
    logging.info("O programa está concluído.")
    pyautogui.alert("A automação de pesquisa no Edge foi concluída.")
