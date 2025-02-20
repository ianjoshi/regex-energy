
const fs = require('fs');

// Load corpus first
const corpus = fs.readFileSync('data/test_corpus.txt', 'utf8');
const patterns = ["hello", "Pikles"];

// Signal ready and wait for start
fs.writeFileSync('regex_engines/ready_pipe', 'ready\n');
fs.readFileSync('regex_engines/start_pipe'); // Wait for start signal

// Perform regex matching
patterns.forEach((pattern, i) => {
    console.log(`Pattern ${i}: ${pattern}`);
    const regex = new RegExp(pattern, 'g');
    let match;
    while ((match = regex.exec(corpus)) !== null) {
        console.log(`Match: ${match[0]}`);
    }
    console.log();
});

// Signal completion
fs.writeFileSync('regex_engines/done_pipe', 'done\n');
