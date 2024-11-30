import java.io.*;
import java.net.*;

public class Socket {

    // Função para imprimir mensagens
    public static void print(String msg) {
        System.out.println(msg);
    }

    // Função para se conectar ao servidor
    public static void connect(String host) {
        try {
            // Divide a string de conexão no formato "host:port"
            String[] parts = host.split(":");
            String rhost = parts[0]; // Host (endereço do servidor)
            int rport = Integer.parseInt(parts[1]); // Porta (convertida para inteiro)

            // Cria o socket e inicializa os streams
            Socket socket = new Socket(rhost, rport);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader consoleInput = new BufferedReader(new InputStreamReader(System.in));

            print("Conectado!");

            // Loop para comunicação com o servidor
            while (true) {
                System.out.print("Digite uma mensagem para o servidor (ou 'exit' para sair): ");
                String userInput = consoleInput.readLine(); // Lê mensagem do usuário
                if (userInput == null || userInput.equalsIgnoreCase("exit")) {
                    print("Encerrando conexão...");
                    break;
                }

                out.println(userInput); // Envia mensagem ao servidor
                String serverResponse = in.readLine(); // Lê resposta do servidor
                if (serverResponse == null) {
                    print("Conexão com o servidor foi encerrada.");
                    break;
                }
                print("Servidor: " + serverResponse); // Mostra a resposta do servidor
            }

            // Fecha os recursos
            socket.close();
            in.close();
            out.close();
            consoleInput.close();
        } catch (IOException e) {
            print(" > Ocorreu um erro: " + e.getMessage());
        }
    }

    // Função principal
    public static void main(String[] args) {
        print("Conectando...");
        connect("127.0.0.1:12345"); // Exemplo de uso da função connect
    }
}
