import csv
from models.cpf import CPF  


 #inicializa uma instância da classe Pessoa com os dados fornecidos.
class Pessoa:
    def __init__(self, info: dict):
        self.nomeCompleto = info.get('NomeCompleto', '').strip()
        self.email = info.get('Email', '')
        self.celular = info.get('Celular', '')
        self.cpf_str = info.get('CPF', '') 
        self.cep = info.get('CEP', '')
        self.interesse = info.get('Interesse', '')
        self.nomePrincipal = ''
        self.preposicaoEntre = ''
        self.segundoNome = ''
        self.genero = 'desconhecido'

        self.observacoes = []

        self.tratar_nomes()
        self.cpf = CPF(self.cpf_str)  #instancia CPF
        self.validar_campos()


#Formata os nomes e indentificar
    def tratar_nomes(self) -> str:
        preposicoes = {"de", "da", "do", "dos", "das", "em", "no", "na", "nos", "nas", "e"}
        palavras = self.nomeCompleto.lower().split()
        nome_formatado = []

        for palavra in palavras:
            if palavra in preposicoes:
                nome_formatado.append(palavra)
            else:
                nome_formatado.append(palavra.capitalize())

        self.nomeCompleto = " ".join(nome_formatado)

        nomes = self.nomeCompleto.split()
        if nomes:
            self.nomePrincipal = nomes[0]
            self.preposicaoEntre = ''
            self.segundoNome = ''

            i = 1
            while i < len(nomes):
                if nomes[i].lower() in preposicoes:
                    self.preposicaoEntre = nomes[i]
                    i += 1
                    if i < len(nomes) and nomes[i].lower() not in preposicoes:
                        self.segundoNome = nomes[i]
                        break
                else:
                    self.segundoNome = nomes[i]
                    break
                i += 1

        return self.nomeCompleto

#Formata e reduz o nome original
    def nome_reduzido(self) -> str:
        if self.segundoNome:
            if self.preposicaoEntre:
                return f"{self.nomePrincipal} {self.preposicaoEntre} {self.segundoNome}"
            else:
                return f"{self.nomePrincipal} {self.segundoNome}"
        else:
            return self.nomePrincipal

    def validar_campos(self):
        #validar da classe CPF
        if not self.cpf.valido:
            self.observacoes.append(self.cpf.observacao)

        if not self.celular or len(''.join(filter(str.isdigit, self.celular))) < 8:
            self.observacoes.append("Telefone ausente ou inválido")

        if not self.cep or len(''.join(filter(str.isdigit, self.cep))) != 8:
            self.observacoes.append("CEP inválido")

def carregar_pessoas_csv(caminho_arquivo):
    pessoas = []
    with open(caminho_arquivo, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            pessoa = Pessoa(linha)
            pessoas.append(pessoa)
    return pessoas


if __name__ == "__main__":
    caminho = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'
    lista_pessoas = carregar_pessoas_csv(caminho)

    for pessoa in lista_pessoas:
        obs = ", ".join(pessoa.observacoes) if pessoa.observacoes else "Nenhuma"
        print(f'Nome: {pessoa.nome_reduzido()} | Observações: {obs}')
