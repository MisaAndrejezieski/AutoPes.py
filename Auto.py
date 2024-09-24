import time
import pyautogui
import random
import logging
import requests

# Configuração de logging
logging.basicConfig(filename='automacao_pesquisa.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Lista de possíveis temas para as pesquisas
temas = [
    "tecnologia", "saúde", "educação", "esportes", "política", "economia", 
    "ciência", "arte", "música", "literatura", "história", "geografia", 
    "filosofia", "psicologia", "sociologia", "antropologia", "astronomia", 
    "biologia", "química", "física", "matemática", "engenharia", "medicina", 
    "direito", "administração", "marketing", "finanças", "arquitetura", 
    "design", "moda", "gastronomia"
]

# Função para gerar uma lista de pesquisas aleatórias sobre um tema
def gerar_pesquisas_sobre_tema(tema, n):
    perguntas = [
        f"O que é {tema}?",
        f"Quais são as últimas novidades em {tema}?",
        f"Como {tema} impacta a sociedade?",
        f"Quais são os principais desafios em {tema}?",
        f"Quem são os principais especialistas em {tema}?"
    ]
    return perguntas[:n]

# Função para abrir o Edge
def abrir_edge():
    try:
        pyautogui.press('win')
        pyautogui.write('edge')
        pyautogui.press('enter')
        time.sleep(2)  # Aumentar o tempo para garantir que o navegador abra
        logging.info("Navegador Edge aberto com sucesso.")
        return True
    except Exception as e:
        logging.error(f"Erro ao abrir o Edge: {e}")
        pyautogui.alert(f"Erro ao abrir o Edge: {e}")
        return False

# Função para realizar uma pesquisa
def realizar_pesquisa(pesquisa):
    try:
        pyautogui.hotkey('ctrl', 't')  # Abrir uma nova aba
        pyautogui.write(pesquisa)
        pyautogui.press('enter')
        time.sleep(2)  # Tempo para carregar a página
        pyautogui.hotkey('ctrl', 'w')  # Fechar a aba após a pesquisa
        logging.info(f"Pesquisa realizada: {pesquisa}")
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")
        pyautogui.alert(f"Erro ao realizar a pesquisa: {e}")

# Função para limpar dados de navegação e cookies
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

# Função para fechar o navegador
def fechar_navegador():
    try:
        pyautogui.hotkey('alt', 'f4')
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
def executar_automacao(num_temas=2, num_pesquisas=5):
    # Alerta inicial
    pyautogui.alert('O código de automação de pesquisa no Edge vai começar....')
    pyautogui.PAUSE = 0.5

    # Verificar conectividade com a internet
    if verificar_conectividade():
        # Abrindo o Edge uma vez
        if abrir_edge():
            # Iniciando o laço de repetição para os temas diferentes
            for _ in range(num_temas):
                tema = random.choice(temas)
                pesquisas = gerar_pesquisas_sobre_tema(tema, num_pesquisas)
                
                for pesquisa in pesquisas:
                    realizar_pesquisa(pesquisa)
            
            # Limpar dados de navegação e cookies
            limpar_dados_navegacao()
            
            # Fechar o navegador
            fechar_navegador()
        else:
            pyautogui.alert("Não foi possível abrir o navegador Edge.")
    else:
        pyautogui.alert("Não foi possível verificar a conectividade com a internet.")

# Executar a automação com parâmetros configuráveis
executar_automacao(num_temas=2, num_pesquisas=5)
