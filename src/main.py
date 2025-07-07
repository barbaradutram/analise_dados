import csv
import json
from models.pessoa import Pessoa
from models.endereco import CEP, Celular
from services.gender_service import GenderService  

def main():
    caminho = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\lista_clientes.csv'
    caminho_saida = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\usuarios_formatados.json'

    gender_service = None  #roda o gender_service

    usuarios = []

    with open(caminho, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for i, linha in enumerate(leitor, start=1):
            pessoa = Pessoa(linha)

            # executa genero

            cep = CEP(pessoa.cep)
            celular = Celular(pessoa.celular, cep)

            observacoes = pessoa.observacoes + celular.observacoes
            obs_str = "; ".join(observacoes) if observacoes else "Nenhuma"

            usuario = {
                "nome_completo": pessoa.nomeCompleto,
                "primeiro_nome": pessoa.nomePrincipal,
                "segundo_nome": pessoa.segundoNome if pessoa.segundoNome else "",
                "genero": pessoa.genero,
                "email": pessoa.email,
                "celular": str(celular),
                "interesse": pessoa.interesse,
                "cpf": pessoa.cpf_str,
                "bairro": cep.bairro,
                "cidade": cep.cidade,
                "estado": cep.estado,
                "observacoes": obs_str
            }

            usuarios.append(usuario)

    # Ordenar por nome completo
    usuarios.sort(key=lambda x: x["nome_completo"])

    # Criar estrutura final
    saida = {"users": usuarios}

    # Gerar arquivo JSON
    with open(caminho_saida, 'w', encoding='utf-8') as json_file:
        json.dump(saida, json_file, ensure_ascii=False, indent=2)

    print(f"Arquivo JSON gerado com sucesso em: {caminho_saida}")

if __name__ == "__main__":
    main()