from pathlib import Path
import csv
import os
from tkinter import Tk, filedialog

# criação de "interface gráfica" para solucionar problema de path dinâmico
Tk().withdraw()  
pasta = filedialog.askdirectory(title="Selecione a pasta onde estão os CSVs")

if not pasta:
    raise Exception("Nenhuma pasta foi selecionada") 
    exit()

pasta = Path(pasta)
pathTXT = pasta/"resultado.txt"
arquivos_csv = list(pasta.glob("*.csv"))

if not arquivos_csv:
    raise FileNotFoundError("A pasta selecionada não contém arquivos CSV.")

# variáveis para os cálculos globais

# lista com todas as médias dos alunos de todas as turmas
todas_medias = []  
# total de alunos de todas as turmas
total_alunos_geral = 0   
# total de alunos aprovados 
total_aprovados_geral = 0  
# lista para controlar alunos e suas disciplinas e aprovação
alunos_lista = []          
# Lista para guardar dados das disciplinas: [cod_turma, nome_disciplina, total_alunos, total_matriculas, total_aprovados]
disciplinas_lista = []

with open(pathTXT, "w", encoding="utf-8") as resultado:
    for arquiv in arquivos_csv:
        with open(arquiv, "r", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)

            cabecalho = next(leitor)
            cod_turma = cabecalho[0].strip()
            nome_disciplina = cabecalho[1].strip()

            config = next(leitor)
            media_minima = float(config[0].strip())
            peso_av1 = int(config[1].strip())
            peso_av2 = int(config[2].strip())
            peso_av3 = int(config[3].strip())

# soma dos pesos para encontrar média ponderada

            soma_pesos = peso_av1 + peso_av2 + peso_av3

# variáveis para calcular médias e aprovações na turma

            medias_alunos = []
            total_alunos = 0
            total_aprovados = 0

            for linha in leitor:
                total_alunos += 1
                matricula = linha[0].strip()
                av1 = float(linha[1].strip())
                av2 = float(linha[2].strip())
                av3 = float(linha[3].strip())

                media = (av1 * peso_av1 + av2 * peso_av2 + av3 * peso_av3) / soma_pesos
                medias_alunos.append(media)

# valor booleano para variável aprovado 

                aprovado = media >= media_minima
                if aprovado:
                    total_aprovados += 1

# Atualizar lista geral de alunos (matricula, [turmas], [medias], [aprovado])

                encontrou = False
                for aluno in alunos_lista:
                    if aluno[0] == matricula:
                        aluno[1].append(cod_turma)
                        aluno[2].append(media)
                        aluno[3].append(aprovado)
                        encontrou = True
                        break
                if not encontrou:
                    alunos_lista.append([matricula, [cod_turma], [media], [aprovado]])

# Atualiza dados globais com os dados de turma por turma 

            todas_medias.extend(medias_alunos)
            total_alunos_geral += total_alunos
            total_aprovados_geral += total_aprovados

            percentual_aprovados = (total_aprovados / total_alunos) * 100
            media_turma = sum(medias_alunos) / total_alunos 
            alunos_acima_media = sum(1 for m in medias_alunos if m > media_turma)
            maior_media = max(medias_alunos) 
            menor_media = min(medias_alunos) 

# Guarda dados da disciplina para depois analisar taxa aprovação
# obs: os indices 2 e 3 possuem o mesmo valor pois são total_alunos (contador) e total_matriculas

            disciplinas_lista.append([cod_turma, nome_disciplina, total_alunos, total_alunos, total_aprovados])

# Escrever resultado da turma
            resultado.write(f"TURMA: {cod_turma} - {nome_disciplina}\n")
            resultado.write(f"Total de alunos: {total_alunos}, Percentual de alunos aprovados: {percentual_aprovados:.2f}%\n")
            resultado.write(f"Média da turma: {media_turma:.2f}, Alunos acima da média: {alunos_acima_media}\n")
            resultado.write(f"Maior média: {maior_media:.2f}, Menor média: {menor_media:.2f}\n")
            resultado.write("-" * 50 + "\n\n")

# média global e percentual de aprovação do professor

    media_global = sum(todas_medias) / len(todas_medias) 
    percentual_aprovados_global = (total_aprovados_geral / total_alunos_geral) * 100 

# Quantidade de alunos matriculados em mais de 2 disciplinas
    alunos_mais_2 = sum(1 for aluno in alunos_lista if len(aluno[1]) > 2)

# Quantidade e percentual de alunos aprovados em todas as disciplinas que estavam matriculados
    alunos_aprovados_todas = 0
    for aluno in alunos_lista:
        if all(aluno[3]):
            alunos_aprovados_todas += 1
    percentual_aprovados_todas = (alunos_aprovados_todas / len(alunos_lista)) * 100 

# Disciplinas com maior e menor taxa de aprovação

    maior_taxa = -1
    menor_taxa = 101
    nome_maior = ""
    nome_menor = ""

# obs: disc[4] -> Total de Aprovados / disc[2] -> total de alunos nessa disciplina

    for disc in disciplinas_lista:
        taxa = (disc[4] / disc[2]) * 100 if disc[2] > 0 else 0
        if taxa > maior_taxa:
            maior_taxa = taxa
            nome_maior = disc[1]
        if taxa < menor_taxa:
            menor_taxa = taxa
            nome_menor = disc[1]

    resultado.write("Resumo geral do professor:\n")
    resultado.write(f"Média global da turma: {media_global:.2f}\n")
    resultado.write(f"Percentual global de aprovados: {percentual_aprovados_global:.2f}%\n")
    resultado.write(f"Alunos matriculados em mais de 2 disciplinas: {alunos_mais_2}\n")
    resultado.write(f"Alunos aprovados em todas as disciplinas: {alunos_aprovados_todas} ({percentual_aprovados_todas:.2f}%)\n")
    resultado.write(f"Disciplina com maior taxa de aprovação: {nome_maior} ({maior_taxa:.2f}%)\n")
    resultado.write(f"Disciplina com menor taxa de aprovação: {nome_menor} ({menor_taxa:.2f}%)\n")
    resultado.write("-" * 50 + "\n\n")

# Estatísticas por aluno

    resultado.write("\nEstatísticas por aluno:\n")
    for aluno in alunos_lista:
        matricula = aluno[0]
        turmas = aluno[1]
        medias = aluno[2]
        aprovados = aluno[3]

        total_disciplinas = len(turmas)
        total_aprovacoes = sum(1 for ap in aprovados if ap)
        taxa_aprovacao = (total_aprovacoes / total_disciplinas) * 100 if total_disciplinas > 0 else 0

        melhor_media = max(medias) 
        pior_media = min(medias) 

        melhores = []
        piores = []

        for i, media in enumerate(medias):
            cod = turmas[i]
            nome_disc = ""
            for disc in disciplinas_lista:
                if disc[0] == cod:
                    nome_disc = disc[1]
                    break
            if media == melhor_media:
                melhores.append((nome_disc, media))
            if media == pior_media:
                piores.append((nome_disc, media))

        resultado.write(f"Aluno {matricula}:\n")
        resultado.write(f"  Taxa de aprovação: {taxa_aprovacao:.2f}% ({total_aprovacoes}/{total_disciplinas})\n")
        resultado.write(f"  Melhor média em:\n")
        for disc_nome, media_val in melhores:
            resultado.write(f"    - {disc_nome}: {media_val:.2f}\n")
        resultado.write(f"  Pior média em:\n")
        for disc_nome, media_val in piores:
            resultado.write(f"    - {disc_nome}: {media_val:.2f}\n")
        resultado.write("\n")

print("Arquivo 'resultado.txt' gerado com sucesso!")
os.startfile(pathTXT)
