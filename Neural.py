# pip install scikit-learn rich python-nmap
import datetime
import sys
import socket
import threading, nmap
from time import sleep
from rich.console import Console
from rich.table import Table
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
console = Console()
import ipaddress

class NetworkScanner:
    def __init__(self):
        self.console = Console()
        self.scanner = nmap.PortScanner()

    def get_local_ip(self):
        """Obtem o IP local"""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    def get_cidr(self, local_ip):
        """Gera o CIDR para a rede atual."""
        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
        return str(network.network_address) + "/24"

    def scan_network(self, cidr):
        """Realiza o scan da rede."""
        self.console.print(f"[bold green]Escaneando a rede:[/bold green] {cidr}")
        self.scanner.scan(hosts=cidr, arguments="-p- -T4 -A")
        return self.scanner

    def display_results(self):
        """Exibe os resultados da varredura."""
        table = Table(title="Resultados do Scanner de Rede")
        table.add_column("Host", style="cyan", justify="left")
        table.add_column("Protocolo", style="magenta", justify="center")
        table.add_column("Porta", style="green", justify="center")
        table.add_column("Serviço", style="yellow", justify="center")

        for host in self.scanner.all_hosts():
            for proto in self.scanner[host].all_protocols():
                ports = self.scanner[host][proto].keys()
                for port in ports:
                    service = self.scanner[host][proto][port]["name"]
                    table.add_row(host, proto, str(port), service)

        self.console.print(table)

def msg(message, end=True, delay=0.2):
    """Função para mostrar mensagens de forma suave"""
    sys.stdout.write(message)
    sys.stdout.flush()
    if end:
        print()
    sleep(delay)

# CLASSE SERVER
class Server:
    def __init__(self, host, port, backlog):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.clients = []

    def start_server(self):
        """Inicia o servidor"""
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.host, self.port))
            self.s.listen(self.backlog)
            msg(f" + Servidor criado com sucesso {self.host}:{self.port}")
        except Exception as error:
            msg(f" - Erro ao criar o servidor: {error}")
            return

    def accept_clients(self):
        """Aceita as conexões dos clientes"""
        try:
            msg(" + Aguardando conexão de clientes...")
            while True:
                s_socket, s_addr = self.s.accept()
                msg(f" + Cliente conectado: {s_addr}")
                self.clients.append({"socket": s_socket, "address": s_addr})
                msg(" + Cliente registrado")
                s_socket.send("Welcome".encode())
                threading.Thread(target=self.handle_client, args=(s_socket, s_addr), daemon=True).start()
       
        except KeyboardInterrupt:
            msg(" + Fechando...")
        except Exception as erro:
            msg(f" - Erro ao registrar o cliente: {erro}")
        finally:
            self.s.close()

    def handle_client(self, s_socket, s_addr):
        """Receber dados do cliente em segundo plano"""
        try:
            while True:
                data = s_socket.recv(1024)
                if not data:
                    break
                msg(f" + Results {s_addr}: {data.decode()}")
                s_socket.send("200".encode())
        except Exception as erro:
            msg(f" - Erro ao receber dados de {s_addr}: {erro}")
        finally:
            s_socket.close()
            msg(f" - Cliente {s_addr} desconectado.")
            

    def send_client(self, client_index, msg):
        """Envia mensagens para o cliente específico"""
        try:
            s_socket = self.clients[client_index]["socket"]
            s_socket.send(msg.encode())
            msg(" + Mensagem enviada com sucesso")
        except IndexError:
            msg(" - Cliente não encontrado")      
        except Exception as erro:
            msg(f" - Ocorreu um erro ao enviar a mensagem: {erro}")


# CLASSE TASK
class Task:
    def __init__(self):
        self.ids = []
        self.tasks = []
        self.dates = []
        self.status = []
        self.counter = 0

    def add_task(self, task, date, stats):
        """Adiciona uma nova tarefa"""
        self.counter += 1
        self.ids.append(self.counter)
        self.dates.append(date)
        self.status.append(stats)
        self.tasks.append(task)
        msg(" > Task adicionada")

    def remove_task(self, task):
        """Remove uma tarefa pelo nome"""
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
        """Remove uma tarefa pelo ID"""
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
        """Lista todas as tarefas"""
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


# Texto para análise de comandos
textos = [
    # Comandos para listar tarefas
    "listar tarefas", 
    "mostrar tarefas", 
    "exibir tarefas", 
    "ver lista de tarefas", 
    "quais tarefas estão pendentes", 
    "listar tasks", 
    "quero ver as tarefas", 
    "lista de tarefas", 
    "mostrar tasks", 
    "ver todas as tarefas", 

    # Comandos para adicionar tarefas
    "adicionar tarefa", 
    "adicionar task", 
    "tem como adicionar uma tarefa?", 
    "inserir nova tarefa", 
    "criar tarefa", 
    "gostaria de adicionar uma tarefa", 
    "adicionar nova task", 
    "nova tarefa", 
    "como adicionar uma task?", 
    "pode adicionar uma tarefa?", 

    # Comandos para remover tarefas
    "remover tarefa", 
    "apagar tarefa", 
    "deletar tarefa", 
    "tem como remover uma tarefa?", 
    "quero excluir uma tarefa", 
    "excluir tarefa", 
    "remover task", 
    "apagar task", 
    "eliminar tarefa", 
    "deletar task",

    # Comandos para iniciar servidor
    "iniciar servidor nous", 
    "start server nous", 
    "ligar servidor nous", 
    "nous server start", 
    "iniciar servidor 01", 
    "start server 01", 
    "criar servidor", 
    "subir servidor nous", 
    "startar servidor", 
    "iniciar servidor de teste",

    # Comandos para listar clientes conectados ao servidor
    "listar clientes conectados", 
    "quais clientes estão conectados", 
    "exibir clientes conectados", 
    "listar clients do server nous", 
    "listar clients do server 01", 
    "listar clientes do servidor", 
    "quais são os clientes conectados", 
    "lista de clientes", 
    "mostrar clientes conectados", 
    "quais são os clientes do servidor?", 

    # Comandos para escanear redes
    "scanear rede wifi", 
    "quero escanear a rede", 
    "scan wifi", 
    "analisar rede wifi", 
    "fazer scan da rede local", 
    "poderia escanear a rede wifi", 
    "scanear dispositivos na rede", 
    "mapear rede", 
    "fazer scan da rede wifi", 
    "procurar dispositivos na rede",

    # Comandos para exibir resultados do escaneamento
    "exibir resultados do scan de rede", 
    "mostrar resultados do scanner de rede", 
    "resultados do scanner de rede", 
    "quais dispositivos foram encontrados na rede", 
    "mostrar resultados do scan wifi", 
    "resultados do scanner wifi", 
    "ver dispositivos escaneados", 
    "mostrar resultados do scanner", 
    "resultados do scan 01", 
    "exibir dispositivos da rede"
]

tags = [
    # Tags relacionadas a tarefas
    "task_list",  # para listar tarefas
    "task_list", 
    "task_list", 
    "task_list", 
    "task_list", 
    "task_list", 
    "task_list", 
    "task_list", 
    "task_list", 
    "task_list", 

    "add_task",  # para adicionar tarefas
    "add_task", 
    "add_task", 
    "add_task", 
    "add_task", 
    "add_task", 
    "add_task", 
    "add_task", 
    "add_task", 
    "add_task", 

    "rm_task",  # para remover tarefas
    "rm_task", 
    "rm_task", 
    "rm_task", 
    "rm_task", 
    "rm_task", 
    "rm_task", 
    "rm_task", 
    "rm_task", 
    "rm_task",

    # Tags relacionadas ao servidor
    "nous_s",  # para iniciar servidor
    "nous_s", 
    "nous_s", 
    "nous_s", 
    "nous_s", 
    "nous_s", 
    "nous_s", 
    "nous_s", 
    "nous_s", 
    "nous_s",

    "server_nous_listing",  # para listar clientes conectados
    "server_nous_listing", 
    "server_nous_listing", 
    "server_nous_listing", 
    "server_nous_listing", 
    "server_nous_listing", 
    "server_nous_listing", 
    "server_nous_listing", 
    "server_nous_listing", 
    "server_nous_listing", 

    # Tags relacionadas ao scanner de redes
    "scan_network",  # para escanear redes
    "scan_network", 
    "scan_network", 
    "scan_network", 
    "scan_network", 
    "scan_network", 
    "scan_network", 
    "scan_network", 
    "scan_network", 
    "scan_network",

    "scan_network_results",  # para exibir resultados do escaneamento
    "scan_network_results", 
    "scan_network_results", 
    "scan_network_results", 
    "scan_network_results", 
    "scan_network_results", 
    "scan_network_results", 
    "scan_network_results", 
    "scan_network_results", 
    "scan_network_results"
]


# Treinamento do modelo
X_train, X_test, y_train, y_test = train_test_split(textos, tags, test_size=0.25, random_state=42)
modelo = make_pipeline(TfidfVectorizer(), MultinomialNB())
modelo.fit(X_train, y_train)

task_manager = Task()

servidor = None
def server_nous():
    global servidor
    HOST = "0.0.0.0"
    BACKLOG = 5
    servidor = Server(HOST, 4545, BACKLOG)
    servidor.start_server()
    threading.Thread(target=servidor.accept_clients, daemon=True).start()

def server_nous_listing():
    if servidor is None or not servidor.clients:
        msg(" - Nenhum cliente conectado")
        return
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Endereço", style="dim")
    for idx, client in enumerate(servidor.clients):
        client_address = client["address"]
        table.add_row(str(idx + 1), str(client_address))
    console.print(table)


    
def task_list():
    task_manager.list_task()

def task_add():
    msg(" > Qual tarefa deseja adicionar?", end=False)
    task = input()
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    task_manager.add_task(task, now, "Pendente")

def task_remove():
    msg(" > Qual ID da task deseja remover?", end=False)
    task_id = input()
    task_manager.remove_task_id(int(task_id))

def scan_network():
   now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
   task_manager.add_task("Scanner de rede", now, "EXECUTADO")
   scanner = NetworkScanner()
   local_ip = scanner.get_local_ip()
   cidr = scanner.get_cidr(local_ip)
   scanner.scan_network(cidr)
   scanner.display_results()

def scan_network_results():
   scanner.display_results()

funcoes = {
    "task_list": task_list,
    "add_task": task_add,
    "rm_task": task_remove,
    "nous_s": server_nous,
    "server_nous_listing": server_nous_listing,
    "scan_network": scan_network,
    "scan_network_results": scan_network_results
}


while True:
    msg(" > ", end=False)
    text = input()
    previsao = modelo.predict([text])
    print(f'Comando: {text}')
    print(f'Função a ser executada: {previsao[0]}')
    funcoes[previsao[0]]()
        
