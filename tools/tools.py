import numpy as np
import locale
from decimal import Decimal

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def extrair_dados_medicao(dados_experimento, arquivo_medicoes):
    for linha in arquivo_medicoes:
        objeto = linha[0]
        instrumento = linha[1]
        unidade = linha[3]
        erro = float(linha[2]) * (10 if unidade == 'cm' else 1)
        dados = [float(float(item) * (10 if unidade == 'cm' else 1)) for item in linha[4:]]
        
        dados_experimento.adicionar_medicao(
            objeto=objeto,
            instrumento=instrumento,
            erro=erro,
            unidade=unidade,
            dados=dados
        )
        
def contar_casas_decimais(*numeros):
    return min(len(str(float(numero)).split('.')[-1]) for numero in numeros)

def extrair_dados_massa(dados_experimento, arquivo_massas):
    for linha in arquivo_massas:
        objeto = linha[0]
        erro = float(linha[1])
        dados = [float(item) for item in linha[2:]]
        
        dados_experimento.adicionar_massa(
            objeto=objeto,
            erro=erro,
            dados=dados
        )

def med(dados):
    return np.mean(dados)

def desvpadmed(dados):
    return np.std(dados, ddof=1) / np.sqrt(len(dados))

def sqrt_sum_sqr(*dados):
    soma_quadrados = 0
    for dado in dados:
        if isinstance(dado, (list, np.ndarray)):
            soma_quadrados += np.sum(np.square(dado))
        else:
            soma_quadrados += dado ** 2
    return np.sqrt(soma_quadrados)

def erro_total(*erros, n=10):
    return sqrt_sum_sqr(erros/np.sqrt(n))

def medicao(dados_experimento, objeto, aluno_index, numero_medicao):
    return dados_experimento.medicoes[objeto][aluno_index]['dados'][numero_medicao]

def massa(dados_experimento, objeto, aluno_index, numero_medicao):
    return dados_experimento.massas[objeto][aluno_index]['dados'][numero_medicao]

def instrumento(dados_experimento, objeto, aluno_index):
    return dados_experimento.medicoes[objeto][aluno_index]['instrumento']

def erro(dados_experimento, objeto, aluno_index, tipo='medicoes',):
    return getattr(dados_experimento, tipo)[objeto][aluno_index]['erro']

def dados(dados_experimento, objeto, aluno_index, tipo='medicoes'):
    return getattr(dados_experimento, tipo)[objeto][aluno_index]['dados']

# Função para formatar a média com casas decimais
def str_media(media, casas_decimais=2):
    return locale.format_string(f"%.{casas_decimais}f", media, grouping=True)

# Função para formatar a média com incerteza, considerando potência de 10
def str_media_incerteza(media, incerteza, casas_decimais=1):
    value = Decimal(media)
    uncertainty = Decimal(incerteza)

    # Convert to scientific notation
    scientific_value = f"{value:.{casas_decimais+1}e}"
    scientific_uncertainty = f"{uncertainty:.{casas_decimais+1}e}"

    # Split into mantissa and exponent
    _, exponent_value = scientific_value.split('e')
    mantissa_uncertainty, exponent_uncertainty = scientific_uncertainty.split('e')

    # Convert strings to numbers for calculations
    mantissa_uncertainty_num = float(mantissa_uncertainty)
    exponent_value_num = int(exponent_value)
    exponent_uncertainty_num = int(exponent_uncertainty)

    # Adjust mantissas and exponents
    adjusted_mantissa_value = value * (10 ** (exponent_value_num - exponent_uncertainty_num)) / (10 **(exponent_value_num))
    adjusted_mantissa_uncertainty = mantissa_uncertainty_num

    # Format the result
    if exponent_uncertainty_num == 0 or exponent_uncertainty_num == -1:
        return f"{media:.{casas_decimais}f} ± {incerteza:.{casas_decimais}f}".replace('.', ',')
    elif exponent_uncertainty_num == 1:
        return f"({adjusted_mantissa_value:.{casas_decimais}f} ± {adjusted_mantissa_uncertainty:.{casas_decimais}f})·10".replace('.', ',')
    else:
        return f"({adjusted_mantissa_value:.{casas_decimais}f} ± {adjusted_mantissa_uncertainty:.{casas_decimais}f})·10$^{{{exponent_uncertainty_num}}}$".replace('.', ',')

def criar_tabela_latex(arquivo, alinhamento, n):
    arquivo.write('\\documentclass{article}\n')
    arquivo.write('\\usepackage{amsmath}\n')
    arquivo.write('\\usepackage{booktabs}\n')
    arquivo.write('\\usepackage[portuguese]{babel}\n')
    arquivo.write('\\usepackage[a4paper, margin=0.1cm, top=0.5cm, bottom=0.5cm]{geometry}\n')
    arquivo.write('\\begin{document}\n\n')
    arquivo.write('\\begin{table}[h!]\n')
    arquivo.write('\\centering\n')
    arquivo.write(f'\\begin{{tabular}}{{{f"{alinhamento} " * n}}}\n')
    arquivo.write('\\toprule\n')
    
def shortsack(*textos, parenteses=False):
    linha = '\\shortstack{'
    for i, texto in enumerate(textos):
        if texto != '':
            if i == 0 and parenteses:
                texto = f'({texto})'
            linha += texto
            if i < len(textos) - 1:  # Corrigido aqui
                linha += '\\\\'
    linha += '}'
    return linha
    
def italic(texto):
    return f'\\textit{{{texto}}}'

def terminar_tabela_latex(arquivo):
    arquivo.write('\\bottomrule\n')
    arquivo.write('\\end{tabular}\n')
    arquivo.write('\\end{table}\n')
    arquivo.write('\\end{document}\n')
    
def handle_espaço(linha, aluno_index):
    if aluno_index < 4:
        linha += ' & '
    return linha 