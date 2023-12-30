# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 18:55:26 2023

@author: User
"""

# Data Import

import pandas as pd

file_path = r'C:\Users\User\Desktop\steam_reviews.csv'


# Specify the columns to be read from the CSV file
columns_to_read = ['review', 'language']  # Include 'language' column if it exists

# Define the data types to improve performance (if known)
data_types = {'review': str, 'language': str}  # Assuming 'review' and 'language' columns contain strings

chunk_size = 100000  # Adjust the chunk size as needed

try:
    # Initialize an empty DataFrame to append valid chunks
    english_reviews = pd.DataFrame(columns=columns_to_read)
    
    # Read the file in chunks to identify problematic rows
    for chunk in pd.read_csv(file_path, usecols=columns_to_read, dtype=data_types, chunksize=chunk_size, on_bad_lines='skip'):
        chunk = chunk.dropna()  # Drop any rows with missing values
        
        # Filter English reviews if 'language' column exists
        if 'language' in chunk.columns:
            english_chunk = chunk[chunk['language'] == 'english']
            english_reviews = pd.concat([english_reviews, english_chunk], ignore_index=True)

except Exception as e:
    print("Error:", e)

# Display the results after processing
print("Number of English reviews:", len(english_reviews))
print(english_reviews.head())  # Display the first few rows of English reviews
print("Total number of English reviews:", len(english_reviews))  # Display the count of English reviews


## Word count
from collections import Counter
import string
import time
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords list if not downloaded
nltk.download('stopwords')

# Function to clean and tokenize text
def clean_and_tokenize(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Split text into words
    words = text.split()
    return words

# Concatenate all reviews into a single string
all_reviews_text = ' '.join(english_reviews['review'])

start_time = time.time()  # Record starting time

# Clean and tokenize the text
words_list = clean_and_tokenize(all_reviews_text)

# Remove stop words
stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words_list if word not in stop_words]

# Perform word count using Counter
word_counts = Counter(filtered_words)

end_time = time.time()  # Record ending time

# Calculate the duration of the process
duration = end_time - start_time

# Display the most common words and their counts
most_common_words = word_counts.most_common(20)  # Change 20 to display more or fewer words
for word, count in most_common_words:
    print(f"{word}: {count}")

# Display the time taken to run the process
print(f"Time taken: {duration:.4f} seconds")



