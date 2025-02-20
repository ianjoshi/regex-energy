
import java.io.*;
import java.util.regex.*;
import java.util.List;
import java.util.Arrays;

public class RegexMatcher {
    public static void main(String[] args) throws IOException {
        // Load corpus first
        String corpus = readFile("data/test_corpus.txt");
        List<String> patterns = Arrays.asList("hello", "Pikles");
        
        // Signal ready and wait for start
        BufferedWriter readyWriter = new BufferedWriter(new FileWriter("regex_engines/ready_pipe"));
        readyWriter.write("ready\n");
        readyWriter.flush();
        readyWriter.close();
        
        BufferedReader startReader = new BufferedReader(new FileReader("regex_engines/start_pipe"));
        startReader.readLine();  // Wait for start signal
        startReader.close();
        
        // Perform regex matching
        for (int i = 0; i < patterns.size(); i++) {
            String pattern = patterns.get(i);
            System.out.println("Pattern " + i + ": " + pattern);
            Pattern compiledPattern = Pattern.compile(pattern);
            Matcher matcher = compiledPattern.matcher(corpus);
            while (matcher.find()) {
                System.out.println("Match: " + matcher.group());
            }
            System.out.println();
        }
        
        // Signal completion
        BufferedWriter doneWriter = new BufferedWriter(new FileWriter("regex_engines/done_pipe"));
        doneWriter.write("done\n");
        doneWriter.flush();
        doneWriter.close();
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