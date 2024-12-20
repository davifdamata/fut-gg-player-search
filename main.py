import requests
import tkinter as tk
from tkinter import ttk

# Função para realizar a pesquisa do jogador


def buscar_jogador(*args):
    """
    Função chamada automaticamente a cada alteração no campo de texto.
    Faz a consulta à API e exibe os resultados ou uma mensagem indicando que não há jogadores encontrados.
    """
    playerrequest = nome_var.get().strip().replace(' ', '+')

    if not playerrequest:
        atualizar_resultados(
            "Digite o nome de um jogador para iniciar a busca.")
        return

    try:
        api_url = f'https://www.fut.gg/api/fut/players/v2/search/?name={
            playerrequest}'
        response = requests.get(api_url)
        response.raise_for_status()
        dados = response.json()
    except requests.RequestException:
        atualizar_resultados(
            "Erro ao acessar a API. Tente novamente mais tarde.")
        return

    if not dados.get('data'):
        atualizar_resultados("Nenhum jogador encontrado.")
        return

    players = []
    for player in dados['data']:
        name = player.get('commonName', 'Desconhecido')
        rarity = player.get('rarityName', 'Desconhecido')
        quality = player.get('quality', '')
        ovr = player.get('overall', 'N/A')

        version = f"{quality} {rarity}" if rarity in [
            'Rare', 'Common'] else rarity

        if player.get('price') is None:
            price = 'Jogador Extinto' if not player.get(
                'isObjective') else 'Jogador de Objetivo'
        else:
            fprice = f'{player["price"]:,}'.replace(',', '.')
            price = f'{fprice} moedas'
            if player.get('isSbc', False):
                price = f'O jogador é de DME custando {fprice} moedas'

        players.append(f"Nome: {name}\nVersão: {
                       version}\nOver: {ovr}\nPreço: {price}\n")

    atualizar_resultados("\n".join(players))


def atualizar_resultados(texto):
    """
    Atualiza o campo de resultados com o texto fornecido.
    """
    label_result.config(state=tk.NORMAL)
    label_result.delete(1.0, tk.END)
    label_result.insert(tk.END, texto)
    label_result.config(state=tk.DISABLED)


# Configuração da janela principal
root = tk.Tk()
root.title("Busca de Jogadores - EA FC 25")
root.geometry("700x500")
root.config(bg="#001f3f")  # Azul escuro EA FC

# Título da aplicação
label_titulo = tk.Label(
    root,
    text="Busca de Jogadores FIFA",
    font=("Helvetica", 24, "bold"),
    fg="#ff8300",  # Laranja EA FC
    bg="#001f3f"
)
label_titulo.pack(pady=20)

# Campo para digitar o nome do jogador
frame_busca = tk.Frame(root, bg="#001f3f")
frame_busca.pack(pady=10)

label_nome = tk.Label(
    frame_busca,
    text="Digite o nome do jogador:",
    font=("Helvetica", 14),
    fg="#ffffff",
    bg="#001f3f"
)
label_nome.grid(row=0, column=0, padx=10)

nome_var = tk.StringVar()
nome_var.trace_add("write", buscar_jogador)
entry_nome = ttk.Entry(frame_busca, textvariable=nome_var,
                       font=("Helvetica", 14), width=30)
entry_nome.grid(row=0, column=1)

# Frame para o campo de resultados, com barra de rolagem
frame_resultados = tk.Frame(root, bg="#001f3f")
frame_resultados.pack(pady=10)

scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)

label_result = tk.Text(
    frame_resultados,
    width=75,
    height=15,
    font=("Courier", 12),
    wrap=tk.WORD,
    yscrollcommand=scrollbar.set,
    state=tk.DISABLED,
    bg="#003366",  # Azul secundário EA FC
    fg="#ffffff",  # Texto branco
    bd=0,
    relief="flat"
)
label_result.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

scrollbar.config(command=label_result.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

frame_resultados.grid_rowconfigure(0, weight=1)
frame_resultados.grid_columnconfigure(0, weight=1)

# Exibe uma mensagem inicial
atualizar_resultados("Digite o nome de um jogador para iniciar a busca.")

# Inicia a interface gráfica
root.mainloop()
