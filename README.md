# Cliente Web Raiz
Este projeto é um Cliente Web Raiz desenvolvido em Python, semelhante a ferramentas como HTTP Toolkit, Postman ou Insomnia. Ele permite enviar requisições HTTP/HTTPS e visualizar as respostas completas, incluindo cabeçalhos e conteúdo. O programa suporta todos os verbos HTTP (GET, POST, PUT, DELETE, etc.) e é capaz de interpretar respostas.

Este trabalho foi desenvolvido como parte da avaliação 1 da disciplina de Sistemas para Internet II, da Universidade Federal do Rio Grande (FURG). Ele serve como base para futuros desenvolvimentos e demonstra o uso dos módulos requests para comunicação HTTP e tkinter para a interface gráfica de usuário (GUI).

Funcionalidades
Envio de Requisições HTTP/HTTPS: Suporta diversos métodos HTTP (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD).
Visualização Completa do Protocolo: Exibe tanto os cabeçalhos quanto o corpo da requisição e da resposta.
Suporte a Diferentes Formatos de Resposta: Renderiza respostas forma clara.
Interface Gráfica (GUI): Uma interface intuitiva construída com tkinter para facilitar a interação.
Interface de Linha de Comando (CLI): Opção para interagir com o cliente via terminal para automação ou uso rápido.
Instalação
Para rodar este projeto, você precisará ter o Python instalado.

Clone o repositório:

```Bash

git clone https://github.com/seu-usuario/cliente-web-raiz.git
cd cliente-web-raiz
```
- Crie e ative um ambiente virtual (recomendado):

```Bash

python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```
- Instale as dependências:

```Bash

pip install -r requirements.txt
```
- O arquivo requirements.txt deve conter:

`requests
Como Usar
Você pode executar o Cliente Web Raiz de duas maneiras: com interface gráfica (GUI) ou via linha de comando (CLI).

Modo Gráfico (GUI)
Para iniciar a aplicação com a interface gráfica, execute o main.py sem argumentos ou com a flag --gui:

```Bash

python main.py
```
ou

```Bash

python main.py --gui
```
A janela da aplicação será aberta, permitindo que você insira URLs, escolha verbos HTTP, adicione cabeçalhos e corpo da requisição, e visualize a resposta.

Modo Linha de Comando (CLI)
Para usar a interface de linha de comando, execute main.py com a flag --cli e os argumentos necessários para sua requisição:

```Bash

python main.py --cli --help
```
Isso exibirá as opções disponíveis para o modo CLI. Um exemplo de uso seria:

```Bash

python main.py --cli get https://jsonplaceholder.typicode.com/posts/1
```
Você também pode omitir a flag --cli se passar outros argumentos que não sejam --gui:

```Bash

python main.py get https://jsonplaceholder.typicode.com/posts/1 -H "User-Agent: MeuClienteHTTP"
```
Estrutura do Projeto
`main.py:` Ponto de entrada principal da aplicação, responsável por decidir entre a GUI ou CLI.
`gui.py:` Contém a lógica e a interface construída com tkinter para o cliente HTTP gráfico.
`ttp_cli.py:` Contém a lógica para a interface de linha de comando do cliente HTTP.
requirements.txt: Lista as dependências do projeto.

Licença
Este projeto está licenciado sob a MIT License.
