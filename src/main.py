from models.pessoa import Pessoa
from repo.csv_repo import LeitorCSV

# Caminho do arquivo CSV
caminho = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'

# Lê os dados
dados = LeitorCSV(caminho).ler_arquivo()

# Cria os objetos Pessoa
pessoas = [Pessoa(dado) for dado in dados]

# Imprime os dados formatados
for i, pessoa in enumerate(pessoas, start=1):
    print(f"Pessoa {i}")
    print(f"Nome completo: {pessoa.nomeCompleto}")
    print(f"Primeiro nome: {pessoa.primeiroNome}")
    print(f"Segundo nome: {pessoa.segundoNome}")
    print(f"Email: {pessoa.email}")
    print(f"Celular: {pessoa.celular}")
    print(f"CPF: {pessoa.cpf}")
    print(f"CEP: {pessoa.cep}")
    print(f"Interesse: {pessoa.interesse}")
    print("-" * 50)
