import time
import pyautogui
import random
import logging
import requests

# Configuração de logging
logging.basicConfig(filename='automacao_pesquisa.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# Listas de temas em diferentes idiomas
temas_pt = [
    "tecnologia", "saude", "educacao", "esportes", "politica", "economia", 
    "ciencia", "arte", "musica", "literatura", "historia", "geografia", 
    "filosofia", "psicologia", "sociologia", "antropologia", "astronomia", 
    "biologia", "quimica", "fisica", "matematica", "engenharia", "medicina", 
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
    "Como {tema} pode melhorar a educação?", "Quais são os avanços mais recentes em {tema}?",
    "Como {tema} está mudando o mercado de trabalho?", "Quais são os benefícios de {tema} na saúde?",
    "Como {tema} pode ajudar a combater as mudanças climáticas?", "Quais são os riscos associados ao uso de {tema}?",
    "Como {tema} está transformando a comunicação?", "Quais são as tendências futuras em {tema}?",
    "Como {tema} pode melhorar a segurança pública?", "Quais são os impactos de {tema} na economia?",
    "Como {tema} está mudando a indústria de entretenimento?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de recursos naturais?", "Quais são os desafios éticos de {tema}?",
    "Como {tema} está influenciando a política?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a mobilidade urbana?", "Quais são os impactos de {tema} na privacidade?",
    "Como {tema} está mudando a agricultura?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na resposta a desastres naturais?", "Quais são os impactos de {tema} na cultura?",
    "Como {tema} está transformando o setor financeiro?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a qualidade de vida?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando o comércio?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na preservação do meio ambiente?", "Quais são os impactos de {tema} na educação?",
    "Como {tema} está transformando o transporte?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a saúde mental?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de manufatura?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na inclusão social?", "Quais são os impactos de {tema} na segurança?",
    "Como {tema} está transformando o setor de serviços?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a acessibilidade?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de construção?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de resíduos?", "Quais são os impactos de {tema} na arte?",
    "Como {tema} está transformando o setor de turismo?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a eficiência energética?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de moda?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de água?", "Quais são os impactos de {tema} na música?",
    "Como {tema} está transformando o setor de varejo?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a sustentabilidade?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de jogos?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de saúde pública?", "Quais são os impactos de {tema} na literatura?",
    "Como {tema} está transformando o setor de energia?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a produtividade?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de mídia?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de crises?", "Quais são os impactos de {tema} na fotografia?",
    "Como {tema} está transformando o setor de educação?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a inovação?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de publicidade?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de projetos?", "Quais são os impactos de {tema} na dança?",
    "Como {tema} está transformando o setor de saúde?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a colaboração?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de transporte?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de tempo?", "Quais são os impactos de {tema} na escultura?",
    "Como {tema} está transformando o setor de manufatura?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a criatividade?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de alimentos?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de recursos humanos?", "Quais são os impactos de {tema} na pintura?",
    "Como {tema} está transformando o setor de telecomunicações?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a inovação?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de moda?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de finanças?", "Quais são os impactos de {tema} na arquitetura?",
    "Como {tema} está transformando o setor de turismo?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a eficiência?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de jogos?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de marketing?", "Quais são os impactos de {tema} na escultura?",
    "Como {tema} está transformando o setor de energia?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a produtividade?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de mídia?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de crises?", "Quais são os impactos de {tema} na fotografia?",
    "Como {tema} está transformando o setor de educação?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a inovação?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de publicidade?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de projetos?", "Quais são os impactos de {tema} na dança?",
    "Como {tema} está transformando o setor de saúde?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a colaboração?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de transporte?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de tempo?", "Quais são os impactos de {tema} na escultura?",
    "Como {tema} está transformando o setor de manufatura?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a criatividade?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de alimentos?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de recursos humanos?", "Quais são os impactos de {tema} na pintura?",
    "Como {tema} está transformando o setor de telecomunicações?", "Quais são os avanços em {tema}?",
    "Como {tema} pode melhorar a inovação?", "Quais são os desafios de {tema}?",
    "Como {tema} está mudando a indústria de moda?", "Quais são os principais desenvolvimentos em {tema}?",
    "Como {tema} pode ajudar na gestão de finanças?", "Quais são os impactos de {tema} na arquitetura?",
    "Como {tema} está transformando o setor de turismo"
]

# Lista de perguntas em inglês
perguntas_en = [
    "What is {tema}?", "What are the latest news in {tema}?", "How does {tema} impact society?",
    "What are the main challenges in {tema}?", "Who are the leading experts in {tema}?",
    "How can {tema} improve education?", "What are the latest advancements in {tema}?",
    "How is {tema} changing the job market?", "What are the benefits of {tema} in health?",
    "How can {tema} help combat climate change?", "What are the risks associated with the use of {tema}?",
    "How is {tema} transforming communication?", "What are the future trends in {tema}?",
    "How can {tema} improve public safety?", "What are the impacts of {tema} on the economy?",
    "How is {tema} changing the entertainment industry?", "What are the main developments in {tema}?",
    "How can {tema} help manage natural resources?", "What are the ethical challenges of {tema}?",
    "How is {tema} influencing politics?", "What are the advancements in {tema}?",
    "How can {tema} improve urban mobility?", "What are the impacts of {tema} on privacy?",
    "How is {tema} changing agriculture?", "What are the main developments in {tema}?",
    "How can {tema} help in disaster response?", "What are the impacts of {tema} on culture?",
    "How is {tema} transforming the financial sector?", "What are the advancements in {tema}?",
    "How can {tema} improve quality of life?", "What are the challenges of {tema}?",
    "How is {tema} changing commerce?", "What are the main developments in {tema}?",
    "How can {tema} help preserve the environment?", "What are the impacts of {tema} on education?",
    "How is {tema} transforming transportation?", "What are the advancements in {tema}?",
    "How can {tema} improve mental health?", "What are the challenges of {tema}?",
    "How is {tema} changing the manufacturing industry?", "What are the main developments in {tema}?",
    "How can {tema} help with social inclusion?", "What are the impacts of {tema} on security?",
    "How is {tema} transforming the service sector?", "What are the advancements in {tema}?",
    "How can {tema} improve accessibility?", "What are the challenges of {tema}?",
    "How is {tema} changing the construction industry?", "What are the main developments in {tema}?",
    "How can {tema} help with waste management?", "What are the impacts of {tema} on art?",
    "How is {tema} transforming the tourism sector?", "What are the advancements in {tema}?",
    "How can {tema} improve energy efficiency?", "What are the challenges of {tema}?",
    "How is {tema} changing the fashion industry?", "What are the main developments in {tema}?",
    "How can {tema} help with water management?", "What are the impacts of {tema} on music?",
    "How is {tema} transforming the retail sector?", "What are the advancements in {tema}?",
    "How can {tema} improve sustainability?", "What are the challenges of {tema}?",
    "How is {tema} changing the gaming industry?", "What are the main developments in {tema}?",
    "How can {tema} help with public health management?", "What are the impacts of {tema} on literature?",
    "How is {tema} transforming the energy sector?", "What are the advancements in {tema}?",
    "How can {tema} improve productivity?", "What are the challenges of {tema}?",
    "How is {tema} changing the media industry?", "What are the main developments in {tema}?",
    "How can {tema} help with crisis management?", "What are the impacts of {tema} on photography?",
    "How is {tema} transforming the education sector?", "What are the advancements in {tema}?",
    "How can {tema} improve innovation?", "What are the challenges of {tema}?",
    "How is {tema} changing the advertising industry?", "What are the main developments in {tema}?",
    "How can {tema} help with project management?", "What are the impacts of {tema} on dance?",
    "How is {tema} transforming the health sector?", "What are the advancements in {tema}?",
    "How can {tema} improve collaboration?", "What are the challenges of {tema}?",
    "How is {tema} changing the transportation industry?", "What are the main developments in {tema}?",
    "How can {tema} help with time management?", "What are the impacts of {tema} on sculpture?",
    "How is {tema} transforming the manufacturing sector?", "What are the advancements in {tema}?",
    "How can {tema} improve creativity?", "What are the challenges of {tema}?",
    "How is {tema} changing the food industry?", "What are the main developments in {tema}?",
    "How can {tema} help with human resources management?", "What are the impacts of {tema} on painting?",
    "How is {tema} transforming the telecommunications sector?", "What are the advancements in {tema}?",
    "How can {tema} improve innovation?", "What are the challenges of {tema}?",
    "How is {tema} changing the fashion industry?", "What are the main developments in {tema}?",
    "How can {tema} help with financial management?", "What are the impacts of {tema} on architecture?",
    "How is {tema} transforming the tourism sector?", "What are the advancements in {tema}?",
    "How can {tema} improve efficiency?", "What are the challenges of {tema}?",
    "How is {tema} changing the gaming industry?", "What are the main developments in {tema}?",
    "How can {tema} help with marketing management?", "What are the impacts of {tema} on sculpture?",
    "How is {tema} transforming the energy sector?", "What are the advancements in {tema}?",
    "How can {tema} improve productivity?", "What are the challenges of {tema}?",
    "How is {tema} changing the media industry?", "What are the main developments in {tema}?",
    "How can {tema} help with crisis management?", "What are the impacts of {tema} on photography?",
    "How is {tema} transforming the education sector?", "What are the advancements in {tema}?",
    "How can {tema} improve innovation?", "What are the challenges of {tema}?",
    "How is {tema} changing the advertising industry?", "What are the main developments in {tema}?",
    "How can {tema} help with project management?", "What are the impacts of {tema} on dance?",
    "How is {tema} transforming the health sector?", "What are the advancements in {tema}?",
    "How can {tema} improve collaboration?", "What are the challenges of {tema}?",
    "How is {tema} changing the transportation industry?", "What are the main developments in {tema}?",
    "How can {tema} help with time management?", "What are the impacts of {tema} on sculpture?",
    "How is {tema} transforming the manufacturing sector?", "What are the advancements in {tema}?",
    "How can {tema} improve creativity?", "What are the challenges of {tema}?",
    "How is {tema} changing the food industry?", "What are the main developments in {tema}?",
    "How can {tema} help with human resources management?", "What are the impacts of {tema} on painting?",
    "How is {tema} transforming the telecommunications sector?", "What are the advancements in {tema}?",
    "How can {tema} improve innovation?", "What are the challenges of {tema}?",
    "How is {tema} changing the fashion industry?", "What are the main developments in {tema}?",
    "How can {tema} help with financial management?", "What are the impacts of {tema} on architecture?",
    "How is {tema} transforming the tourism sector?", "What are the advancements in {tema}?",
    "How can {tema} improve efficiency?", "What are the challenges of {tema}?",
    "How is {tema} changing the gaming industry?", "What are the main developments in {tema}?",
    "How can {tema} help with marketing management?", "What are the impacts of {tema} on sculpture?",
    "How is {tema} transforming the energy sector?", "What are the advancements in {tema}?",
    "How can {tema} improve productivity?", "What are the challenges of {tema}?",
    "How is {tema} changing the media industry?", "What are the main developments in {tema}?",
    "How can {tema} help with crisis management?", "What are the impacts of {tema} on photography?",
    "How is {tema} transforming the education sector?", "What are the advancements in {tema}?",
    "How can {tema} improve innovation?", "What are the challenges of {tema}?",
    "How is {tema} changing the advertising industry?", "What are the main developments in {tema}?",
    "How can {tema} help with project management?", "What are the impacts of {tema} on dance?",
    "How is {tema} transforming the health sector?"
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

# Função principal para executar a automação
def executar_automacao(num_pesquisas=3):
    while True:
        # Selecionar o idioma
        idioma, temas = selecionar_idioma()
        
        # Perguntar ao usuário se deseja realizar a pesquisa
        resposta = pyautogui.confirm('Você deseja realizar a pesquisa?', buttons=['Sim', 'Não'])
        
        if resposta == 'Sim':
            # Selecionar o tema
            tema = pyautogui.confirm('Escolha um tema:', buttons=temas)
            
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
executar_automacao(num_pesquisas=3)
