import datetime
import sys
from time import sleep
from rich.console import Console
from rich.table import Table
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

console = Console()

class Task:
    def __init__(self):
        self.ids = []
        self.tasks = []
        self.dates = []
        self.status = []
        self.counter = 0  # Contador para id

    def add_task(self, task, date, stats):
        """Adicionando task"""
        self.counter += 1
        self.ids.append(self.counter)
        self.dates.append(date)
        self.status.append(stats)
        self.tasks.append(task)
        msg(" > Task adicionada")

    def remove_task(self, task):
        if task in self.tasks:
            index = self.tasks.index(task)
            self.tasks.pop(index)
            self.dates.pop(index)
            self.status.pop(index)
            self.ids.pop(index)
            msg(" > Task removida")
        else:
            msg(" > Task não encontrada")
    
    def remove_task_id(self, task_id):
        if task_id in self.ids:
            index = self.ids.index(task_id)
            self.tasks.pop(index)
            self.dates.pop(index)
            self.status.pop(index)
            self.ids.pop(index)
            msg(" > Task removida")
        else:
            msg(" > Task não encontrada")
    
    def list_task(self):
        if not self.tasks:
            msg(" > Nenhuma task encontrada")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Date", style="dim")
        table.add_column("Task", style="bold")
        table.add_column("Status", justify="center")
        
        for task_id, date, task, stats in zip(self.ids, self.dates, self.tasks, self.status):
            table.add_row(str(task_id), date, task, stats)
        
        console.print(table)

def msg(message, end=True, delay=0.05):
    """Função para mostrar mensagens de forma suave"""
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(delay)
    if end:
        print()

# Texto para análise de comandos
textos = [
    "listar tarefas", 
    "listar tasks", 
    "tarefas",
    "função 1",
    "1",
    "adicionar tarefa", 
    "adicionar task", 
    "Tem como adiconar uma tarefa",
    "remover tarefa", 
    "tem como remover uma tarefa", 
    "remover task"
]

tags = [
    "task_list", 
    "task_list", 
    "task_list", 
    "task_list",
    "task_list",
    "add_task", 
    "add_task", 
    "add_task",
    "rm_task", 
    "rm_task", 
    "rm_task"
]

# Treinamento do modelo
X_train, X_test, y_train, y_test = train_test_split(textos, tags, test_size=0.25, random_state=42)
modelo = make_pipeline(TfidfVectorizer(), MultinomialNB())
modelo.fit(X_train, y_train)

# Funções para manipulação das tasks
task_manager = Task()  # Instância global do gerenciador de tarefas

def task_list():
    task_manager.list_task()

def task_add():
    msg("Qual tarefa deseja adicionar?", end=False)
    task = input()
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    task_manager.add_task(task, now, "Pendente")

def task_remove():
    msg("Qual ID da task deseja remover?", end=False)
    task_id = input()
    task_manager.remove_task_id(int(task_id))

# Mapeamento de funções
funcoes = {
    "task_list": task_list,
    "add_task": task_add,
    "rm_task": task_remove
}

# Exemplo de uso
while True:
 msg(" > ", end=False)
 text = input()

 # Predição do modelo
 previsao = modelo.predict([text])  # Corrigido para passar lista

 # Exibição do comando e execução da função
 print(f'Comando: {text}')
 print(f'Função a ser executada: {previsao[0]}')

 # Executar a função predita
 funcoes[previsao[0]]()
            
