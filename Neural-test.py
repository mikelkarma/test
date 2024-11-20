from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
textos = [
    "executar", 
    "executar função 2", 
    "executar função 3", 
    "executar portscan", 
    "rodar função 1", 
    "rodar função 2", 
    "rodar função 3", 
    "iniciar portscan"
]

tags = [
    "funcao_1", 
    "funcao_2", 
    "funcao_3", 
    "portscan", 
    "funcao_1", 
    "funcao_2", 
    "funcao_3", 
    "portscan"
]

X_train, X_test, y_train, y_test = train_test_split(textos, tags, test_size=0.25, random_state=42)
modelo = make_pipeline(TfidfVectorizer(), MultinomialNB())
modelo.fit(X_train, y_train)

def funcao_1():
    print("Função 1 executada!")

def funcao_2():
    print("Função 2 executada!")

def funcao_3():
    print("Função 3 executada!")

def portscan():
    print("Função portscan executada!")

funcoes = {
    "funcao_1": funcao_1,
    "funcao_2": funcao_2,
    "funcao_3": funcao_3,
    "portscan": portscan
}

text = ["abrir portscan"]
previsao = modelo.predict(text)

print(f'Comando: {novo_texto[0]}')
print(f'Função a ser executada: {previsao[0]}')

funcoes[previsao[0]]()
