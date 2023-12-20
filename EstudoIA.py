import streamlit as st
import numpy as np

class Caso:
    def __init__(self, descricao, atributos, pesos, tratamento):
        self.descricao = descricao
        self.atributos = np.array(atributos)
        self.pesos = np.array(pesos)
        self.tratamento = tratamento

def similaridade_local(caso1, caso2):
    return np.sum(caso1.atributos[:-2] != caso2.atributos[:-2])

def similaridade_global(caso1, caso2):
    similaridades_locais = np.array([similaridade_local(caso1, caso2)])
    similaridade_ponderada = np.sum(similaridades_locais * caso1.pesos) / np.sum(caso1.pesos)
    return similaridade_ponderada

class SistemaCBR:
    def __init__(self):
        self.base_de_dados = []

    def adicionar_caso(self, caso):
        self.base_de_dados.append(caso)

    def recuperar_caso(self, novo_caso, medida_similaridade):
        similaridades = [medida_similaridade(novo_caso, caso) for caso in self.base_de_dados]
        indice_mais_similar = np.argmin(similaridades)
        return self.base_de_dados[indice_mais_similar]

# Exemplo de uso
categorias = {
    'Sensibilidade ao Som': {'Normal': 0,'Média': 1, 'Alta': 2},
    'Produtividade em Grupo': {'Não': 0, 'Sim': 1},
    'Cansaço Mental': {'Não': 0, 'Sim': 1},
    'Autismo': {'Não': 0, 'Sim': 1},
    'Concentração com Som': {'Baixa': 2, 'Média': 1, 'Alta':0},
    'Tipo de Conteúdo': {'Exatas': 0, 'Biológicas': 1, 'Humanas': 2},
    'Tratamento': {'Regime simples com pausas desregulares e música opcional': 0, 'Regime com pausas a cada 1 hora e uso de trilha sonora leve': 1, 'Regime com pausas a cada 25 min e auxilio para fixação do conteúdo': 2, 'Regime com pausas estritamente demarcadas, acompanhamento direto e diversificação de apresentação do conteúdo': 3}
}

# Pesos agora têm a forma (1, n), onde n é o número de atributos
pesos_atributos = np.array([1, 2, 4, 5, 1, 4, 1]).reshape(1, -1)

caso1 = Caso("Caso 1", [0, 0, 0, 0, 0, 0, 0], pesos_atributos, 'Regime simples com pausas desregulares e música opcional')
caso2 = Caso("Caso 2", [1, 1, 1, 0, 1, 0, 1], pesos_atributos, 'Regime com pausas a cada 1 hora e uso de trilha sonora leve')
caso3 = Caso("Caso 3", [1, 0, 1, 1, 0, 0, 1], pesos_atributos, 'Regime com pausas a cada 25 min e auxilio para fixação do conteúdo')
caso3 = Caso("Caso 4", [2, 1, 1, 0, 0, 1, 2], pesos_atributos, 'Regime com pausas estritamente demarcadas, acompanhamento direto e diversificação de apresentação do conteúdo')

sistema = SistemaCBR()
sistema.adicionar_caso(caso1)
sistema.adicionar_caso(caso2)
sistema.adicionar_caso(caso3)

# Interface Streamlit
st.title("Verificação de Regime de Estudo (RBC)")

# Coleta de dados do usuário
st.header("Preencha o Formulário:")
sensisom = st.radio("Sensibilidade ao Som", ['Normal','Média', 'Alta'])
prodigrupo = st.radio("Produtividade em Grupo", ['Não', 'Sim'])
cansaço = st.radio("Cansaço Mental", ['Não', 'Sim'])
autismo = st.radio("Autismo", ['Não', 'Sim'])
concensom = st.radio("Concentração com Som", ['Baixa', 'Média', 'Alta'])
conteudo = st.radio("Tipo de Conteúdo", ['Exatas', 'Biológicas', 'Humanas'])

# Criação do novo caso
novo_caso = Caso("Novo Caso", 
                 [categorias['Sensibilidade ao Som'][sensisom], 
                  categorias['Produtividade em Grupo'][prodigrupo], 
                  categorias['Cansaço Mental'][cansaço], 
                  categorias['Autismo'][autismo], 
                  categorias['Concentração com Som'][concensom], 
                  categorias['Tipo de Conteúdo'][conteudo], 
                  0], 
                 pesos_atributos,
                 None)

# Recuperação usando similaridade global
caso_recuperado_global = sistema.recuperar_caso(novo_caso, similaridade_global)

# Mostrar informações do caso recuperado
st.header("Resultado!")
st.write(f"Medidas mais indicadas: {caso_recuperado_global.tratamento}")
