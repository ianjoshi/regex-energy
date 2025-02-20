
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class RegexMatcher {
    public static void main(String[] args) {
        String corpus = readFile("data/corpus.txt");
        
        
        Pattern pattern0 = Pattern.compile("hello");
        Matcher matcher0 = pattern0.matcher(corpus);
        while (matcher0.find()) {
            System.out.println("Match 0: " + matcher0.group());
        }

        Pattern pattern1 = Pattern.compile("Pikles");
        Matcher matcher1 = pattern1.matcher(corpus);
        while (matcher1.find()) {
            System.out.println("Match 1: " + matcher1.group());
        }
    }

    private static String readFile(String filepath) {
        StringBuilder content = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append("\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return content.toString();
    }
}