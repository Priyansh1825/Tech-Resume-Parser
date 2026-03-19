import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Example of how data is structured for BiLSTM-CRF
# Each word gets a tag: B-SKILL (Begin), I-SKILL (Inside), O (Outside/None)
def prepare_sequences(tokenized_resumes, labels, word_to_index, tag_to_index, max_len=100):
    X = [[word_to_index.get(w, word_to_index["ENDPAD"]) for w in s] for s in tokenized_resumes]
    X = pad_sequences(maxlen=max_len, sequences=X, padding="post", value=word_to_index["ENDPAD"])
    
    y = [[tag_to_index[l] for l in s] for s in labels]
    y = pad_sequences(maxlen=max_len, sequences=y, padding="post", value=tag_to_index["O"])
    
    return X, y

# Note: In a full implementation, you would use a dataset from Kaggle[cite: 61, 93].