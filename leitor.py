from pathlib import Path
import csv
import os
from tkinter import Tk, filedialog

# minimiza a janela padrão do tkinter
Tk().withdraw()  
# Abrir janela para selecionar a pasta
pasta = filedialog.askdirectory(title="Selecione a pasta onde estão os CSVs")

if not pasta:
    raise Exception("Nenhuma pasta foi selecionada") 
    exit()

# Converter para objeto Path
pasta = Path(pasta)

# Path onde criar e ler o arquivo txt
caminhoTXT = pasta/"resultado.txt"

# lista com todos os arquivos do path dinâmico
arquivos_csv = list(pasta.glob("*.csv"))

# Abrir arquivo de resultado para escrita
with open(caminhoTXT, "w", encoding="utf-8") as resultado:
    if not arquivos_csv:
        raise FileNotFoundError("A pasta selecionada não contém arquivos CSV.")
   
# Percorrer todos os arquivos CSV da pasta
    for caminho in arquivos_csv:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            leitor1 = csv.reader(arquivo)

            # Ler dados iniciais
            cabecalho = next(leitor1)
            cod_turma = cabecalho[0].strip()
            nome_disciplina = cabecalho[1].strip()

            # Ler dados da segunda linha
            config = next(leitor1)
            media_minima = float(config[0].strip())
            peso_av1 = int(config[1].strip())
            peso_av2 = int(config[2].strip())
            peso_av3 = int(config[3].strip())

            soma_pesos = peso_av1 + peso_av2 + peso_av3

            # Processar alunos
            medias_alunos = []
            total_alunos = 0
            total_aprovados = 0

            for linha in leitor1:
                total_alunos += 1

                matricula = linha[0].strip()
                av1 = float(linha[1].strip())
                av2 = float(linha[2].strip())
                av3 = float(linha[3].strip())

                media = (av1 * peso_av1 + av2 * peso_av2 + av3 * peso_av3) / soma_pesos
                medias_alunos.append(media)

                if media >= media_minima:
                    total_aprovados += 1

            media_turma = sum(medias_alunos) / total_alunos if total_alunos > 0 else 0
            alunos_acima_media = sum(1 for m in medias_alunos if m > media_turma)

            maior_media = max(medias_alunos) if medias_alunos else 0
            menor_media = min(medias_alunos) if medias_alunos else 0

            percentual_aprovados = (total_aprovados / total_alunos) * 100 if total_alunos > 0 else 0

            # Escrever no arquivo de resultado
            resultado.write(f"TURMA: {cod_turma} - {nome_disciplina}\n")
            resultado.write(f"a) Total de alunos: {total_alunos}, Percentual de aprovados: {percentual_aprovados:.2f}%\n")
            resultado.write(f"b) Média da turma: {media_turma:.2f}, Alunos acima da média: {alunos_acima_media}\n")
            resultado.write(f"c) Maior média: {maior_media:.2f}, Menor média: {menor_media:.2f}\n")
            resultado.write("-" * 50 + "\n\n")

print("Arquivo 'resultado.txt' gerado com sucesso!")
os.startfile(caminhoTXT)  
