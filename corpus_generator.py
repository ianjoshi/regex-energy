import requests
import os

class CorpusGenerator:
    """
    A class to fetch Python files from Github and convert them to .txt.

    Attributes:
        urls (dictionary): Dictionary of URLs with the size as key and the URL as value.
        output_dir (str): Directory where the .txt files will be saved.
    """

    def __init__(self, output_dir='data'):
        """
        Initialises the CorpusGenerator.

        Args:
            output_dir (str): Directory where the .txt file will be saved.
        """
        self.urls = {
            # Include the raw URL of the Python file to fetch
            'corpus.txt' : 'https://raw.githubusercontent.com/numpy/numpy/refs/heads/main/numpy/_core/tests/test_multiarray.py'
        }
        self.output_dir = output_dir
        # Create the directory if it does not exist
        os.makedirs(output_dir, exist_ok=True)

    def generate_corpus_files(self):
        """
        Fetches the code from each URL and saves it as a .txt file.
        """
        for file_name in self.urls.keys():
            code = self.fetch_url(self.urls[file_name])
            amplified_code = self.amplify_code(code)
            if amplified_code:
                self.save_to_file(file_name, amplified_code)

    def fetch_url(self, url):
        """
        Fetches the content of the given URL.

        Args:
            url (str): The URL to fetch the content of.

        Returns:
            str: The content of the URL if successful, None otherwise.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch {url}: Status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        
    def amplify_code(self, code):
        """
        Amplifies the code by repeating it multiple times until the file reaches a size of 100MB.

        Args:
            code (str): The code to amplify.

        Returns:
            str: The amplified code.
        """
        target_size = 100 * 1024 * 1024
        amplified_code = code
        while len(amplified_code) < target_size:
            amplified_code += code
        return amplified_code

    def save_to_file(self, file_name, content):
        """
        Saves the content to a file in the output directory.

        Args:
            file_name (str): The name of the file.
            content (str): The content to save.
        """
        file_path = os.path.join(self.output_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved {file_path}")

if __name__ == '__main__':
    corpus_generator = CorpusGenerator()
    corpus_generator.generate_corpus_files()