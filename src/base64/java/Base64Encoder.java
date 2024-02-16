import java.util.Base64;

/**
 * [A-Z] 26
 * [a-z] 26
 * [0-9] 10
 * +/ 2
 * Total 64 = 2 ^ 6 bit
 */

public class Base64Encoder {
    private String base64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    public String encode(String data) {
        StringBuilder encodedData = new StringBuilder();
        StringBuilder binaryData = new StringBuilder();
        for (char c : data.toCharArray()) {
            binaryData.append(String.format("%8s", Integer.toBinaryString(c)).replace(' ', '0'));
        }

        // pad binary data
        while (binaryData.length() % 6 != 0) {
            binaryData.append('0');
        }

        // encode bytes
        for (int i = 0; i < binaryData.length(); i += 6) {
            String chunk = binaryData.substring(i, i + 6);
            int decimalVal = Integer.parseInt(chunk, 2);
            encodedData.append(base64Chars.charAt(decimalVal));
        }

        // add padding '=' if needed
        int padding = (4 - encodedData.length() % 4) % 4;
        for (int i = 0; i < padding; i++) {
            encodedData.append('=');
        }

        return encodedData.toString();
    }

    public byte[] decode(String encodedData) {
        byte[] decodedData = null;

        return decodedData;
    }

    public static void main(String args[]) {
        System.out.println("Program started");

        Base64Encoder encoder = new Base64Encoder();
        String input = "Hello World!";
        String myEncoded = encoder.encode(input);
        byte[] myDecoded = encoder.decode(myEncoded);

        String encoded = Base64.getEncoder().encodeToString(input.getBytes());
        System.out.println(String.format("Base64 Encoder : %s", myEncoded));
        System.out.println(String.format("Base64 Library : %s", encoded));
    }
}