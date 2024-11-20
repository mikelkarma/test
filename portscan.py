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
# task_manager.add_task("Estudar Python", "2024-11-19", "Pendente")
# task_manager.add_task("Fazer exercícios", "2024-11-20", "Concluído")
# task_manager.add_task("Enviar relatório", "2024-11-21", "Em progresso")
# Listar tarefas
# task_manager.list_task()
# Remover uma tarefa
# task_manager.remove_task("Fazer exercícios")
# Listar tarefas novamente
# task_manager.list_task()

import signal
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

class PortScanner:
    def __init__(self, ip: str, ports: range):
        self.ip = ip
        self.ports = ports
        self.open_ports = []
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[ip]}:{task.fields[port]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            TimeRemainingColumn(),
        )
        self.done_event = Event()

    def handle_sigint(self, signum, frame):
        self.done_event.set()

    def scan_port(self, ip: str, port: int) -> bool:
        """Try to connect to a port to determine if it's open."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            try:
                result = s.connect_ex((ip, port))
                return result == 0  # True if port is open
            except Exception:
                return False

    def run_scan(self):
        """Run the port scan and update the progress bar."""
        task_id = self.progress.add_task("scan", ip=self.ip, port="N/A", total=len(self.ports))

        with self.progress:
            with ThreadPoolExecutor(max_workers=10) as pool:
                for port in self.ports:
                    self.progress.update(task_id, advance=0, ip=self.ip, port=port)
                    pool.submit(self.scan_task, task_id, port)

    def scan_task(self, task_id, port):
        """Scan a single port and log its status."""
        if self.done_event.is_set():
            return

        is_open = self.scan_port(self.ip, port)
        if is_open:
            self.open_ports.append(port)

        self.progress.update(task_id, advance=1)

    def show_results(self):
        """Display open ports in a table."""
        console = Console()
        table = Table(title=f"Open Ports for {self.ip}", show_lines=True)
        table.add_column("Port", justify="center", style="green")
        table.add_column("Status", justify="center", style="bold cyan")

        for port in self.open_ports:
            table.add_row(str(port), "Open")

        if not self.open_ports:
            console.print("[yellow]No open ports found![/yellow]")
        else:
            console.print(table)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:\n\tpython scanner.py <IP> <START_PORT> <END_PORT>")
        sys.exit(1)

    target_ip = "localhost"
    start_port = 0
    end_port = 65535

    scanner = PortScanner(target_ip, range(start_port, end_port + 1))
    signal.signal(signal.SIGINT, scanner.handle_sigint)

    try:
        scanner.run_scan()
        scanner.show_results()
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
