import sys
import argparse
from gui import HTTPClientGUI
from http_cli import HTTPClientCLI

def main():
    """Função principal que escolhe entre GUI e CLI"""
    
    # Se não há argumentos ou se o primeiro argumento é --gui, usar GUI
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == '--gui'):
        # Interface gráfica
        import tkinter as tk
        root = tk.Tk()
        app = HTTPClientGUI(root)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            root.quit()
            
    elif sys.argv[1] == '--cli':
        # Interface de linha de comando
        # Remove --cli dos argumentos para o parser
        sys.argv.pop(1)
        cli = HTTPClientCLI()
        cli.run()
    else:
        # Se tem argumentos mas não é --gui, assumir CLI
        cli = HTTPClientCLI()
        cli.run()

if __name__ == "__main__":
    main()