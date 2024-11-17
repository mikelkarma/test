# coded by mik

# IMPORTS
import socket
import threading

# FUNCTIONS SOCKET
class Server:
    def __init__(self, host, port, backlog):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.clients = []

    # START SERVER
    def start_server(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.host, self.port))
            self.s.listen(self.backlog)
            print(f" + Servidor criado com sucesso {self.host}:{self.port}")
        except Exception as error:
            print(f" - Erro ao criar o servidor: {error}")
            return

    # ACCEPT CONNECTIONS
    def accept_clients(self):
        try:
            print("Aguardando conexão de clientes...")
            while True:
                s_socket, s_addr = self.s.accept()  # Corrigido os dois pontos extras
                print(f" + Cliente conectado: {s_addr}")
                self.clients.append({
                    "socket": s_socket,
                    "address": s_addr
                })
                print(" + Cliente registrado")
                s_socket.send("Welcome".encode())

        except KeyboardInterrupt:
            print(" + Fechando...")

        except Exception as erro:
            print(f" - Erro ao registrar o cliente: {erro}")

        finally:
            self.s.close()

    # FUNCTION SEND MESSAGES
    def send_client(self, client_index, msg):
        try:
            s_socket = self.clients[client_index]["socket"]
            s_socket.send(msg.encode())
            print(" + Mensagem enviada com sucesso")
        except IndexError:
            print(" - Cliente não encontrado")      
        except Exception as erro:
            print(f" - Ocorreu um erro ao enviar a mensagem: {erro}")

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 4545
    BACKLOG = 5

    servidor = Server(HOST, PORT, BACKLOG)
    servidor.start_server()

    # Rodando o servidor para aceitar conexões em um thread
    threading.Thread(target=servidor.accept_clients, daemon=True).start()

    # Loop principal para enviar mensagens
    while True:
        try:
            client_id = int(input("Digite o ID do cliente: "))
            msg = input("Mensagem que deseja enviar: ")
            servidor.send_client(client_id, msg)
        except KeyboardInterrupt:
            print("\n + Fechando...")
            break
        except ValueError:
            print(" - Por favor, insira um número válido para o ID do cliente.")
        except Exception as erro:
            print(f" - Ocorreu um erro: {erro}")
