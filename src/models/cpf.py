import csv

class CPF:
    def __init__(self, numero: str):
        self.numero = self._somente_digitos(numero)
        self.valido = self._validar()
        self.observacao = ''
    
        if not self.valido:
            self.observacao = 'CPF inválido.'


    def _somente_digitos(self, cpfNumb: str) -> str:
        return ''.join(filter(str.isdigit, cpfNumb))

    def _validar(self) -> bool:
        cpfNumb = self.numero
        if len(cpfNumb) != 11 or cpfNumb== cpfNumb[0] * 11:
            return False

        for i in range(9, 11):
            soma = sum(int(cpfNumb[j]) * ((i + 1) - j) for j in range(i))
            digito = (soma * 10 % 11) % 10
            if digito != int(cpfNumb[i]):
                return False

        return True

    def __str__(self):
        return self.numero

# Exemplo de uso:
if __name__ == "__main__":
    caminho = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'

    with open(caminho, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            nome = linha.get("NomeCompleto", "Desconhecido")
            cpf_str = linha.get("CPF", "")
            cpf = CPF(cpf_str)

            print(f"Nome: {nome}")
            print(f"CPF: {cpf}")
            print(f"Válido? {'Sim' if cpf.valido else 'Não'}")
            print(f"Observação: {cpf.observacao}")
            print("-" * 50)

