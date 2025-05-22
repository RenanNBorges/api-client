import requests
import json
import time
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, Any, Optional, Tuple

class HTTPClient:
    """Classe principal para realizar requisições HTTP"""
    
    def __init__(self):
        self.history = []
        self.session = requests.Session()
        
    def parse_headers(self, headers_text: str) -> Dict[str, str]:
        """Parse headers do texto para dicionário"""
        headers = {}
        if headers_text and headers_text.strip():
            for line in headers_text.strip().split('\n'):
                if ':' in line and line.strip():
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
        return headers

    def format_json(self, text: str) -> str:
        """Formata JSON para exibição"""
        try:
            parsed = json.loads(text)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except:
            return text

    def make_request(self, method: str, url: str, headers: Optional[Dict[str, str]] = None, 
                    body: Optional[str] = None, timeout: int = 30) -> Tuple[requests.Response, float]:
        """
        Faz uma requisição HTTP e retorna a resposta com tempo de execução
        
        Returns:
            Tuple[Response, float]: (response_object, response_time_ms)
        """
        if headers is None:
            headers = {}
            
        # Preparar dados da requisição
        request_kwargs = {
            'method': method.upper(),
            'url': url,
            'headers': headers,
            'timeout': timeout
        }
        
        # Adicionar body se necessário
        if body and body.strip() and method.upper() not in ['GET', 'HEAD']:
            request_kwargs['data'] = body
        
        # Executar requisição
        start_time = time.time()
        response = self.session.request(**request_kwargs)
        end_time = time.time()
        
        # Calcular tempo de resposta em milissegundos
        response_time = round((end_time - start_time) * 1000, 2)
        
        # Adicionar ao histórico
        self.add_to_history(method, url, response.status_code, response_time)
        
        return response, response_time

    def add_to_history(self, method: str, url: str, status_code: int, response_time: float):
        """Adiciona requisição ao histórico"""
        entry = {
            'method': method,
            'url': url,
            'status_code': status_code,
            'response_time': response_time,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.insert(0, entry)  # Adicionar no início
        
        # Manter apenas últimas 50 requisições
        if len(self.history) > 50:
            self.history = self.history[:50]

    def get_formatted_response(self, response: requests.Response) -> Dict[str, Any]:
        """Retorna resposta formatada"""
        try:
            content_type = response.headers.get('content-type', '').lower()
            if 'application/json' in content_type:
                formatted_body = self.format_json(response.text)
            else:
                formatted_body = response.text
        except:
            formatted_body = response.text
            
        return {
            'status_code': response.status_code,
            'status_text': response.reason,
            'headers': dict(response.headers),
            'body': formatted_body,
            'raw_body': response.text,
            'url': response.url,
            'encoding': response.encoding
        }
