# Automação de Pesquisa no Navegador Edge

Descrição
Este programa realiza automações de pesquisa no navegador Microsoft Edge utilizando a biblioteca pyautogui para controlar a interface gráfica do usuário (GUI). Ele gera pesquisas aleatórias sobre diversos temas, realiza essas pesquisas no navegador, limpa os dados de navegação e fecha o navegador automaticamente após a conclusão. A automação também inclui uma interface gráfica amigável, desenvolvida com a biblioteca tkinter, para facilitar a configuração e execução da automação.

Funcionalidades
Automação de Pesquisa: Realiza pesquisas automáticas no navegador Edge.
Geração de Pesquisas Aleatórias: Gera perguntas aleatórias sobre diversos temas, como tecnologia, saúde, política, entre outros.
Limpeza de Dados de Navegação: Limpa os dados de navegação e cookies após cada pesquisa para manter o navegador limpo.
Verificação de Conectividade: Verifica a conectividade com a internet antes de iniciar as pesquisas.
Interface Gráfica: Interface amigável desenvolvida com tkinter, onde é possível configurar o número de temas e perguntas por tema.
Logs: Registra logs detalhados das operações realizadas, incluindo erros e eventos importantes.
Requisitos
Python 3.x
Bibliotecas Python: pyautogui, requests, tkinter
Navegador Microsoft Edge (necessário para a automação)
Instalação

1. Clone o repositório
bash
Copiar código
git clone github.com/MisaAndrejezieski/automacao-pesquisa.git
cd automacao-pesquisa
2. Instale as dependências
bash
Copiar código
pip install pyautogui requests
3. Certifique-se de que o navegador Edge esteja instalado no seu sistema.
Uso

1.Execute o programa:
bash
Copiar código
python automacao_pesquisa.py

2.Interface Gráfica:
Insira o número de temas e perguntas por tema.
Clique em "Iniciar Automação" para começar a automação de pesquisas.
Clique em "Fechar Programa" para encerrar o programa.
Estrutura do Projeto
plaintext
Copiar código
automacao-pesquisa/
│
├── 22287dragon_98813.ico          # Ícone para a barra superior (do programa)
├── 22287dragon_98813.png          # Imagem para a interface (opcional, caso queira personalizar)
├── automacao_pesquisa.log         # Arquivo de log com registros de operações realizadas
├── automacao_pesquisa.py          # Código principal do programa
└── README.md                      # Documentação do projeto
Exemplo de Código Principal
O código principal do programa é o seguinte:

python
Copiar código

## Insira aqui o código principal do programa

Funcionalidade do código:
Abrir o navegador Edge automaticamente e realizar pesquisas.
Limpar dados de navegação após cada pesquisa para manter o navegador limpo.
Gerar perguntas aleatórias sobre diversos temas e executá-las.
Interface gráfica para personalização da quantidade de temas e perguntas.
Registro de logs detalhados para depuração e análise.
Contribuição
Se você deseja contribuir com o projeto, siga os passos abaixo:

1. Fork o projeto.
Clique no botão "Fork" no GitHub.
2. Crie uma nova branch:
bash
Copiar código
git checkout -b minha-nova-funcionalidade
3. Faça suas alterações e commit:
bash
Copiar código
git commit -am 'Adiciona nova funcionalidade'
4. Envie para a branch original:
bash
Copiar código
git push origin minha-nova-funcionalidade
5. Crie um novo Pull Request.
Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

Contato
Nome: Misa Andrejezieski
E-mail:misaelandrejezieski130982@outlook.com
GitHub:github.com/MisaAndrejezieski

Explicação do README:
Descrição: Uma explicação geral sobre o que o programa faz.
Funcionalidades: Lista das principais funções do programa.
Requisitos: Instruções para configurar o ambiente e as dependências.
Instalação: Como clonar o repositório e instalar as dependências necessárias.
Uso: Como rodar o programa e interagir com a interface.
Estrutura do Projeto: Detalha a organização dos arquivos no projeto.
Contribuição: Passos para contribuir com melhorias no código.
Licença: Explicação sobre a licença do projeto (MIT).

Configuração de logging
logging.basicConfig( filename='automacao_eventos.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8' )

Log de erros específicos
logging.basicConfig( filename='automacao_erros.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8' )

Lista de temas em inglês
temas_en = [ "technology", "health", "education", "sports", "politics", "economy", "science", "art", "music", "literature", "history", "geography", "philosophy", "psychology", "sociology", "anthropology", "astronomy", "biology", "chemistry", "physics", "mathematics", "engineering", "medicine", "law", "administration", "marketing", "finance", "architecture", "design", "fashion", "gastronomy" ]

Lista de perguntas em inglês
perguntas_en = [ "What is {tema}?", "What are the latest news in {tema}?", "How does {tema} impact society?", "What are the main challenges in {tema}?", "Who are the leading experts in {tema}?", "How to make money with {tema}", ]

Função para gerar uma lista de pesquisas aleatórias sobre um tema
def gerar_pesquisas_sobre_tema(tema, n): return random.sample([p.format(tema=tema) for p in perguntas_en], n)

Função para salvar os resultados em CSV
def salvar_resultados(resultados): with open('resultados_pesquisas.csv', 'a', newline='', encoding='utf-8') as file: writer = csv.writer(file) if os.stat('resultados_pesquisas.csv').st_size == 0: writer.writerow(["Tema", "Pergunta", "Status"]) for resultado in resultados: writer.writerow([resultado['tema'], resultado['pergunta'], resultado['status']])

Função de "tentar novamente" com múltiplas tentativas
def tentar_novamente(funcao, max_tentativas=3, *args, **kwargs): for tentativa in range(max_tentativas): try: return funcao(*args,**kwargs) except Exception as e: logging.error(f"Tentativa {tentativa+1} de {funcao.name} falhou: {e}") if tentativa + 1 == max_tentativas: logging.error(f"Falha ao tentar executar {funcao.name} após {max_tentativas} tentativas.") raise e time.sleep(2)

Função para abrir o Edge
def abrir_edge(): try: pyautogui.press('win') pyautogui.write('edge') pyautogui.press('enter') time.sleep(2) logging.info("Navegador Edge aberto com sucesso.") return True except Exception as e: logging.error(f"Erro ao abrir o Edge: {e}") return False

Função para realizar uma pesquisa
def realizar_pesquisa(pesquisa): try: pyautogui.hotkey('ctrl', 't') pyautogui.write(pesquisa) pyautogui.press('enter') time.sleep(10) pyautogui.hotkey('ctrl', 'w') logging.info(f"Pesquisa realizada: {pesquisa}") return True except Exception as e: logging.error(f"Erro ao realizar a pesquisa: {e}") return False

Função para limpar dados de navegação e cookies
def limpar_dados_navegacao(): try: pyautogui.hotkey('ctrl', 'shift', 'delete') time.sleep(2) pyautogui.press('enter') time.sleep(2) logging.info("Dados de navegação e cookies limpos com sucesso.") return True except Exception as e: logging.error(f"Erro ao limpar os dados de navegação: {e}") return False

Função para verificar a conectividade com a internet
async def verificar_conectividade(): try: endpoints = ['https://www.google.com', 'https://www.bing.com', 'https://www.duckduckgo.com'] for url in endpoints: try: response = requests.get(url, timeout=5) if response.status_code == 200: logging.info(f"Conectividade com {url} verificada.") return True except requests.ConnectionError: logging.warning(f"Falha ao acessar {url}. Tentando outro...") return False except requests.RequestException as e: logging.error(f"Erro ao verificar conectividade: {e}") return False

Função para executar a automação
async def executar_automacao(num_temas=6, num_perguntas=6): resultados = [] if await verificar_conectividade(): if abrir_edge(): for_ in range(num_temas): tema = random.choice(temas_en) pesquisas = gerar_pesquisas_sobre_tema(tema, num_perguntas) for pesquisa in pesquisas: sucesso = False while not sucesso: sucesso = realizar_pesquisa(pesquisa) if not sucesso: logging.error(f"Falha ao realizar a pesquisa: {pesquisa}. Tentando novamente.") time.sleep(5) resultados.append({'tema': tema, 'pergunta': pesquisa, 'status': 'Concluída'}) await asyncio.sleep(5) limpar_dados_navegacao() salvar_resultados(resultados) logging.info("Automação concluída com sucesso.") else: logging.error("Falha ao abrir o navegador.") else: logging.error("Falha na verificação de conectividade com a internet.")

Função para rodar a automação em segundo plano
def iniciar_automacao_bg(num_temas, num_perguntas): asyncio.run(executar_automacao(num_temas, num_perguntas))

Interface gráfica
def iniciar_interface(): root = tk.Tk() root.title("Automação de Pesquisa") root.geometry('600x500') root.configure(bg='#cfffca')

Verify

Open In Editor
Edit
Copy code

## Adicionando o ícone

try:
    root.iconbitmap("Luffys_flag.ico")  # Defina o caminho do seu ícone
except Exception as e:
    logging.warning(f"Não foi possível carregar o ícone: {e}")

## Estilos

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', background='#A7D8D7', foreground='#2E4053', font=('Helvetica', 12, 'bold'))
style.map('TButton', background=[('active', '#80C7C6')])
style.configure('Red.TButton', background='#F28C8C', foreground='#2E4053', font=('Helvetica', 12, 'bold'))
style.map('Red.TButton', background=[('active', '#F76C6C')])
style.configure('TLabel', background='#F3F4F6', foreground='#2E4053', font=('Helvetica', 12))
style.configure('TEntry', font=('Helvetica', 12), padding=5)

## Barra de título personalizada

title_bar = tk.Frame(root, bg='#fdcae1', relief='raised', bd=2)
title_bar.pack(fill=tk.X)

## Adicionando a imagem na barra de título e centralizando

try:
    img = PhotoImage(file="22287dragon_98813.png")  # Use uma imagem PNG em vez de ICO
    logo_label = tk.Label(title_bar, image=img, bg='#fdcae1')
    logo_label.image = img  # Manter uma referência da imagem
    logo_label.pack(side=tk.TOP, pady=5)
except Exception as e:
    logging.warning(f"Não foi possível carregar a imagem: {e}")

## Função para mover a janela

def move_window(event):
    root.geometry(f'+{event.x_root - root.start_x}+{event.y_root - root.start_y}')

def start_move(event):
    root.start_x = event.x
    root.start_y = event.y

title_bar.bind('<Button-1>', start_move)
title_bar.bind('<B1-Motion>', move_window)

## Elementos da interface

ttk.Label(root, text="Número de Temas:", style='TLabel').pack(pady=10)
num_temas_entry = ttk.Entry(root, width=20)
num_temas_entry.pack(pady=5)
num_temas_entry.insert(0, "6")

ttk.Label(root, text="Número de Perguntas por Tema:", style='TLabel').pack(pady=10)
num_perguntas_entry = ttk.Entry(root, width=20)
num_perguntas_entry.pack(pady=5)
num_perguntas_entry.insert(0, "6")

    # Função de iniciar a automação
def iniciar_automacao_handler():
    try:
        num_temas = int(num_temas_entry.get())
        num_perguntas = int(num_perguntas_entry.get())
        threading.Thread(target=iniciar_automacao_bg, args=(num_temas, num_perguntas)).start()
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira números válidos.")

## Botão para iniciar a automação

start_button = ttk.Button(root, text="Iniciar Automação", command=iniciar_automacao_handler)
start_button.pack(pady=20)

## Botão para fechar a aplicação

close_button = ttk.Button(root, text="Fechar", command=root.quit, style='Red.TButton')
close_button.pack(pady=10)

root.mainloop()
Iniciar a interface gráfica
if name == "main": iniciar_interface()

O código apresentado é um script Python que implementa uma automação de pesquisas na internet utilizando a biblioteca pyautogui para interação com o sistema operacional e a interface gráfica do usuário (GUI) construída com tkinter. A seguir, farei uma análise detalhada dos principais componentes e funcionalidades do código.

Estrutura Geral
Importações: O código importa diversas bibliotecas, incluindo time, pyautogui, random, logging, requests, tkinter, threading, os, csv, e asyncio. Essas bibliotecas fornecem funcionalidades para manipulação de tempo, automação de GUI, geração de números aleatórios, registro de logs, requisições HTTP, e criação de interfaces gráficas.

Configuração de Logging: O código configura dois arquivos de log: um para registrar eventos gerais (automacao_eventos.log) e outro para registrar erros específicos (automacao_erros.log). Isso é útil para rastrear o comportamento da aplicação e diagnosticar problemas.

Listas de Temas e Perguntas: O código define listas de temas e perguntas em inglês, que serão utilizadas para gerar pesquisas aleatórias.

Funções Principais
gerar_pesquisas_sobre_tema(tema, n): Gera uma lista de perguntas aleatórias sobre um tema específico. Utiliza a função random.sample para selecionar perguntas sem repetição.

salvar_resultados(resultados): Salva os resultados das pesquisas em um arquivo CSV. Verifica se o arquivo está vazio para escrever o cabeçalho.

**tentar_novamente(funcao, max_tentativas, *args, kwargs): Uma função utilitária que tenta executar uma função várias vezes em caso de falha, registrando erros em log.

abrir_edge(): Utiliza pyautogui para abrir o navegador Microsoft Edge. Se a operação falhar, registra um erro.

realizar_pesquisa(pesquisa): Realiza uma pesquisa no navegador, abrindo uma nova aba e fechando-a após um tempo. Registra o sucesso ou falha da operação.

limpar_dados_navegacao(): Executa uma combinação de teclas para limpar dados de navegação e cookies no navegador.

verificar_conectividade(): Uma função assíncrona que verifica a conectividade com a internet ao tentar acessar várias URLs.

executar_automacao(num_temas, num_perguntas): Função principal que orquestra a automação. Gera temas e perguntas, executa pesquisas, registra os resultados e limpa dados de navegação.

Interface Gráfica
iniciar_interface(): Cria a interface gráfica utilizando tkinter. Inclui elementos como entradas para o número de temas e perguntas, botões para iniciar a automação e fechar a aplicação, além de um título personalizado.

Funções de Mover Janela: Implementa funcionalidades para mover a janela da aplicação, permitindo uma experiência de usuário mais interativa.

Considerações Finais
Uso de asyncio: O uso de asyncio para gerenciar a automação é interessante, pois permite que a aplicação não bloqueie a interface gráfica enquanto aguarda ações assíncronas, como verificações de conectividade.

Tratamento de Erros: O código faz um bom uso do tratamento de exceções, registrando erros em log e permitindo tentativas de reexecução de funções que falham.

Limitações do pyautogui: A automação com pyautogui é dependente da interface gráfica do sistema operacional e pode ser suscetível a falhas se a interface mudar ou se houver interrupções (como um usuário movendo o mouse).

Melhorias Potenciais: Poderia haver uma validação mais robusta das entradas do usuário, além de um feedback visual durante a execução da automação. Além disso, o uso de uma API para realizar pesquisas em vez de automação de GUI poderia ser mais eficiente e menos propenso a erros.

Em resumo, o código é um exemplo funcional de automação de tarefas de pesquisa na web, utilizando uma combinação de técnicas de programação assíncrona e interações com a interface gráfica do usuário.
