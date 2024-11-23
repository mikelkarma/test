import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.util.Base64;

public class Main {

    // Gerando chave
    public static SecretKey generateAESKey() throws Exception {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(128); 
        return keyGenerator.generateKey(); 
    }

    // Encrypt AES
    public static String encrypt(String data, SecretKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key); 
        byte[] encryptedData = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encryptedData);
    
    }


    public static String decrypt(String data, SecretKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] decodedData = Base64.getDecoder().decode(data);
        byte[] decryptedData = cipher.doFinal(decodedData);
        return new String(decryptedData);
    }

    
    public static void print(String text) {
        System.out.println(text);
    }

    public static void main(String[] args) {
        try {
            SecretKey key = generateAESKey(); // Gerando chave
            String data = "Informações confidenciais";
            
            print("> Gerando chave: " + key);
            print(" > Criptografando: " + data);
            String crypt = encrypt(data, key);
            print(" > Resultado criptografado: " + crypt);

            print("\n > Descriptografando...");
            String uncrypt = decrypt(crypt, key); // Passando 'crypt' para descriptografar
            print(" > Resultado descriptografado: " + uncrypt);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
