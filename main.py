import numpy as np
import csv
import os
import math
import tools.tools as t
from classes.files import DadosExperimento

alunos = ['Nelson', 'Patrick', 'Gabriel', 'Ian', 'Henrique']
arquivo_medicoes = csv.reader(open('data/medicoes.txt', 'r'), delimiter='\t')
arquivo_massas = csv.reader(open('data/massas.txt', 'r'), delimiter='\t')

dados_experimento = DadosExperimento()

t.extrair_dados_medicao(dados_experimento, arquivo_medicoes)
t.extrair_dados_massa(dados_experimento, arquivo_massas)

for objeto in dados_experimento.medicoes:
    os.makedirs(f'output/latex/medicoes/', exist_ok=True)
    with open(f'output/latex/medicoes/{objeto}.tex', 'w') as arquivo:
        t.criar_tabela_latex(arquivo, 'c', 6)
        
        # Cabeçalho
        linha = 'Medição nº & '
        for aluno_index in range(5):
            linha += t.shortsack(
                alunos[aluno_index],
                t.instrumento(dados_experimento, objeto, aluno_index), t.italic(f"(± {t.str_media(t.erro(dados_experimento, objeto, aluno_index), t.contar_casas_decimais(t.erro(dados_experimento, objeto, aluno_index)))} mm)")
            )
            linha = t.handle_espaço(linha, aluno_index)
        arquivo.write(linha + '\\\\\n')
        arquivo.write('\\midrule\n')
                
        # Dados
        for numero_medicao in range(10):
            linha = f'{numero_medicao+1} & '
            for aluno_index in range(5):
                medicao = t.medicao(dados_experimento, objeto, aluno_index, numero_medicao)
                erro = t.erro(dados_experimento, objeto, aluno_index)
                casas_decimais = t.contar_casas_decimais(erro)
                linha += t.str_media(medicao, casas_decimais)
                linha = t.handle_espaço(linha, aluno_index)
            arquivo.write(linha + '\\\\\n')
        arquivo.write('\\midrule\n')
        
        # Cabeçalho 2
        linha = '&'
        for aluno_index in range(5):
            instrumento = t.instrumento(dados_experimento, objeto, aluno_index)
            linha += t.shortsack(alunos[aluno_index], f'({instrumento})', t.italic(f'(mm)'))
            linha = t.handle_espaço(linha, aluno_index)
        arquivo.write(linha + '\\\\\n')
        arquivo.write('\\midrule\n')
        
        # Média
        linha = 'Média & '
        for aluno_index in range(5):
            media = t.med(t.dados(dados_experimento, objeto, aluno_index))
            erro = t.erro(dados_experimento, objeto, aluno_index)
            casas_decimais = t.contar_casas_decimais(erro)
            linha += t.str_media(media, casas_decimais)
            linha = t.handle_espaço(linha, aluno_index)
        arquivo.write(linha + '\\\\[3pt]\n')
        
        # Desvio Padrão da Média
        linha = t.shortsack('Desvio', 'Padrão da', 'Média') + ' & '
        for aluno_index in range(5):
            desvio_padrao_media = t.desvpadmed(t.dados(dados_experimento, objeto, aluno_index))
            erro = t.erro(dados_experimento, objeto, aluno_index)
            casas_decimais = t.contar_casas_decimais(erro)
            linha += t.str_media(desvio_padrao_media, casas_decimais)
            linha = t.handle_espaço(linha, aluno_index)
        arquivo.write(linha + '\\\\[3pt]\n')
        
        # Incerteza
        linha = 'Incerteza & '
        for aluno_index in range(5):
            desvio_padrao_media = t.desvpadmed(t.dados(dados_experimento, objeto, aluno_index))
            erro = t.erro(dados_experimento, objeto, aluno_index)
            incerteza = t.sqrt_sum_sqr(desvio_padrao_media, erro)
            casas_decimais = t.contar_casas_decimais(erro, incerteza)
            linha += t.str_media(incerteza, casas_decimais)
            linha = t.handle_espaço(linha, aluno_index)
        arquivo.write(linha + '\\\\\n')        
        t.terminar_tabela_latex(arquivo)
        
for objeto in dados_experimento.massas:
    os.makedirs(f'output/latex/grandezas/', exist_ok=True)
    with open(f'output/latex/grandezas/{objeto}.tex', 'w') as arquivo:
        t.criar_tabela_latex(arquivo, 'c', 6)
        
        # Cabeçalho
        linha_cabecalho = 'Grandeza & '
        for aluno_index in range(5):
            linha_cabecalho += alunos[aluno_index]
            linha_cabecalho = t.handle_espaço(linha_cabecalho, aluno_index)
        arquivo.write(linha_cabecalho + '\\\\\n')
        arquivo.write('\\midrule\n')
        
        # Grandeza | Nelson | ... | Henrique
        
        # Comprimento
        linha_comprimento = t.shortsack('Comprimento', t.italic('(mm)')) + ' & '
        for aluno_index in range(5):
            if objeto != 'Barra' and objeto != 'Barrinha':
                media = t.med(t.dados(dados_experimento, objeto, aluno_index))
                erro = t.erro(dados_experimento, objeto, aluno_index)
                desvio_padrao_media = t.desvpadmed(t.dados(dados_experimento, objeto, aluno_index))
                incerteza = t.sqrt_sum_sqr(desvio_padrao_media, erro)
                linha_comprimento += t.str_media_incerteza(media, incerteza)
                linha_comprimento = t.handle_espaço(linha_comprimento, aluno_index)
            else:
                media_x = t.med(t.dados(dados_experimento, objeto+'_x', aluno_index))
                media_y = t.med(t.dados(dados_experimento, objeto+'_y', aluno_index))
                media_z = t.med(t.dados(dados_experimento, objeto+'_z', aluno_index))
                desvio_padrao_media_x = t.desvpadmed(t.dados(dados_experimento, objeto+'_x', aluno_index))
                desvio_padrao_media_y = t.desvpadmed(t.dados(dados_experimento, objeto+'_y', aluno_index))
                desvio_padrao_media_z = t.desvpadmed(t.dados(dados_experimento, objeto+'_z', aluno_index))
                erro_x = t.erro(dados_experimento, objeto+'_x', aluno_index)
                erro_y = t.erro(dados_experimento, objeto+'_y', aluno_index)
                erro_z = t.erro(dados_experimento, objeto+'_z', aluno_index)
                incerteza_x = t.sqrt_sum_sqr(desvio_padrao_media_x, erro_x)
                incerteza_y = t.sqrt_sum_sqr(desvio_padrao_media_y, erro_y)
                incerteza_z = t.sqrt_sum_sqr(desvio_padrao_media_z, erro_z)
                casas_decimais = t.contar_casas_decimais(erro_x, erro_y, erro_z, incerteza_x, incerteza_y, incerteza_z)
                linha_comprimento += t.shortsack('x: ' + t.str_media_incerteza(media_x, incerteza_x), 'y: ' + t.str_media_incerteza(media_y, incerteza_y), 'z: ' + t.str_media_incerteza(media_z, incerteza_z))
                linha_comprimento = t.handle_espaço(linha_comprimento, aluno_index)
        arquivo.write(linha_comprimento + '\\\\[4pt]\n')
        
        # Massa
        massas = []
        incertezas_massas = []
        linha_massa = t.shortsack('Massa', t.italic('(g)')) + ' & '
        for aluno_index in range(5):
            dados = t.dados(dados_experimento, objeto, aluno_index, 'massas')
            media = t.med(dados)
            erro = t.erro(dados_experimento, objeto, aluno_index, 'massas')
            desvio_padrao_media = t.desvpadmed(dados)
            incerteza = t.sqrt_sum_sqr(desvio_padrao_media, erro)
            massas.append(media)
            incertezas_massas.append(incerteza)
            linha_massa += t.str_media_incerteza(media, incerteza)
            linha_massa = t.handle_espaço(linha_massa, aluno_index)
        arquivo.write(linha_massa + '\\\\[4pt]\n')
        
        # Volume
        volumes = []
        incertezas_volumes = []
        linha_volume = t.shortsack('Volume', t.italic('(cm³)')) + ' & '
        for aluno_index in range(5):
            if objeto != 'Barra' and objeto != 'Barrinha':
                dados = t.dados(dados_experimento, objeto, aluno_index)
                dados = [item / 10 for item in dados]
                media = t.med(dados)
                desvio_padrao_media = t.desvpadmed(dados)
                volume = media**3
                desvio_padrao_volume = volume * 3 * desvio_padrao_media / media
                if objeto == 'Bola':
                    desvio_padrao_volume = (4/3) * math.pi * desvio_padrao_volume
                    volume = (1/6) * math.pi * volume
                erro = t.erro(dados_experimento, objeto, aluno_index) / 10
                incerteza = t.sqrt_sum_sqr(desvio_padrao_media, erro)
                volumes.append(volume)
                incertezas_volumes.append(incerteza)
                linha_volume += t.str_media_incerteza(volume, incerteza)
                linha_volume = t.handle_espaço(linha_volume, aluno_index)
            else:
                dados_x = t.dados(dados_experimento, objeto+'_x', aluno_index)
                dados_y = t.dados(dados_experimento, objeto+'_y', aluno_index)
                dados_z = t.dados(dados_experimento, objeto+'_z', aluno_index)
                dados_x = [item / 10 for item in dados_x]
                dados_y = [item / 10 for item in dados_y]
                dados_z = [item / 10 for item in dados_z]
                media_x = t.med(dados_x) 
                media_y = t.med(dados_y) 
                media_z = t.med(dados_z) 
                desvio_padrao_media_x = t.desvpadmed(dados_x) 
                desvio_padrao_media_y = t.desvpadmed(dados_y) 
                desvio_padrao_media_z = t.desvpadmed(dados_z) 
                erro_x = dados_experimento.medicoes[objeto+'_x'][aluno_index]['erro'] / 10
                erro_y = dados_experimento.medicoes[objeto+'_y'][aluno_index]['erro'] / 10
                erro_z = dados_experimento.medicoes[objeto+'_z'][aluno_index]['erro'] / 10
                incerteza_x = t.sqrt_sum_sqr(desvio_padrao_media_x, erro_x)
                incerteza_y = t.sqrt_sum_sqr(desvio_padrao_media_y, erro_y)
                incerteza_z = t.sqrt_sum_sqr(desvio_padrao_media_z, erro_z) 
                volume = media_x * media_y * media_z
                incerteza = t.sqrt_sum_sqr(incerteza_x/media_x, incerteza_y/media_y, incerteza_z/media_z)
                volumes.append(volume)
                incertezas_volumes.append(incerteza)
                linha_volume += t.str_media_incerteza(volume, incerteza)
                linha_volume = t.handle_espaço(linha_volume, aluno_index)
        arquivo.write(linha_volume + '\\\\[4pt]\n')
        
        # Densidade
        linha_densidade = t.shortsack('Densidade', t.italic('(kg/m³)')) + ' & '
        for aluno_index in range(5):
            densidade = massas[aluno_index] / volumes[aluno_index]
            incerteza = densidade * t.sqrt_sum_sqr(incertezas_massas[aluno_index]/ massas[aluno_index], incertezas_volumes[aluno_index]/volumes[aluno_index])
            densidade = densidade * 10**3
            incerteza = incerteza * 10**3
            linha_densidade += t.str_media_incerteza(densidade, incerteza)
            linha_densidade = t.handle_espaço(linha_densidade, aluno_index)
        arquivo.write(linha_densidade + '\\\\[4pt]\n')        
        t.terminar_tabela_latex(arquivo)

os.makedirs('output/latex/', exist_ok=True)
with open('output/latex/total.tex', 'w') as arquivo:
    t.criar_tabela_latex(arquivo, 'c', 5)
    
    # Cabeçalho
    linha = f"Objeto & {t.shortsack('Comprimento', t.italic(f'(mm)'))} & {t.shortsack('Massa', t.italic(f'(g)'))} & {t.shortsack('Volume', t.italic(f'(cm$^3$)'))} & {t.shortsack('Densidade', t.italic(f'(kg/m$^3$)'))} \\\\\n"
    arquivo.write(linha)
    arquivo.write('\\midrule\n')
    
    Barra_c = ['Barra_x', 'Barra_y', 'Barra_z']
    Barrinha_c = ['Barrinha_x', 'Barrinha_y', 'Barrinha_z']
    flag_barra = False
    flag_barrinha = False
    for objeto in dados_experimento.medicoes:
        if objeto in Barra_c:
            if not flag_barra:
                flag_barra = True
                linha = 'Barra & '
            else:
                continue
        
        elif objeto in Barrinha_c:
            if not flag_barrinha:
                flag_barrinha = True
                linha = 'Barrinha & '
            else:
                continue
        
        if (linha):
            if objeto not in Barra_c and objeto not in Barrinha_c:
                linha = f'{objeto} & '
            else:
                linha = f'{objeto[:-2]} & '

            # Comprimento
            comprimento = 0
            incerteza_comprimento = 0
            comprimento_x = 0
            comprimento_y = 0
            comprimento_z = 0
            incerteza_comprimento_x = 0
            incerteza_comprimento_y = 0
            incerteza_comprimento_z = 0
            if objeto not in Barra_c and objeto not in Barrinha_c:
                total = []
                desvios = []
                for aluno_index in range(len(alunos)):
                    total.extend(t.dados(dados_experimento, objeto, aluno_index))
                    desvios.append(t.desvpadmed(t.dados(dados_experimento, objeto, aluno_index)))
                media = t.med(total)
                erro = t.erro_total(*[t.erro(dados_experimento, objeto, aluno_index) for aluno_index in range(5)])
                desvio_padrao_media = t.sqrt_sum_sqr(*desvios)
                incerteza = t.sqrt_sum_sqr(desvio_padrao_media, erro)
                comprimento = media
                incerteza_comprimento = incerteza
                linha += t.str_media_incerteza(media, incerteza)
            else:
                objeto = objeto[:-2]
                total_x = []
                total_y = []
                total_z = []
                desvios_x = []
                desvios_y = []
                desvios_z = []
                for aluno_index in range(len(alunos)): 
                    total_x.extend(t.dados(dados_experimento, objeto+'_x', aluno_index))
                    total_y.extend(t.dados(dados_experimento, objeto+'_y', aluno_index))
                    total_z.extend(t.dados(dados_experimento, objeto+'_z', aluno_index))
                    desvios_x.append(t.desvpadmed(t.dados(dados_experimento, objeto+'_x', aluno_index)))
                    desvios_y.append(t.desvpadmed(t.dados(dados_experimento, objeto+'_y', aluno_index)))
                    desvios_z.append(t.desvpadmed(t.dados(dados_experimento, objeto+'_z', aluno_index)))
                media_x = t.med(total_x)
                media_y = t.med(total_y)
                media_z = t.med(total_z)
                desvio_padrao_media_x = t.sqrt_sum_sqr(*desvios_x)
                desvio_padrao_media_y = t.sqrt_sum_sqr(*desvios_y)
                desvio_padrao_media_z = t.sqrt_sum_sqr(*desvios_z)
                erro_x = t.erro_total(*[t.erro(dados_experimento, objeto+'_x', aluno_index) for aluno_index in range(5)])
                erro_y = t.erro_total(*[t.erro(dados_experimento, objeto+'_y', aluno_index) for aluno_index in range(5)])
                erro_z = t.erro_total(*[t.erro(dados_experimento, objeto+'_z', aluno_index) for aluno_index in range(5)])
                incerteza_x = t.sqrt_sum_sqr(desvio_padrao_media_x, erro_x)
                incerteza_y = t.sqrt_sum_sqr(desvio_padrao_media_y, erro_y)
                incerteza_z = t.sqrt_sum_sqr(desvio_padrao_media_z, erro_z)
                comprimento_x = media_x
                comprimento_y = media_y
                comprimento_z = media_z
                incerteza_comprimento_x = incerteza_x
                incerteza_comprimento_y = incerteza_y
                incerteza_comprimento_z = incerteza_z
                linha += t.shortsack('x: ' + t.str_media_incerteza(media_x, incerteza_x), 'y: ' + t.str_media_incerteza(media_y, incerteza_y), 'z: ' + t.str_media_incerteza(media_z, incerteza_z))
            
            # Massa
            massa = 0
            incerteza_massa = 0
            if objeto in dados_experimento.massas:
                linha += ' & '
                total = []
                desvios = []
                for aluno_index in range(5):
                    total.extend(t.dados(dados_experimento, objeto, aluno_index, 'massas'))
                    desvios.append(t.desvpadmed(t.dados(dados_experimento, objeto, aluno_index, 'massas')))
                media = t.med(total)
                desvio_padrao_media = t.sqrt_sum_sqr(*desvios)
                erro = t.erro(dados_experimento, objeto, 0, 'massas')
                incerteza = t.sqrt_sum_sqr(desvio_padrao_media, erro)
                massa = media
                incerteza_massa = incerteza
                linha += t.str_media_incerteza(massa, incerteza_massa)        
            elif objeto in Barra_c or objeto in Barrinha_c:
                objeto = objeto[:-2]
                linha += ' & '
                total = []
                desvios = []
                for aluno_index in range(5):
                    total.extend(t.dados(dados_experimento, objeto, aluno_index, 'massas'))
                    desvios.append(t.desvpadmed(t.dados(dados_experimento, objeto, aluno_index, 'massas')))
                media = t.med(total)
                desvio_padrao_media = t.sqrt_sum_sqr(*desvios)
                erro = t.erro(dados_experimento, objeto, 0, 'massas')
                incerteza = t.sqrt_sum_sqr(desvio_padrao_media, erro)
                massa = media
                incerteza_massa = incerteza
                linha += t.str_media_incerteza(massa, incerteza_massa)        
            # Volume
            volume = 0
            incerteza_volume = 0
            if objeto in dados_experimento.massas:
                linha += ' & '
                if comprimento_x == 0:
                    volume = comprimento ** 3
                    incerteza_volume = volume * 3 * incerteza_comprimento / comprimento
                    if objeto == 'Bola':
                        incerteza_volume = (4/3) * math.pi * incerteza_volume
                        volume = (1/6) * math.pi * volume
                else:
                    volume = comprimento_x * comprimento_y * comprimento_z
                    incerteza_volume = t.sqrt_sum_sqr(incerteza_comprimento_x/comprimento_x, incerteza_comprimento_y/comprimento_y, incerteza_comprimento_z/comprimento_z)
                volume = volume / 10**3
                incerteza_volume = incerteza_volume / 10**3
                linha += t.str_media_incerteza(volume, incerteza_volume)
            
            # Densidade
            if objeto in dados_experimento.massas or objeto in Barra_c or objeto in Barrinha_c:
                linha += ' & '
                densidade = massa / volume
                incerteza_densidade = densidade * t.sqrt_sum_sqr(incerteza_massa/massa, incerteza_volume/volume)
                densidade = densidade * 10**3
                incerteza_densidade = incerteza_densidade * 10**3
                linha += t.str_media_incerteza(densidade, incerteza_densidade)       
            else:
                linha += ' & & & '
            
        arquivo.write(linha + '\\\\[5pt]\n')
    
    t.terminar_tabela_latex(arquivo)