import requests
import tkinter as tk
from tkinter import messagebox

# Função para realizar a pesquisa do jogador
def buscar_jogador(*args):
    """
    Função chamada automaticamente a cada alteração no campo de texto.
    Faz a consulta à API e exibe os resultados ou uma mensagem indicando que não há jogadores encontrados.
    """
    # Pega o nome do jogador do campo de entrada, substituindo espaços por '+'
    playerrequest = nome_var.get().strip().replace(' ', '+')
    
    # Se o campo estiver vazio, limpa os resultados e retorna
    if not playerrequest:
        atualizar_resultados("Digite o nome de um jogador para iniciar a busca.")
        return

    try:
        # Realiza a chamada à API para buscar os jogadores
        api_url = f'https://www.fut.gg/api/fut/players/v2/search/?name={playerrequest}'
        response = requests.get(api_url)
        response.raise_for_status()  # Garante que erros HTTP sejam tratados como exceções
        dados = response.json()
    except requests.RequestException as e:
        # Em caso de falha na API, exibe uma mensagem genérica no campo de resultados
        atualizar_resultados("Erro ao acessar a API. Tente novamente mais tarde.")
        return

    # Caso a resposta da API não contenha dados, exibe uma mensagem padrão
    if not dados.get('data'):
        atualizar_resultados("Nenhum jogador encontrado.")
        return
    
    # Processa os jogadores retornados pela API
    players = []
    for player in dados['data']:
        name = player.get('commonName', 'Desconhecido')  # Nome do jogador
        rarity = player.get('rarityName', 'Desconhecido')  # Raridade do jogador
        quality = player.get('quality', '')  # Qualidade (ex.: Gold, Silver)
        ovr = player.get('overall', 'N/A')  # Rating geral
        id = player.get('eaId', 'N/A')  # ID do jogador

        # Determina a versão do jogador
        version = f"{quality} {rarity}" if rarity in ['Rare', 'Common'] else rarity

        # Determina o preço do jogador
        if player.get('price') is None:
            if player.get('isObjective', False):
                price = 'Jogador de Objetivo'
            else:
                price = 'Jogador Extinto'
        else:
            fprice = f'{player["price"]:,}'.replace(',', '.')
            price = f'{fprice} moedas'
            if player.get('isSbc', False):
                price = f'O jogador é de DME custando {fprice} moedas'

        # Armazena os dados formatados do jogador
        players.append(f"Nome: {name}\nVersão: {version}\nOver: {ovr}\nPreço: {price}\n")

    # Atualiza os resultados na interface
    atualizar_resultados("\n".join(players))

def atualizar_resultados(texto):
    """
    Atualiza o campo de resultados com o texto fornecido.
    """
    label_result.config(state=tk.NORMAL)  # Habilita o campo para edição
    label_result.delete(1.0, tk.END)  # Limpa o conteúdo atual
    label_result.insert(tk.END, texto)  # Insere o novo texto
    label_result.config(state=tk.DISABLED)  # Desabilita o campo para edição

# Configuração da janela principal
root = tk.Tk()
root.title("Busca de Jogadores - FUT GG")
root.geometry("600x400")  # Define o tamanho da janela
root.config(bg="#f0f0f0")

# Título da aplicação
label_titulo = tk.Label(root, text="Busca de Jogadores EA FC 25", font=("Arial", 20, "bold"), fg="#333", bg="#f0f0f0")
label_titulo.pack(pady=20)

# Campo para digitar o nome do jogador
label_nome = tk.Label(root, text="Digite o nome do jogador:", font=("Arial", 12), bg="#f0f0f0")
label_nome.pack(pady=10)

# Usa StringVar para monitorar alterações no campo de entrada
nome_var = tk.StringVar()
nome_var.trace_add("write", buscar_jogador)  # A cada tecla pressionada, chama buscar_jogador
entry_nome = tk.Entry(root, width=40, font=("Arial", 14), textvariable=nome_var)
entry_nome.pack(pady=10)

# Frame para o campo de resultados, com barra de rolagem
frame_resultados = tk.Frame(root)
frame_resultados.pack(pady=10)

# Barra de rolagem para os resultados
scrollbar = tk.Scrollbar(frame_resultados, orient=tk.VERTICAL)

# Campo de texto para exibir os resultados
label_result = tk.Text(frame_resultados, width=70, height=10, font=("Arial", 12), wrap=tk.WORD, yscrollcommand=scrollbar.set, state=tk.DISABLED)
label_result.grid(row=0, column=0)

# Configuração da barra de rolagem
scrollbar.config(command=label_result.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Exibe uma mensagem inicial
atualizar_resultados("Digite o nome de um jogador para iniciar a busca.")

# Inicia a interface gráfica
root.mainloop()
