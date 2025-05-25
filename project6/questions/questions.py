import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = {}
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    contents = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            full_path = os.path.join(directory, filename)
            with open(full_path, 'r', encoding="utf-8") as file:
                contents[filename] = file.read()
    return contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # convert to lowercase and tokenize
    words_lower = nltk.tokenize.word_tokenize(document.lower())

    filtered_words = []

    # filter out punctuation and stopwords
    for word in words_lower:
        if word not in nltk.corpus.stopwords.words("english") and word not in string.punctuation:
            filtered_words.append(word)

    return filtered_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # count the number of documents each word appears in
    frequencies = {}
    for word_list in documents.values():
        unique_words = set(word_list)
        for word in unique_words:
            if word not in frequencies:
                frequencies[word] = 1
            else:
                frequencies[word] += 1
    
    total_documents = len(documents)
    idf_values = {}

    # calculate IDF
    for word, doc_freq in frequencies.items():
        idf_values[word] = math.log(total_documents / doc_freq)

    return idf_values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_scores = []

    # calculate tf-idf score
    for filename, words in files.items():
        score = 0
        for word in query:
            if word in words:
                score += idfs[word] * words.count(word)
        file_scores.append((filename, score))

    # sort and get top n TF-IDFs for each file
    sorted_files = sorted(file_scores, key=lambda x: x[1], reverse=True)
    top_files = [filename for filename, _ in sorted_files[:n]]

    return top_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_scores = []

    for sentence, words in sentences.items():
        # calculate sum of IDF values for any word in query that also appears in sentence
        matching_word_measure = 0
        for word in query:
            if word in words:
                matching_word_measure += idfs[word]

        # calculate query term density
        query_term_density = 0
        for word in words:
            if word in query:
                query_term_density += 1/ len(words)

        sentence_scores.append((sentence, matching_word_measure, query_term_density))

    # sort sentences based on scores and query term density in descending order
    sorted_sentences = sorted(sentence_scores, key=lambda x: (x[1], x[2]), reverse=True)

    # take the top n sentences
    top_sentences = [sentence for sentence, _, _ in sorted_sentences[:n]]

    return top_sentences


if __name__ == "__main__":
    main()
