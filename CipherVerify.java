import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.*;
import java.util.Base64;

public class CipherVerify {

    // Gerar chave RSA para o cliente
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
        return new SecretKeySpec(decryptedAESKey, "AES");
    }

    // Gerar chave AES
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

    // Assinar dados com a chave privada RSA do Cliente
    public static String signData(byte[] data, PrivateKey privateKey) throws Exception {
        Signature signature = Signature.getInstance("SHA256withRSA");
        signature.initSign(privateKey);
        signature.update(data);
        byte[] signedData = signature.sign();
        return Base64.getEncoder().encodeToString(signedData);
    }

    // verificacao de chave
    public static boolean verifySignature(byte[] data, String signatureStr, PublicKey publicKey) throws Exception {
        Signature signature = Signature.getInstance("SHA256withRSA");
        signature.initVerify(publicKey);
        signature.update(data);
        byte[] signatureBytes = Base64.getDecoder().decode(signatureStr);
        return signature.verify(signatureBytes);
    }

    // Funcao para printar na tela
    public static void print(String text) {
        System.out.println(text);
    }

    public static void main(String[] args) {
        try {
            // Gerar as chaves RSA para o Cliente Master e Cliente
            KeyPair rsaMasterKeyPair = generateRSAKey(); 
            KeyPair rsaClientKeyPair = generateRSAKey(); 

            PublicKey publicKeyMaster = rsaMasterKeyPair.getPublic();
            PrivateKey privateKeyMaster = rsaMasterKeyPair.getPrivate();
            PublicKey publicKeyClient = rsaClientKeyPair.getPublic();
            PrivateKey privateKeyClient = rsaClientKeyPair.getPrivate(); 

            // Gerar chave AES e criptografar os dados no Cliente
            SecretKey keyAES = generateAESKey();
            String data = "Informação confidenciais";
            print(" > Gerando chave AES: " + Base64.getEncoder().encodeToString(keyAES.getEncoded()));
            print(" > Criptografando mensagem com AES: " + data);
            String crypt = encryptAES(data, keyAES);
            print(" > Resultado criptografado com AES: " + crypt);

            // Criptografar a chave AES com a chave pública do Cliente Master
            String encryptedAESKey = encryptRSA(keyAES, publicKeyMaster);
            print(" > Chave AES criptografada com RSA (pelo Public Master): " + encryptedAESKey);

            // Assinar a mensagem criptografada com a chave privada do Cliente
            String signedMessage = signData(crypt.getBytes(), privateKeyClient);
            print(" > Assinatura digital da mensagem: " + signedMessage);

            print("Chave Aes(Rsa): " + encryptedAESKey);
            print("Mensagem: " + crypt);
            print("Assinatura: " + signedMessage);

            // Descriptografar a chave AES no Cliente Master
            SecretKey decryptedAESKey = decryptRSA(encryptedAESKey, privateKeyMaster);
            print(" > Chave AES descriptografada com a chave privada do Cliente Master: " + Base64.getEncoder().encodeToString(decryptedAESKey.getEncoded()));

            // Verificar a assinatura da mensagem
            boolean isSignatureValid = verifySignature(crypt.getBytes(), signedMessage, publicKeyClient);
            print(" > Verificando assinatura do cliente: " + isSignatureValid);

            // Descriptografar a mensagem com a chave AES no Cliente Master
            print(" > Descriptografando mensagem...");
            String uncrypt = decryptAES(crypt, decryptedAESKey); 
            print(" > Resultado descriptografado: " + uncrypt);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
