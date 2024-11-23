import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class AES {
  // Gerando chave
  public static SecretKey generateAESKey() throws Exception {
    KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
    keyGenerator.init(128);
    return KeyGenerator.generateKey();
  }

  // Encrypt AES
  public static String encrypt(String data, SecretKey key) throws Exception {
    Cipher cipher = Cipher.getInstance("AES");
    cipher.init(Cipher.ENCRYPT_MODE, key);
    byte[] decodedData = Base64.getDecoder().decode(data);
    byte[] decryptedData = cipher.doFinal(decodedData);
    return new String(decryptedData);
  }

  // Decrypt AES
  public static String decrypt(String data, SecretKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] decodedData = Base64.getDecoder().decode(data);
        byte[] decryptedData = cipher.doFinal(decodedData);
        return new String(decryptedData);
  }
  
  // print :)
  public static void print(String text) throws Exception {
    System.out.println(text);
  }
  
  public static void main(String[] args) {
    SecretKey key = generateAESKey(); // gerando key

    // Criptogrando com  a key gerada
    String data = "Informações confidencial";
    print("> GenerateKEY: ", key);
    print(" > Criptografando:", data);
    String crypt = encrypt(data, key);
    print(" > Result:", crypt);

    // descriptografando
    print("\n > Decrypting...");
    String uncrypt = decrypt(crypt, key);
    print(" > Result:", uncrypt);
    
  }
  
}
