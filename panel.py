# coded by nous, mik

import os
import sys
from time import sleep
from rich.console import Console
from rich.table import Table

class Task:
    def __init__(self):
        self.tasks = []
        self.dates = []
        self.status = []
    
    def add_task(self, task, date, stats):
        """Adicionando task"""
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
            msg(" > Task removida")
        else:
            msg(" > Task não encontrada")
    
    def list_task(self):
        if not self.tasks:
            msg(" > Nenhuma task encontrada")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Date", style="dim")
        table.add_column("Task", style="bold")
        table.add_column("Status", justify="center")
        
        for date, task, stats in zip(self.dates, self.tasks, self.status):
            table.add_row(date, task, stats)
        
        console.print(table)


# Rich start
console = Console()

# Animação de texto
def msg(message, delay=0.05):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(delay)
    print()

# Exemplo de uso:
task_manager = Task()

# Adicionar tarefas
task_manager.add_task("Estudar Python", "2024-11-19", "Pendente")
task_manager.add_task("Fazer exercícios", "2024-11-20", "Concluído")
task_manager.add_task("Enviar relatório", "2024-11-21", "Em progresso")

# Listar tarefas
task_manager.list_task()

# Remover uma tarefa
task_manager.remove_task("Fazer exercícios")

# Listar tarefas novamente
task_manager.list_task()
