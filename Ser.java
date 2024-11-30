import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class Ser {
    private static final int PORT = 12345;
    private static final Map<String, ClientHandler> clients = new ConcurrentHashMap<>();
    private static final Set<String> validIds = new HashSet<>(Arrays.asList("client1", "client2", "client3")); // IDs válidos

    public static void main(String[] args) {
        System.out.println("Servidor iniciado na porta " + PORT);
        ExecutorService executor = Executors.newCachedThreadPool();

        // Thread para CLI do servidor
        new Thread(() -> {
            try (Scanner scanner = new Scanner(System.in)) {
                while (true) {
                    System.out.print("Comando (list | connect <ID>): ");
                    String input = scanner.nextLine().trim();
                    String[] parts = input.split(" ", 2);
                    String command = parts[0];

                    switch (command) {
                        case "list":
                            listClients();
                            break;

                        case "connect":
                            if (parts.length == 2) {
                                connectToClient(parts[1], scanner);
                            } else {
                                System.out.println("Uso: connect <ID>");
                            }
                            break;

                        default:
                            System.out.println("Comando inválido.");
                            break;
                    }
                }
            }
        }).start();

        // Gerenciamento de conexões de clientes
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            while (true) {
                Socket socket = serverSocket.accept();
                executor.submit(() -> handleClient(socket));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void handleClient(Socket socket) {
        try (
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true)
        ) {
            out.println("Digite seu ID:");
            String clientId = in.readLine();

            if (clientId == null || !validIds.contains(clientId)) {
                out.println("ID inválido. Conexão encerrada.");
                socket.close();
                return;
            }

            synchronized (clients) {
                if (clients.containsKey(clientId)) {
                    out.println("ID já conectado. Conexão encerrada.");
                    socket.close();
                    return;
                }
                clients.put(clientId, new ClientHandler(clientId, socket, in, out));
                System.out.println("Cliente conectado: " + clientId);
            }

            out.println("Bem-vindo, " + clientId + "! Você está conectado.");

            String message;
            while ((message = in.readLine()) != null) {
                System.out.println("Mensagem de " + clientId + ": " + message);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            disconnectClient(socket);
        }
    }

    private static void listClients() {
        if (clients.isEmpty()) {
            System.out.println("Nenhum cliente conectado.");
        } else {
            System.out.println("Clientes conectados:");
            clients.keySet().forEach(id -> System.out.println(" - " + id));
        }
    }

    private static void connectToClient(String clientId, Scanner scanner) {
        ClientHandler client = clients.get(clientId);

        if (client == null) {
            System.out.println("Cliente " + clientId + " não está conectado.");
            return;
        }

        System.out.println("Conectado ao cliente: " + clientId);
        System.out.println("Digite mensagens para enviar (ou 'exit' para sair):");

        while (true) {
            String message = scanner.nextLine();
            if (message.equalsIgnoreCase("exit")) {
                System.out.println("Desconectado de " + clientId);
                break;
            }
            client.sendMessage("Servidor: " + message);
        }
    }

    private static void disconnectClient(Socket socket) {
        try {
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        synchronized (clients) {
            clients.values().removeIf(client -> {
                if (client.getSocket().equals(socket)) {
                    System.out.println("Cliente desconectado: " + client.getClientId());
                    return true;
                }
                return false;
            });
        }
    }

    private static class ClientHandler {
        private final String clientId;
        private final Socket socket;
        private final PrintWriter out;

        public ClientHandler(String clientId, Socket socket, BufferedReader in, PrintWriter out) {
            this.clientId = clientId;
            this.socket = socket;
            this.out = out;
        }

        public String getClientId() {
            return clientId;
        }

        public Socket getSocket() {
            return socket;
        }

        public void sendMessage(String message) {
            out.println(message);
        }
    }
}
