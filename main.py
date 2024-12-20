import requests
import tkinter as tk
from tkinter import ttk

# Dicionários de idiomas
texts = {
    "en": {
        "title": "Player Search - EA FC 25",
        "app_title": "EA FC Player Search",
        "enter_name": "Enter the player's name:",
        "search_prompt": "Enter a player's name to start the search.",
        "search_error": "Error accessing the API. Please try again later.",
        "not_found": "No players found.",
        "language_button": "Mudar para Português",
        "player_format": "Name: {name}\nVersion: {version}\nOverall: {ovr}\nPrice: {price}\n",
        "extinct": "Player Extinct",
        "objective": "Player Objective",
        "coins": "coins",
    },
    "pt": {
        "title": "Busca de Jogadores - EA FC 25",
        "app_title": "Busca de Jogadores EA FC",
        "enter_name": "Digite o nome do jogador:",
        "search_prompt": "Digite o nome de um jogador para iniciar a busca.",
        "search_error": "Erro ao acessar a API. Tente novamente mais tarde.",
        "not_found": "Nenhum jogador encontrado.",
        "language_button": "Switch to English",
        "player_format": "Nome: {name}\nVersão: {version}\nOverall: {ovr}\nPreço: {price}\n",
        "extinct": "Jogador Extinto",
        "objective": "Jogador de Objetivo",
        "coins": "moedas",
    }
}

# Variável global para o idioma atual
current_language = "en"


# Função para alternar o idioma
def switch_language():
    global current_language
    current_language = "pt" if current_language == "en" else "en"
    update_interface()


# Atualiza a interface com base no idioma selecionado
def update_interface():
    root.title(texts[current_language]["title"])
    label_titulo.config(text=texts[current_language]["app_title"])
    label_nome.config(text=texts[current_language]["enter_name"])
    botao_language.config(text=texts[current_language]["language_button"])

    # Atualiza o texto exibido na caixa de resultados para o idioma selecionado
    current_results = label_result.get("1.0", tk.END).strip()
    if current_results == texts["en"]["search_prompt"] or current_results == texts["pt"]["search_prompt"]:
        atualizar_resultados(texts[current_language]["search_prompt"])
    elif current_results == texts["en"]["not_found"] or current_results == texts["pt"]["not_found"]:
        atualizar_resultados(texts[current_language]["not_found"])
    else:
        translate_results(current_results)


# Traduz os resultados atuais para o idioma selecionado
def translate_results(current_results):
    translated_results = []
    for block in current_results.split("\n\n"):
        lines = block.split("\n")
        if len(lines) == 4:
            name_line, version_line, overall_line, price_line = lines
            name_key = "Name: " if current_language == "en" else "Nome: "
            version_key = "Version: " if current_language == "en" else "Versão: "
            overall_key = "Overall: " if current_language == "en" else "Overall: "
            price_key = "Price: " if current_language == "en" else "Preço: "

            translated_results.append(
                f"{name_key}{name_line.split(': ')[1]}\n"
                f"{version_key}{version_line.split(': ')[1]}\n"
                f"{overall_key}{overall_line.split(': ')[1]}\n"
                f"{price_key}{price_line.split(': ')[1]}"
            )
    atualizar_resultados("\n\n".join(translated_results))


# Função para realizar a pesquisa do jogador
def buscar_jogador(*args):
    playerrequest = nome_var.get().strip().replace(' ', '+')

    if not playerrequest:
        atualizar_resultados(texts[current_language]["search_prompt"])
        return

    try:
        api_url = f'https://www.fut.gg/api/fut/players/v2/search/?name={
            playerrequest}'
        response = requests.get(api_url)
        response.raise_for_status()
        dados = response.json()
    except requests.RequestException:
        atualizar_resultados(texts[current_language]["search_error"])
        return

    if not dados.get('data'):
        atualizar_resultados(texts[current_language]["not_found"])
        return

    players = []
    for player in dados['data']:
        name = player.get('commonName', 'Unknown')
        rarity = player.get('rarityName', 'Unknown')
        quality = player.get('quality', '')
        ovr = player.get('overall', 'N/A')

        version = f"{quality} {rarity}" if rarity in [
            'Rare', 'Common'] else rarity

        if player.get('price') is None:
            price = texts[current_language]["extinct"] if not player.get(
                'isObjective') else texts[current_language]["objective"]
        else:
            fprice = f'{player["price"]:,}'.replace(',', '.')
            price = f"{fprice} {texts[current_language]['coins']}"

        players.append(texts[current_language]["player_format"].format(
            name=name, version=version, ovr=ovr, price=price))

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
root.geometry("700x500")
root.config(bg="#001f3f")  # Azul escuro EA FC

# Título da aplicação
label_titulo = tk.Label(
    root,
    font=("Helvetica", 24, "bold"),
    fg="#ff8300",  # Laranja EA FC
    bg="#001f3f"
)
label_titulo.pack(pady=20)

# Botão para alternar idioma
botao_language = tk.Button(
    root,
    font=("Helvetica", 10),
    bg="#0077FF",  # Azul EA FC
    fg="#ffffff",
    text=texts[current_language]["language_button"],
    command=switch_language
)
botao_language.pack(anchor="ne", padx=10, pady=5)

# Campo para digitar o nome do jogador
frame_busca = tk.Frame(root, bg="#001f3f")
frame_busca.pack(pady=10)

label_nome = tk.Label(
    frame_busca,
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
update_interface()

# Inicia a interface gráfica
root.mainloop()
