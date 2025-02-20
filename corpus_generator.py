import requests
import os

class CorpusGenerator:
    """
    A class to fetch Python files from Github and convert them to .txt.

    Attributes:
        urls (dictionary): Dictionary of URLs with the size as key and the URL as value.
        output_dir (str): Directory where the .txt files will be saved.
    """

    def __init__(self, output_dir='data/converted_files'):
        """
        Initialises the CorpusGenerator.

        Args:
            output_dir (str): Directory where the .txt files will be saved.
        """
        self.urls = {
            # Include the raw URLs of the Python files to fetch
            'small.txt' : 'https://raw.githubusercontent.com/huggingface/transformers/refs/heads/main/examples/pytorch/text-classification/run_glue.py',
            'medium.txt' : 'https://raw.githubusercontent.com/pytorch/pytorch/refs/heads/main/torch/nn/functional.py',
            'large.txt' : 'https://raw.githubusercontent.com/numpy/numpy/refs/heads/main/numpy/_core/tests/test_multiarray.py'
        }
        self.output_dir = output_dir
        # Create the directory if it does not exist
        os.makedirs(output_dir, exist_ok=True)

    def fetch_and_save(self):
        """
        Fetches the code from each URL and saves it as a .txt file.
        """
        for file_size in self.urls.keys():
            code = self.fetch_url(self.urls[file_size])
            if code:
                self.save_to_file(file_size, code)

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
    fetcher = CorpusGenerator()
    fetcher.fetch_and_save()