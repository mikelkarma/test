import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;  // Corrigido: Importar SecretKeySpec
import java.security.*;
import java.util.Base64;

public class Cipher {

    // Gerar chave RSA
    public static KeyPair generateRSAKey() throws Exception {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
        keyPairGenerator.initialize(2048); 
        return keyPairGenerator.generateKeyPair();
    }

    // Criptografar com RSA
    public static String encryptRSA(SecretKey aesKey, PublicKey rsaPublicKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, rsaPublicKey);
        byte[] encryptedAESKey = cipher.doFinal(aesKey.getEncoded());
        return Base64.getEncoder().encodeToString(encryptedAESKey);
    }

    // Descriptografar com RSA
    public static SecretKey decryptRSA(String encryptedAESKey, PrivateKey rsaPrivateKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.DECRYPT_MODE, rsaPrivateKey);
        byte[] decodedEncryptedAESKey = Base64.getDecoder().decode(encryptedAESKey);
        byte[] decryptedAESKey = cipher.doFinal(decodedEncryptedAESKey);
        return new SecretKeySpec(decryptedAESKey, "AES");  // Corrigido: Adicionar SecretKeySpec
    }

    // Gerando chave AES
    public static SecretKey generateAESKey() throws Exception {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(128); 
        return keyGenerator.generateKey(); 
    }

    // Criptografar com AES
    public static String encryptAES(String data, SecretKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key); 
        byte[] encryptedData = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encryptedData);
    }

    // Descriptografar com AES
    public static String decryptAES(String data, SecretKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] decodedData = Base64.getDecoder().decode(data);
        byte[] decryptedData = cipher.doFinal(decodedData);
        return new String(decryptedData);
    }

    // Função para printar na tela
    public static void print(String text) {
        System.out.println(text);
    }

    public static void main(String[] args) {
        try {
            // Gerar as chaves RSA
            KeyPair rsaKeyPair = generateRSAKey();
            PublicKey publicKey = rsaKeyPair.getPublic(); // Chave pública
            PrivateKey privateKey = rsaKeyPair.getPrivate(); // Chave privada

            // Gerar chave AES e criptografar os dados
            SecretKey keyAES = generateAESKey();
            String data = "Informação confidenciais";
            print(" > Gerando chave: " + Base64.getEncoder().encodeToString(keyAES.getEncoded()));
            print(" > Criptografando: " + data);
            String crypt = encryptAES(data, keyAES);
            print(" > Resultado criptografado: " + crypt);

            // Criptografando a chave AES com a chave pública RSA
            String keyenc = encryptRSA(keyAES, publicKey);
            print("Chave AES criptografada com RSA: " + keyenc);

            // Descriptografar a chave AES com a chave privada RSA
            SecretKey decryptedAESKey = decryptRSA(keyenc, privateKey);
            print("Chave AES descriptografada com RSA: " + Base64.getEncoder().encodeToString(decryptedAESKey.getEncoded()));
            
            // Descriptografar os dados com a chave AES
            print("\n > Descriptografando...");
            String uncrypt = decryptAES(crypt, decryptedAESKey); // Corrigido: Usar 'decryptedAESKey' ao invés de 'key'
            print(" > Resultado descriptografado: " + uncrypt);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
