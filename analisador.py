import re
import tkinter as tk
from tkinter import scrolledtext

KEYWORDS = ['safira', 'diamante', 'esmeralda', 'return', 'topazio', 'agua-marinha', 'ametista', 'granada']
OPERATORS = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=']
DELIMITERS = ['(', ')', '{', '}', ';', ',']
STRING_LITERAL = r'\".*?\"'

def is_keyword(word):
    return word in KEYWORDS

def is_delimiter(char):
    return char in DELIMITERS

def is_operator(char):
    return char in OPERATORS

def is_number(token):
    return re.match(r'^\d+(\.\d+)?$', token) is not None

def is_identifier(token):
    return re.match(r'^[A-Za-z_]\w*$', token) is not None

def lex_analyzer(code):
    tokens = []
    current_line = 1
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.DOTALL)
    lines = code.split('\n')
    
    for line in lines:
        line_tokens = re.split(r'(\W)', line)
        
        for token in line_tokens:
            token = token.strip()
            if not token:
                continue

            if is_keyword(token):
                tokens.append((current_line, token, 'PALAVRA-CHAVE', None))
            elif is_number(token):
                tokens.append((current_line, token, 'NUMERAL', token))
            elif token in OPERATORS:
                tokens.append((current_line, token, 'OPERADOR', token))
            elif is_delimiter(token):
                tokens.append((current_line, token, 'DELIMITADOR', token))
            elif is_identifier(token):
                tokens.append((current_line, token, 'IDENTIFICADOR', None))
            elif re.match(STRING_LITERAL, token):
                tokens.append((current_line, token, 'STRING', token))
            else:
                tokens.append((current_line, token, 'DESCONHECIDO', token))
        
        current_line += 1

    return tokens

def display_tokens():
    code = text_input.get("1.0", tk.END)
    tokens = lex_analyzer(code)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"{'Linha':<5} {'Lexema':<20} {'Token':<15} {'Valor':<15}\n")
    output_text.insert(tk.END, f"{'-'*5} {'-'*20} {'-'*15} {'-'*15}\n")
    
    for line, lexeme, token, value in tokens:
        output_text.insert(tk.END, f"{line:<5} {lexeme:<20} {token:<15} {str(value):<15}\n")

root = tk.Tk()
root.title("Analisador Léxico")
root.geometry("700x500")
text_input = scrolledtext.ScrolledText(root, width=80, height=20)
text_input.pack(pady=10)
analyze_button = tk.Button(root, text="Analisar Código", command=display_tokens)
analyze_button.pack(pady=5)
output_text = scrolledtext.ScrolledText(root, width=80, height=35)
output_text.pack(pady=10)
root.mainloop()
