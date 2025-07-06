import csv

class CPF:
    #Classe para formatar e validar números de CPF 

    def __init__(self, numero: str):
        self.numero = self._somente_digitos(numero)
        self.valido = self._validar()
        self.observacao = ''

        if not self.valido:
            self.observacao = 'CPF inválido.'


    def _somente_digitos(self, cpf_number: str) -> str:
        return ''.join(filter(str.isdigit, cpf_number))

    def _validar(self) -> bool:
        cpf_number = self.numero
        if len(cpf_number) != 11 or cpf_number == cpf_number[0] * 11:
            return False

        for i in range(9, 11):
            soma = sum(int(cpf_number[j]) * ((i + 1) - j) for j in range(i))
            digito = (soma * 10 % 11) % 10
            if digito != int(cpf_number[i]):
                return False

        return True

    def __str__(self):
        return self.numero

# Exemplo de aplicação de uso:
if __name__ == "__main__":
    CAMINHO = (
    r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'
)
    with open(CAMINHO, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            nome = linha.get("NomeCompleto", "Desconhecido")
            cpf_str = linha.get("CPF", "")
            cpf_obj = CPF(cpf_str)

            print(f"Nome: {nome}")
            print(f"CPF: {cpf_obj} - {'Válido' if cpf_obj.valido else 'Inválido'}")
            if cpf_obj.observacao:
                print(f"Observação: {cpf_obj.observacao}")