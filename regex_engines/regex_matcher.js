
const fs = require('fs');

const corpus = fs.readFileSync('data/corpus.txt', 'utf8');


const regex0 = new RegExp('hello', 'g');
let match0;
while ((match0 = regex0.exec(corpus)) !== null) {
    console.log(`Match 0: ${match0[0]}`);
}

const regex1 = new RegExp('Pikles', 'g');
let match1;
while ((match1 = regex1.exec(corpus)) !== null) {
    console.log(`Match 1: ${match1[0]}`);
}
