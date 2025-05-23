import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os


if not os.path.isfile('estoque.csv'):
    with open('estoque.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Produto', 'Quantidade', 'Localização', 'Valor Unitário'])


def carregar_dados():
    tree.delete(*tree.get_children())
    try:
        with open('estoque.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                tree.insert("", tk.END, values=row)
    except FileNotFoundError:
        pass


def adicionar_produto():
    produto = entry_produto.get().strip()
    quantidade = entry_quantidade.get().strip()
    localizacao = entry_localizacao.get().strip()
    valor = entry_valor.get().strip().replace(',', '.')

    if not (produto and quantidade and localizacao and valor):
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    try:
        quantidade = int(quantidade)
        valor = float(valor)
    except ValueError:
        messagebox.showwarning("Atenção", "Quantidade deve ser número inteiro e valor deve ser numérico.")
        return

    
    atualizado = False
    linhas = []
    with open('estoque.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        cabecalho = next(reader)
        for row in reader:
            if row[0] == produto and row[2] == localizacao:
                nova_quantidade = int(row[1]) + quantidade
                linhas.append([produto, nova_quantidade, localizacao, row[3]])
                atualizado = True
            else:
                linhas.append(row)

    if not atualizado:
        linhas.append([produto, quantidade, localizacao, valor])

    with open('estoque.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)
        writer.writerows(linhas)

    carregar_dados()
    limpar_campos()


def retirar_produto():
    produto = entry_produto.get().strip()
    quantidade = entry_quantidade.get().strip()
    localizacao = entry_localizacao.get().strip()

    if not (produto and quantidade and localizacao):
        messagebox.showwarning("Atenção", "Preencha Produto, Quantidade e Localização para retirar.")
        return

    try:
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showwarning("Atenção", "Quantidade deve ser um número inteiro.")
        return

    linhas = []
    encontrado = False
    with open('estoque.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        cabecalho = next(reader)
        for row in reader:
            if row[0] == produto and row[2] == localizacao:
                estoque_atual = int(row[1])
                if estoque_atual >= quantidade:
                    nova_quantidade = estoque_atual - quantidade
                    if nova_quantidade > 0:
                        linhas.append([produto, nova_quantidade, localizacao, row[3]])
                    encontrado = True
                else:
                    messagebox.showerror("Erro", "Quantidade insuficiente em estoque.")
                    return
            else:
                linhas.append(row)

    if not encontrado:
        messagebox.showerror("Erro", "Produto não encontrado na localização especificada.")
    else:
        with open('estoque.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(cabecalho)
            writer.writerows(linhas)
        carregar_dados()
        limpar_campos()


def limpar_campos():
    entry_produto.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_localizacao.delete(0, tk.END)
    entry_valor.delete(0, tk.END)


janela = tk.Tk()
janela.title("Sistema de Gestão de Estoque")
janela.geometry("900x600")
janela.resizable(False, False)
janela.configure(bg="#f0f0f0")


titulo = tk.Label(janela, text="Controle de Estoque", font=("Arial", 20, "bold"), bg="#f0f0f0")
titulo.pack(pady=10)

frame = tk.Frame(janela, bg="#f0f0f0")
frame.pack(pady=10)


tk.Label(frame, text="Produto:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
entry_produto = tk.Entry(frame)
entry_produto.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Quantidade:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
entry_quantidade = tk.Entry(frame)
entry_quantidade.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame, text="Localização:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
entry_localizacao = tk.Entry(frame)
entry_localizacao.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Valor Unitário (R$):", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5)
entry_valor = tk.Entry(frame)
entry_valor.grid(row=1, column=3, padx=5, pady=5)


frame_botoes = tk.Frame(janela, bg="#f0f0f0")
frame_botoes.pack(pady=10)

btn_adicionar = tk.Button(frame_botoes, text="Adicionar Produto", command=adicionar_produto, bg="#4CAF50", fg="white", width=20)
btn_adicionar.grid(row=0, column=0, padx=10)

btn_retirar = tk.Button(frame_botoes, text="Retirar Produto", command=retirar_produto, bg="#f44336", fg="white", width=20)
btn_retirar.grid(row=0, column=1, padx=10)

btn_limpar = tk.Button(frame_botoes, text="Limpar Campos", command=limpar_campos, width=20)
btn_limpar.grid(row=0, column=2, padx=10)


colunas = ("Produto", "Quantidade", "Localização", "Valor Unitário")
tree = ttk.Treeview(janela, columns=colunas, show="headings")
for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")

tree.pack(pady=20)


rodape = tk.Label(janela, text="", bg="#f0f0f0")
rodape.pack(side="bottom", pady=10)


carregar_dados()

janela.mainloop()


