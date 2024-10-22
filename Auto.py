import time  # Importa o módulo time para manipulação de tempo
import pyautogui  # Importa o módulo pyautogui para automação de GUI
import random  # Importa o módulo random para gerar valores aleatórios
import logging  # Importa o módulo logging para registrar logs
import requests  # Importa o módulo requests para fazer requisições HTTP

# Configuração de logging
logging.basicConfig(
    filename='automacao_pesquisa.log',  # Nome do arquivo de log
    level=logging.INFO,  # Nível de log (INFO)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem de log
    encoding='utf-8'  # Codificação do arquivo de log
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
    "What are the main challenges in {tema}?", "Who are the leading experts in {tema}?", "how to make money with {tema}",
    
]

# Função para gerar uma lista de pesquisas aleatórias sobre um tema
def gerar_pesquisas_sobre_tema(tema, n):
    return random.sample([p.format(tema=tema) for p in perguntas_en], n)  # Gera uma lista de n perguntas aleatórias sobre o tema

# Função para abrir o Edge
def abrir_edge():
    try:
        pyautogui.press('win')  # Pressiona a tecla 'win' para abrir o menu Iniciar
        pyautogui.write('edge')  # Digita 'edge' para procurar o navegador Edge
        pyautogui.press('enter')  # Pressiona 'enter' para abrir o Edge
        time.sleep(2)  # Aguarda 2 segundos para garantir que o navegador abra
        logging.info("Navegador Edge aberto com sucesso.")  # Registra no log que o navegador foi aberto com sucesso
        return True  # Retorna True indicando sucesso
    except Exception as e:
        logging.error(f"Erro ao abrir o Edge: {e}")  # Registra no log o erro ocorrido
        pyautogui.alert(f"Erro ao abrir o Edge: {e}")  # Exibe um alerta com o erro
        return False  # Retorna False indicando falha

# Função para realizar uma pesquisa
def realizar_pesquisa(pesquisa):
    try:
        pyautogui.hotkey('ctrl', 't')  # Abre uma nova aba no navegador
        pyautogui.write(pesquisa)  # Digita a pesquisa na barra de endereços
        pyautogui.press('enter')  # Pressiona 'enter' para realizar a pesquisa
        time.sleep(10)  # Aguarda 10 segundos para carregar a página e permanecer nela
        pyautogui.hotkey('ctrl', 'w')  # Fecha a aba após a pesquisa
        logging.info(f"Pesquisa realizada: {pesquisa}")  # Registra no log que a pesquisa foi realizada
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")  # Registra no log o erro ocorrido
        pyautogui.alert(f"Erro ao realizar a pesquisa: {e}")  # Exibe um alerta com o erro

# Função para limpar dados de navegação e cookies
def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')  # Abre a janela de limpeza de dados de navegação
        time.sleep(2)  # Aguarda 2 segundos para abrir a janela de limpeza de dados
        pyautogui.press('enter')  # Confirma a limpeza dos dados
        time.sleep(2)  # Aguarda 2 segundos para concluir a limpeza
        pyautogui.alert("Dados de navegação e cookies limpos com sucesso.")  # Exibe um alerta indicando sucesso
    except Exception as e:
        logging.error(f"Erro ao limpar os dados de navegação: {e}")  # Registra no log o erro ocorrido
        pyautogui.alert(f"Erro ao limpar os dados de navegação: {e}")  # Exibe um alerta com o erro

# Função para fechar o navegador
def fechar_navegador():
    try:
        pyautogui.hotkey('alt', 'f4')  # Fecha o navegador
        logging.info("Navegador fechado com sucesso.")  # Registra no log que o navegador foi fechado com sucesso
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")  # Registra no log o erro ocorrido
        pyautogui.alert(f"Erro ao fechar o navegador: {e}")  # Exibe um alerta com o erro

# Função para verificar a conectividade com a internet
def verificar_conectividade():
    try:
        response = requests.get('https://www.google.com', timeout=5)  # Faz uma requisição para o Google com timeout de 5 segundos
        if response.status_code == 200:
            logging.info("Conectividade com a internet verificada.")  # Registra no log que a conectividade foi verificada
            return True  # Retorna True indicando sucesso
        else:
            logging.error("Falha na verificação de conectividade com a internet.")  # Registra no log a falha na verificação
            return False  # Retorna False indicando falha
    except requests.ConnectionError as e:
        logging.error(f"Erro ao verificar a conectividade com a internet: {e}")  # Registra no log o erro ocorrido
        pyautogui.alert(f"Erro ao verificar a conectividade com a internet: {e}")  # Exibe um alerta com o erro
        return False  # Retorna False indicando falha

# Função principal para executar a automação
def executar_automacao(num_temas=6, num_perguntas=6):
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
                    
                    if abrir_edge():  # Tenta abrir o navegador Edge
                        for pesquisa in pesquisas:  # Realiza cada pesquisa gerada
                            realizar_pesquisa(pesquisa)
                        
                        limpar_dados_navegacao()  # Limpa os dados de navegação e cookies
                        fechar_navegador()  # Fecha o navegador
                    else:
                        pyautogui.alert("Não foi possível abrir o navegador Edge.")  # Exibe um alerta se não conseguir abrir o navegador
            else:
                pyautogui.alert("Não foi possível verificar a conectividade com a internet.")  # Exibe um alerta se não conseguir verificar a conectividade
            
            # Perguntar se deseja realizar outra pesquisa
            nova_pesquisa = pyautogui.confirm('Você deseja realizar outra pesquisa?', buttons=['Sim', 'Não'])
            if nova_pesquisa == 'Não':
                break  # Sai do loop se o usuário não quiser realizar outra pesquisa
        else:
            pyautogui.alert("O programa está fechando.")  # Exibe um alerta indicando que o programa está fechando
            logging.info("O usuário optou por não realizar a pesquisa. O programa está fechando.")  # Registra no log que o programa está fechando
            break  # Sai do loop

# Executar a automação com parâmetros configuráveis
executar_automacao(num_temas=6, num_perguntas=6)  # Executa a automação com 6 temas e 5 perguntas por tema
