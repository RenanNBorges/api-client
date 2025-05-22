import argparse
import sys
from http_client_core import HTTPClient

class HTTPClientCLI:
    """Interface de linha de comando para o HTTP Client"""
    
    def __init__(self):
        self.client = HTTPClient()
        
    def run(self):
        """Executa a interface CLI"""
        parser = argparse.ArgumentParser(description='HTTP Client Tool - Linha de Comando')
        parser.add_argument('method', choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'],
                          help='Método HTTP')
        parser.add_argument('url', help='URL da requisição')
        parser.add_argument('-H', '--header', action='append', 
                          help='Headers (formato: "Nome: Valor")')
        parser.add_argument('-d', '--data', help='Dados do corpo da requisição')
        parser.add_argument('-f', '--file', help='Arquivo com dados do corpo')
        parser.add_argument('-t', '--timeout', type=int, default=30, 
                          help='Timeout em segundos (padrão: 30)')
        parser.add_argument('-v', '--verbose', action='store_true',
                          help='Saída detalhada')
        parser.add_argument('--json', action='store_true',
                          help='Saída em formato JSON')
        
        args = parser.parse_args()
        
        try:
            # Preparar headers
            headers = {}
            if args.header:
                for header in args.header:
                    if ':' in header:
                        key, value = header.split(':', 1)
                        headers[key.strip()] = value.strip()
            
            # Preparar body
            body = None
            if args.data:
                body = args.data
            elif args.file:
                try:
                    with open(args.file, 'r', encoding='utf-8') as f:
                        body = f.read()
                except FileNotFoundError:
                    print(f"Erro: Arquivo '{args.file}' não encontrado")
                    sys.exit(1)
            
            # Fazer requisição
            print(f"Enviando {args.method} para {args.url}...")
            response, response_time = self.client.make_request(
                args.method, args.url, headers, body, args.timeout
            )
            
            # Processar resposta
            formatted_response = self.client.get_formatted_response(response)
            
            # Exibir resultado
            if args.json:
                self.print_json_output(formatted_response, response_time)
            else:
                self.print_formatted_output(formatted_response, response_time, args.verbose)
                
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nRequisição cancelada pelo usuário")
            sys.exit(1)
        except Exception as e:
            print(f"Erro inesperado: {e}")
            sys.exit(1)

    def print_formatted_output(self, response_data: dict, response_time: float, verbose: bool):
        """Imprime saída formatada"""
        print(f"\n{'='*60}")
        print(f"Status: {response_data['status_code']} {response_data['status_text']}")
        print(f"Tempo de resposta: {response_time}ms")
        print(f"URL: {response_data['url']}")
        
        if verbose:
            print(f"\n{'='*20} HEADERS DE RESPOSTA {'='*20}")
            for key, value in response_data['headers'].items():
                print(f"{key}: {value}")
        
        print(f"\n{'='*25} CORPO DA RESPOSTA {'='*25}")
        print(response_data['body'])
        print(f"{'='*60}")

    def print_json_output(self, response_data: dict, response_time: float):
        """Imprime saída em formato JSON"""
        output = {
            'status_code': response_data['status_code'],
            'status_text': response_data['status_text'],
            'response_time_ms': response_time,
            'url': response_data['url'],
            'headers': response_data['headers'],
            'body': response_data['raw_body']
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))

