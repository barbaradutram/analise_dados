import csv

class Pessoa:
    def __init__(self, info: dict):
        self.nomeCompleto = info.get('NomeCompleto', '')
        self.email = info.get('Email', '')
        self.celular = info.get('Celular', '')
        self.cpf = info.get('CPF', '')
        self.cep = info.get('CEP', '')
        self.interesse = info.get('Interesse', '')
        self.primeiroNome = ''
        self.segundoNome = ''
        self.bairro = ''
        self.cidade = ''
        self.estado = ''
        self.genero = ''
        self.tratar_nomes()

    def tratar_nomes(self) -> str:
        preposicoes_nomes = {
        "de", "da", "do", "dos", "das", "em", "no", "na", "nos", "nas", "e"
    }
        palavras = self.nomeCompleto.lower().split()
        nome_formatado = []
        nomes_principais = []

        for palavra in palavras:
            if palavra in preposicoes_nomes:
                nome_formatado.append(palavra)
            else:
                capitalizada = palavra.capitalize()
                nome_formatado.append(capitalizada)
                nomes_principais.append(capitalizada)
            

        self.nomeCompleto = " ".join(nome_formatado)


    # Extrai primeiro e segundo nomes ignorando preposições
        if nomes_principais:
            self.primeiroNome = nomes_principais[0]
            if len(nomes_principais) > 1:
                self.segundoNome = nomes_principais[1]

        return self.nomeCompleto


def carregar_pessoas_csv(caminho_arquivo):
    pessoas = []
    with open(caminho_arquivo, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            nomepessoa = Pessoa(linha)
            pessoas.append(nomepessoa)
    return pessoas


# Exemplo de uso:
if __name__ == "__main__":
    caminho = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'
    lista_pessoas = carregar_pessoas_csv(caminho)

    for pessoa in lista_pessoas:
        print("Nome completo formatado:", pessoa.nomeCompleto)
        print("Primeiro nome:", pessoa.primeiroNome)
        print("Segundo nome:", pessoa.segundoNome)
        print("---")