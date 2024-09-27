import time
import pyautogui
import random
import logging
import requests

# Configuração de logging
logging.basicConfig(filename='automacao_pesquisa.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# Listas de temas em diferentes idiomas
temas_pt = [
    "tecnologia", "saúde", "educação", "esportes", "política", "economia", 
    "ciência", "arte", "música", "literatura", "história", "geografia", 
    "filosofia", "psicologia", "sociologia", "antropologia", "astronomia", 
    "biologia", "química", "física", "matemática", "engenharia", "medicina", 
    "direito", "administração", "marketing", "finanças", "arquitetura", 
    "design", "moda", "gastronomia"
]

temas_en = [
    "technology", "health", "education", "sports", "politics", "economy", 
    "science", "art", "music", "literature", "history", "geography", 
    "philosophy", "psychology", "sociology", "anthropology", "astronomy", 
    "biology", "chemistry", "physics", "mathematics", "engineering", "medicine", 
    "law", "administration", "marketing", "finance", "architecture", 
    "design", "fashion", "gastronomy"
]

# Lista de perguntas em português
perguntas_pt = [
    "O que é {tema}?", "Quais são as últimas novidades em {tema}?", "Como {tema} impacta a sociedade?",
    "Quais são os principais desafios em {tema}?", "Quem são os principais especialistas em {tema}?",
    # Adicione mais perguntas aqui até ter 200
]

# Lista de perguntas em inglês
perguntas_en = [
    "What is {tema}?", "What are the latest news in {tema}?", "How does {tema} impact society?",
    "What are the main challenges in {tema}?", "Who are the leading experts in {tema}?",
    # Adicione mais perguntas aqui até ter 200
]

# Função para gerar uma lista de pesquisas aleatórias sobre um tema
def gerar_pesquisas_sobre_tema(tema, n, idioma):
    if idioma == 'pt':
        perguntas = perguntas_pt
    else:
        perguntas = perguntas_en
    return random.sample([p.format(tema=tema) for p in perguntas], n)

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
        time.sleep(10)  # Tempo para carregar a página e permanecer nela
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

# Função para exibir o menu de seleção de idioma
def selecionar_idioma():
    resposta = pyautogui.confirm('Escolha o idioma para as pesquisas:', buttons=['Português', 'English'])
    if resposta == 'Português':
        return 'pt', temas_pt
    else:
        return 'en', temas_en

# Função para exibir o menu de seleção de tema em três colunas
def selecionar_tema(temas):
    temas_divididos = [temas[i:i + 10] for i in range(0, len(temas), 10)]
    temas_formatados = [", ".join(coluna) for coluna in zip(*temas_divididos)]
    resposta = pyautogui.confirm('Escolha um tema:', buttons=temas_formatados)
    return resposta.split(", ")[0]

# Função principal para executar a automação
def executar_automacao(num_pesquisas=5):
    while True:
        # Selecionar o idioma
        idioma, temas = selecionar_idioma()
        
        # Perguntar ao usuário se deseja realizar a pesquisa
        resposta = pyautogui.confirm('Você deseja realizar a pesquisa?', buttons=['Sim', 'Não'])
        
        if resposta == 'Sim':
            # Selecionar o tema
            tema = selecionar_tema(temas)
            
            # Alerta inicial
            pyautogui.alert('O código de automação de pesquisa no Edge vai começar....')
            pyautogui.PAUSE = 0.5

            # Verificar conectividade com a internet
            if verificar_conectividade():
                # Abrindo o Edge uma vez
                if abrir_edge():
                    # Gerar pesquisas sobre o tema selecionado
                    pesquisas = gerar_pesquisas_sobre_tema(tema, num_pesquisas, idioma)
                    
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
            
            # Perguntar se deseja escolher outro tema
            nova_pesquisa = pyautogui.confirm('Você deseja escolher outro tema?', buttons=['Sim', 'Não'])
            if nova_pesquisa == 'Não':
                break
        else:
            pyautogui.alert("O programa está fechando.")
            logging.info("O usuário optou por não realizar a pesquisa. O programa está fechando.")
            break

# Executar a automação com parâmetros configuráveis
executar_automacao(num_pesquisas=5)
