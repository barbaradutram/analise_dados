import json
from collections import Counter

#Mapear estados para regiões
def obter_regiao(estado):
    regioes = {
        'Norte': {'AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'},
        'Nordeste': {'AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'},
        'Centro-Oeste': {'DF', 'GO', 'MT', 'MS'},
        'Sudeste': {'ES', 'MG', 'RJ', 'SP'},
        'Sul': {'PR', 'RS', 'SC'}
    }
    for regiao, estados in regioes.items():
        if estado in estados:
            return regiao
    return 'Desconhecida'

#CarregarJSON
caminho_json = r'C:\Users\barba\OneDrive\Documentos\Next\BARBARA\next\analise_dados\data\usuarios_formatados.json'

with open(caminho_json, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

usuarios = dados['users']

#contadores
total_usuarios = len(usuarios)
genero_contador = Counter()
regiao_contador = Counter()
cpf_invalidos = 0
telefone_invalidos = 0
interesse_contador = Counter()
interesse_por_genero = {}

#Processar usuário
for usuario in usuarios:
    genero = usuario['genero'].lower()
    estado = usuario['estado']
    interesse = usuario['interesse']
    observacoes = usuario['observacoes']

    genero_contador[genero] += 1
    regiao = obter_regiao(estado)
    regiao_contador[regiao] += 1
    interesse_contador[interesse] += 1

    if genero not in interesse_por_genero:
        interesse_por_genero[genero] = Counter()
    interesse_por_genero[genero][interesse] += 1

    if 'CPF Inválido' in observacoes:
        cpf_invalidos += 1
    if 'Telefone ausente ou inválido' in observacoes:
        telefone_invalidos += 1

#calcular percentual
def percentual(parte, total):
    return round((parte / total) * 100, 2) if total > 0 else 0

# Relatório
print("\n===== RELATÓRIO DE ANÁLISE DOS DADOS =====\n")

print("🔹 Distribuição de Gênero:")
for genero, quantidade in genero_contador.items():
    print(f"  {genero.capitalize()}: {quantidade} usuários ({percentual(quantidade, total_usuarios)}%)")

print("\n🔹 Distribuição Geográfica:")
for regiao, quantidade in regiao_contador.items():
    print(f"  {regiao}: {quantidade} usuários ({percentual(quantidade, total_usuarios)}%)")

print("\n🔹 Qualidade dos Dados:")
print(f"  CPFs Inválidos: {cpf_invalidos} ({percentual(cpf_invalidos, total_usuarios)}%)")
print(f"  Telefones Ausentes ou Inválidos: {telefone_invalidos} ({percentual(telefone_invalidos, total_usuarios)}%)")

print("\n🔹 Percentual das Áreas de Interesse (Geral):")
for interesse, quantidade in interesse_contador.items():
    print(f"  {interesse}: {quantidade} usuários ({percentual(quantidade, total_usuarios)}%)")

print("\n🔹 Áreas de Interesse por Gênero:")
for genero, interesses in interesse_por_genero.items():
    print(f"\n  {genero.capitalize()}:")
    total_genero = sum(interesses.values())
    for interesse, quantidade in interesses.items():
        print(f"    {interesse}: {quantidade} usuários ({percentual(quantidade, total_genero)}%)")

print("\n==========================================\n")