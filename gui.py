import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from http_core import HTTPClient

class DarkTheme:
    """Configurações do tema escuro"""
    BG_COLOR = "#2b2b2b"
    FG_COLOR = "#cb750c"
    SELECT_COLOR = "#404040"
    ENTRY_BG = "#404040"
    ENTRY_FG = "#ffffff"
    BUTTON_BG = "#404040"
    BUTTON_FG = "#ffffff"
    FRAME_BG = "#353535"
    ACCENT_COLOR = "#0078d4"
    SUCCESS_COLOR = "#4caf50"
    ERROR_COLOR = "#f44336"
    WARNING_COLOR = "#ff9800"

class HTTPClientGUI:
    """Interface gráfica para o HTTP Client com tema escuro"""
    
    def __init__(self, root):
        self.root = root
        self.client = HTTPClient()
        self.setup_theme()
        self.setup_ui()
        
    def setup_theme(self):
        """Configura o tema escuro"""
        self.root.title("HTTP Client Tool - Interface Gráfica")
        self.root.geometry("1400x900")
        self.root.configure(bg=DarkTheme.BG_COLOR)
        
        # Configurar estilo ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurações do tema escuro
        self.style.configure('TLabel', 
                           background=DarkTheme.BG_COLOR, 
                           foreground=DarkTheme.FG_COLOR)
        
        self.style.configure('TFrame', 
                           background=DarkTheme.BG_COLOR)
        
        self.style.configure('TLabelFrame', 
                           background=DarkTheme.BG_COLOR, 
                           foreground=DarkTheme.FG_COLOR)
        
        self.style.configure('TEntry', 
                           fieldbackground=DarkTheme.ENTRY_BG, 
                           foreground=DarkTheme.ENTRY_FG,
                           borderwidth=1)
        
        self.style.configure('TCombobox', 
                           fieldbackground=DarkTheme.ENTRY_BG, 
                           foreground=DarkTheme.ENTRY_FG)
        
        self.style.configure('TButton', 
                           background=DarkTheme.BUTTON_BG, 
                           foreground=DarkTheme.BUTTON_FG)
        
        self.style.configure('TNotebook', 
                           background=DarkTheme.BG_COLOR)
        
        self.style.configure('TNotebook.Tab', 
                           background=DarkTheme.FRAME_BG, 
                           foreground=DarkTheme.FG_COLOR)
        
    def setup_ui(self):
        """Configura a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🌐 HTTP Client Tool", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 25))
        
        # Frames principais
        self.setup_request_frame(main_frame)
        self.setup_response_frame(main_frame)
        self.setup_history_frame(main_frame)
        
    def setup_request_frame(self, parent):
        """Configura frame da requisição"""
        req_frame = ttk.LabelFrame(parent, text="🔧 Configuração da Requisição", padding="15")
        req_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       pady=(0, 15))
        req_frame.columnconfigure(3, weight=1)
        
        # Linha do método e URL
        method_frame = ttk.Frame(req_frame)
        method_frame.grid(row=0, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(0, 15))
        method_frame.columnconfigure(2, weight=1)
        
        ttk.Label(method_frame, text="Método:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.method_var = tk.StringVar(value="GET")
        method_combo = ttk.Combobox(method_frame, textvariable=self.method_var, 
                                   values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
                                   state="readonly", width=12)
        method_combo.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(method_frame, text="URL:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.url_var = tk.StringVar(value="https://httpbin.org/get")
        url_entry = ttk.Entry(method_frame, textvariable=self.url_var, font=('Arial', 10))
        url_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 15))
        method_frame.columnconfigure(3, weight=1)
        
        # Botões
        button_frame = ttk.Frame(method_frame)
        button_frame.grid(row=0, column=4)
        
        send_btn = ttk.Button(button_frame, text="🚀 Enviar", command=self.send_request_threaded)
        send_btn.grid(row=0, column=0, padx=(0, 5))
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Limpar", command=self.clear_all)
        clear_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Notebook para configurações
        self.req_notebook = ttk.Notebook(req_frame)
        self.req_notebook.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba Headers
        self.setup_headers_tab()
        
        # Aba Body
        self.setup_body_tab()
        
    def setup_headers_tab(self):
        """Configura aba de headers"""
        headers_frame = ttk.Frame(self.req_notebook)
        self.req_notebook.add(headers_frame, text="Headers")
        
        ttk.Label(headers_frame, text="Headers da requisição (formato: Nome: Valor):", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        self.headers_text = scrolledtext.ScrolledText(
            headers_frame, height=8, 
            bg=DarkTheme.ENTRY_BG, fg=DarkTheme.ENTRY_FG,
            insertbackground=DarkTheme.FG_COLOR,
            font=('Consolas', 10)
        )
        self.headers_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.headers_text.insert(tk.END, "Content-Type: application/json\nUser-Agent: HTTP-Client-Tool/2.0\nAccept: application/json")
        
    def setup_body_tab(self):
        """Configura aba de body"""
        body_frame = ttk.Frame(self.req_notebook)
        self.req_notebook.add(body_frame, text="Body")
        
        # Barra de ferramentas
        toolbar_frame = ttk.Frame(body_frame)
        toolbar_frame.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(toolbar_frame, text="Corpo da requisição:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        ttk.Button(toolbar_frame, text="JSON Exemplo", 
                  command=self.insert_json_example).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar_frame, text="Carregar Arquivo", 
                  command=self.load_file).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar_frame, text="Limpar", 
                  command=self.clear_body).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Área de texto
        self.body_text = scrolledtext.ScrolledText(
            body_frame, height=8,
            bg=DarkTheme.ENTRY_BG, fg=DarkTheme.ENTRY_FG,
            insertbackground=DarkTheme.FG_COLOR,
            font=('Consolas', 10)
        )
        self.body_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
    def setup_response_frame(self, parent):
        """Configura frame da resposta"""
        resp_frame = ttk.LabelFrame(parent, text="Resposta HTTP", padding="15")
        resp_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        resp_frame.columnconfigure(0, weight=1)
        resp_frame.rowconfigure(1, weight=1)
        
        # Status bar
        status_frame = ttk.Frame(resp_frame)
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="Aguardando requisição...", 
                                     font=('Arial', 11, 'bold'))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.time_label = ttk.Label(status_frame, text="", font=('Arial', 10))
        self.time_label.grid(row=0, column=1, sticky=tk.E)
        
        # Notebook da resposta
        self.resp_notebook = ttk.Notebook(resp_frame)
        self.resp_notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Abas da resposta
        self.setup_response_tabs()
        
    def setup_response_tabs(self):
        """Configura abas da resposta"""
        # Response Body
        body_frame = ttk.Frame(self.resp_notebook)
        self.resp_notebook.add(body_frame, text="Response Body")
        self.response_text = scrolledtext.ScrolledText(
            body_frame, height=18,
            bg=DarkTheme.ENTRY_BG, fg=DarkTheme.FG_COLOR,
            font=('Consolas', 10)
        )
        self.response_text.pack(fill=tk.BOTH, expand=True)
        
        # Response Headers
        headers_frame = ttk.Frame(self.resp_notebook)
        self.resp_notebook.add(headers_frame, text="Headers")
        self.response_headers_text = scrolledtext.ScrolledText(
            headers_frame, height=18,
            bg=DarkTheme.ENTRY_BG, fg=DarkTheme.FG_COLOR,
            font=('Consolas', 10)
        )
        self.response_headers_text.pack(fill=tk.BOTH, expand=True)
        
        # Raw Response
        raw_frame = ttk.Frame(self.resp_notebook)
        self.resp_notebook.add(raw_frame, text="Raw")
        self.response_raw_text = scrolledtext.ScrolledText(
            raw_frame, height=18,
            bg=DarkTheme.ENTRY_BG, fg=DarkTheme.FG_COLOR,
            font=('Consolas', 9)
        )
        self.response_raw_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_history_frame(self, parent):
        """Configura frame do histórico"""
        history_frame = ttk.LabelFrame(parent, text="Histórico", padding="15")
        history_frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(15, 0))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(1, weight=1)
        
        # Botão de limpeza
        ttk.Button(history_frame, text="Limpar Histórico", 
                  command=self.clear_history).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Lista do histórico
        self.history_listbox = tk.Listbox(
            history_frame, height=25,
            bg=DarkTheme.ENTRY_BG, fg=DarkTheme.FG_COLOR,
            selectbackground=DarkTheme.ACCENT_COLOR,
            font=('Consolas', 9)
        )
        self.history_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.history_listbox.bind('<Double-Button-1>', self.load_from_history)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, 
                                 command=self.history_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
        
    def send_request_threaded(self):
        """Envia requisição em thread separada"""
        def send():
            try:
                self.send_request()
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro inesperado: {str(e)}"))
        
        threading.Thread(target=send, daemon=True).start()
        
    def send_request(self):
        """Envia a requisição HTTP"""
        try:
            method = self.method_var.get()
            url = self.url_var.get().strip()
            headers_text = self.headers_text.get(1.0, tk.END)
            body_text = self.body_text.get(1.0, tk.END).strip()
            
            if not url:
                messagebox.showerror("Erro", "Por favor, insira uma URL válida")
                return
            
            # Update status
            self.root.after(0, lambda: self.status_label.config(
                text="🔄 Enviando requisição...", foreground=DarkTheme.WARNING_COLOR))
            
            # Parse headers
            headers = self.client.parse_headers(headers_text)
            
            # Fazer requisição
            response, response_time = self.client.make_request(method, url, headers, body_text)
            
            # Atualizar interface
            self.root.after(0, lambda: self.display_response(response, response_time))
            self.root.after(0, lambda: self.update_history())
            
        except Exception as e:
            error_msg = f"❌ Erro: {str(e)}"
            self.root.after(0, lambda: self.status_label.config(
                text=error_msg, foreground=DarkTheme.ERROR_COLOR))
            
    def display_response(self, response, response_time):
        """Exibe a resposta na interface"""
        formatted_response = self.client.get_formatted_response(response)
        
        # Status
        status_color = (DarkTheme.SUCCESS_COLOR if 200 <= response.status_code < 300 
                       else DarkTheme.ERROR_COLOR if response.status_code >= 400 
                       else DarkTheme.WARNING_COLOR)
        
        self.status_label.config(
            text=f"✅ {response.status_code} {response.reason}",
            foreground=status_color
        )
        self.time_label.config(text=f"{response_time}ms")
        
        # Response Body
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, formatted_response['body'])
        
        # Response Headers
        self.response_headers_text.delete(1.0, tk.END)
        headers_display = []
        for key, value in formatted_response['headers'].items():
            headers_display.append(f"{key}: {value}")
        self.response_headers_text.insert(tk.END, '\n'.join(headers_display))
        
        # Raw Response
        self.response_raw_text.delete(1.0, tk.END)
        raw_response = f"HTTP/1.1 {response.status_code} {response.reason}\n"
        for key, value in formatted_response['headers'].items():
            raw_response += f"{key}: {value}\n"
        raw_response += f"\n{formatted_response['raw_body']}"
        self.response_raw_text.insert(tk.END, raw_response)
        
    def update_history(self):
        """Atualiza lista do histórico"""
        self.history_listbox.delete(0, tk.END)
        for entry in self.client.history:
            display_text = f"[{entry['timestamp']}] {entry['method']} - {entry['status_code']} ({entry['response_time']}ms)"
            self.history_listbox.insert(tk.END, display_text)
            
    def load_from_history(self, event):
        """Carrega requisição do histórico"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        if index < len(self.client.history):
            entry = self.client.history[index]
            self.method_var.set(entry['method'])
            self.url_var.set(entry['url'])
            
    def insert_json_example(self):
        """Insere exemplo de JSON"""
        example = {
            "usuario": {
                "nome": "Maria Silva",
                "email": "maria@exemplo.com",
                "idade": 28
            },
            "dados": {
                "telefone": "+55 11 99999-9999",
                "cidade": "São Paulo",
                "ativo": True
            },
            "tags": ["cliente", "premium", "sp"]
        }
        self.body_text.delete(1.0, tk.END)
        self.body_text.insert(tk.END, json.dumps(example, indent=2, ensure_ascii=False))
        
    def load_file(self):
        """Carrega arquivo para o body"""
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=[("Arquivos de texto", "*.txt"), ("JSON", "*.json"), ("Todos", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.body_text.delete(1.0, tk.END)
                self.body_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")
                
    def clear_body(self):
        """Limpa o corpo da requisição"""
        self.body_text.delete(1.0, tk.END)
        
    def clear_all(self):
        """Limpa todas as áreas"""
        self.url_var.set("")
        self.headers_text.delete(1.0, tk.END)
        self.body_text.delete(1.0, tk.END)
        self.response_text.delete(1.0, tk.END)
        self.response_headers_text.delete(1.0, tk.END)
        self.response_raw_text.delete(1.0, tk.END)
        self.status_label.config(text="Aguardando requisição...", foreground=DarkTheme.FG_COLOR)
        self.time_label.config(text="")
        
    def clear_history(self):
        """Limpa o histórico"""
        self.history_listbox.delete(0, tk.END)
        self.client.history.clear()
