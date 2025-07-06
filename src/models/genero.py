import csv
import requests
import unicodedata
import os
from dotenv import load_dotenv

# Carrega variáveis do .env (se houver)
load_dotenv()

class Pessoa:
    def __init__(self, info: dict):
        self.nomeCompleto = info.get('NomeCompleto', '')
        self.email = info.get('Email', '')
        self.celular = info.get('Celular', '')
        self.cpf = info.get('CPF', '')
        self.cep = info.get('CEP', '')
        self.interesse = info.get('Interesse', '')
        self.nomePrincipal = ''
        self.segundoNome = ''
        self.bairro = ''
        self.cidade = ''
        self.estado = ''
        self.genero = 'desconhecido'
        self.tratar_nomes()
        self.inferir_genero()

    def tratar_nomes(self) -> str:
        preposicoes_nomes = {
            "de", "da", "do", "dos", "das", "em", "no", "na", "nos", "nas", 'e'
        }

        palavras = self.nomeCompleto.lower().split()
        nome_formatado = []

        for palavra in palavras:
            if palavra in preposicoes_nomes:
                nome_formatado.append(palavra)
            else:
                nome_formatado.append(palavra.capitalize())

        self.nomeCompleto = " ".join(nome_formatado)

        nomes = self.nomeCompleto.split()
        index = 0

        while index < len(nomes):
            if nomes[index].lower() not in preposicoes_nomes:
                self.nomePrincipal = nomes[index]
                break
            index += 1

        index += 1
        segundo_nome_partes = []
        while index < len(nomes):
            segundo_nome_partes.append(nomes[index])
            if nomes[index].lower() not in preposicoes_nomes:
                break
            index += 1

        self.segundoNome = ' '.join(segundo_nome_partes).strip()
        return self.nomeCompleto

    def inferir_genero(self):
        nome = self._normalizar_nome(self.nomePrincipal)
        if not nome:
            self.genero = "desconhecido"
            return

        # Usa chave de API se estiver disponível
        api_key = os.getenv("GENDERIZE_API_KEY")
        url = f"https://api.genderize.io/?name={nome}"
        if api_key:
            url += f"&apikey={api_key}"

        try:
            response = requests.get(url, timeout=5)
            if response.ok:
                dados = response.json()
                # print(f"Resposta da API: {dados}")  # Descomente para depurar
                self.genero = dados.get("gender", "desconhecido") or "desconhecido"
            else:
                self.genero = "erro"
        except requests.RequestException:
            self.genero = "erro"

    def _normalizar_nome(self, nome):
        nome = nome.strip().lower()
        return unicodedata.normalize('NFD', nome).encode('ascii', 'ignore').decode('utf-8')

def carregar_pessoas_csv(caminho_arquivo):
    pessoas = []
    with open(caminho_arquivo, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            pessoa = Pessoa(linha)
            pessoas.append(pessoa)
    return pessoas

# Exemplo de uso
if __name__ == "__main__":
    caminho = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'
    lista_pessoas = carregar_pessoas_csv(caminho)

    for pessoa in lista_pessoas:
        print(f"Nome completo formatado: {pessoa.nomeCompleto}")
        print(f"Nome Principal: {pessoa.nomePrincipal} {pessoa.segundoNome}")
        print(f"Gênero inferido: {pessoa.genero.capitalize()}")
        print("---")