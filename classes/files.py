class Medicao:
    def __init__(self, dados=None, erro=0.0, instrumento=''):
        self.dados = dados if dados is not None else []
        self.erro = float(erro)
        self.instrumento = instrumento
        
class Massa:
    def __init__(self, dados=None, erro=0.0):
        self.dados = dados if dados is not None else []
        self.erro = float(erro)

class DadosExperimento:
    def __init__(self):
        self.medicoes = {}
        self.massas = {}

    def adicionar_medicao(self, objeto, instrumento, erro, unidade, dados):
        if objeto not in self.medicoes:
            self.medicoes[objeto] = []
        self.medicoes[objeto].append({
            'instrumento': instrumento,
            'erro': erro,
            'unidade': unidade,
            'dados': dados
        })

    def adicionar_massa(self, objeto, erro, dados):
        if objeto not in self.massas:
            self.massas[objeto] = []
        self.massas[objeto].append({
            'erro': erro,
            'dados': dados
        })