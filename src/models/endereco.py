import csv
import re
import requests

 #inicializa uma instância da classe CEP com os dados fornecidos no endereço.
class CEP:
    def __init__(self, cep_raw):
        self.cep = self._formatar_cep(cep_raw)
        self.bairro = ''
        self.cidade = ''
        self.estado = ''
        self.ddd = ''
        self.valido = self._validar_cep()
        if self.valido:
            self._consultar_via_cep()

    def _formatar_cep(self, cep_raw):
        return re.sub(r'\D', '', cep_raw)

    def _validar_cep(self):
        return len(self.cep) == 8 and self.cep.isdigit()


 #textes de cep
    def _consultar_via_cep(self):
        url = f"https://viacep.com.br/ws/{self.cep}/json/"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                dados = response.json()
                if not dados.get("erro"):
                    self.bairro = dados.get("bairro", "")
                    self.cidade = dados.get("localidade", "")
                    self.estado = dados.get("uf", "")
                    self.ddd = self._consultar_ddd()
                else:
                    self.valido = False
        except requests.RequestException:
            self.valido = False

    def _consultar_ddd(self):
        url = f"https://brasilapi.com.br/api/cep/v1/{self.cep}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                dados = response.json()
                return dados.get('ddd', '')
        except requests.RequestException:
            return ''
        return ''

    def __str__(self):
        if self.valido:
            return f"{self.cep} - {self.bairro}, {self.cidade} - {self.estado}"
        return f"{self.cep} (inválido)"


class Celular:
    def __init__(self, celular_raw, cep_obj):
        self.raw = celular_raw
        self.cep_obj = cep_obj
        self.numero_formatado = ''
        self.observacoes = []
        self.formatar()

    def formatar(self):
        telefone = re.sub(r'\D', '', self.raw)

        if not telefone:
            self.observacoes.append('Telefone vazio')
            return

        # Se tiver 8 dígitos: adicionar 9 e DDD
        if len(telefone) == 8:
            telefone = '9' + telefone
            if self.cep_obj.ddd:
                telefone = self.cep_obj.ddd + telefone
            else:
                self.observacoes.append('DDD ausente e não encontrado')
                self.numero_formatado = telefone
                return

        # Se tiver 9 dígitos e começar com 9: adicionar DDD
        elif len(telefone) == 9 and telefone.startswith('9'):
            if self.cep_obj.ddd:
                telefone = self.cep_obj.ddd + telefone
            else:
                self.observacoes.append('DDD ausente e não encontrado')
                self.numero_formatado = telefone
                return

        # Se tiver 10 dígitos: inserir 9 após DDD
        elif len(telefone) == 10:
            telefone = telefone[:2] + '9' + telefone[2:]

        # Se tiver 11 dígitos: verificar se está no formato correto
        elif len(telefone) == 11:
            if telefone[2] != '9':
                telefone = telefone[:2] + '9' + telefone[2:]

        else:
            self.observacoes.append('Número inválido')
            self.numero_formatado = telefone
            return

        # Formatar como "DD 9XXXXXXXX"
        if len(telefone) == 11:
            self.numero_formatado = f"{telefone[:2]} {telefone[2:]}"
        else:
            self.observacoes.append('Número incompleto após formatação')
            self.numero_formatado = telefone

    def __str__(self):
        return self.numero_formatado if self.numero_formatado else 'Número inválido'


#exemplo de aplicação de uso
CAMINHO_CSV = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'


if __name__ == "__main__":
    with open(CAMINHO_CSV, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for i, linha in enumerate(leitor, start=1):
            nome = linha.get("NomeCompleto", "").strip()
            cep_raw = linha.get("CEP", "").strip()
            celular_raw = linha.get("Celular", "").strip()

            cep_info = CEP(cep_raw)
            endereco = f"{cep_info.bairro}, {cep_info.cidade} - {cep_info.estado}" if cep_info.valido else "Endereço inválido"

            celular = Celular(celular_raw, cep_info)

            print(f"{i:02d}. {nome} | {cep_info.cep} | {endereco} | {celular} | Observações: {', '.join(celular.observacoes)}")