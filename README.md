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
git clone https://github.com/MisaAndrejezieski/automacao-pesquisa.git
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

# Insira aqui o código principal do programa...

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
E-mail: misaelandrejezieski130982@outlook.com
GitHub: https://github.com/MisaAndrejezieski
Explicação do README:
Descrição: Uma explicação geral sobre o que o programa faz.
Funcionalidades: Lista das principais funções do programa.
Requisitos: Instruções para configurar o ambiente e as dependências.
Instalação: Como clonar o repositório e instalar as dependências necessárias.
Uso: Como rodar o programa e interagir com a interface.
Estrutura do Projeto: Detalha a organização dos arquivos no projeto.
Contribuição: Passos para contribuir com melhorias no código.
Licença: Explicação sobre a licença do projeto (MIT).
