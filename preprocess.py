import re
import nltk
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')

def clean_text(text):
    """
    Cleans the extracted text by removing noise, symbols, and standardizing format.
    """
    # 1. Lowercase conversion [cite: 67]
    text = text.lower()
    
    # 2. Remove URLs, Emails, and special characters [cite: 66]
    text = re.sub(r'http\S+\s*', ' ', text)  # remove URLs
    text = re.sub(r'RT|cc', ' ', text)       # remove RT and cc
    text = re.sub(r'#\S+', '', text)         # remove hashtags
    text = re.sub(r'@\S+', '  ', text)       # remove mentions
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', text)  # remove punctuations
    text = re.sub(r'[^\x00-\x7f]', r' ', text) # remove non-ASCII characters
    
    # 3. Remove extra whitespace
    text = re.sub('\s+', ' ', text).strip()
    
    return text

# Example usage:
# cleaned_resume = clean_text(raw_text)