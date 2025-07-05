import csv

class LeitorCSV:
    def __init__(self,arquivo_caminho):
        self.caminho = arquivo_caminho

    def ler_arquivo(self):
        try:
            with open(self.caminho, newline='', encoding='utf-8') as arquivo:
                Leitor = csv.reader(arquivo)
                lista = []
                for linha_csv in Leitor:
                    lista.append(linha_csv)
                return lista
        except FileNotFoundError:
            print(f'Arquivo não encontrado: {self.caminho}')
            return []


# Exemplo de aplicação de uso:
if __name__ == '__main__':
    caminho = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'
    leitor = LeitorCSV(caminho)
    dados = leitor.ler_arquivo()
    for linha in dados:
        print(linha)
