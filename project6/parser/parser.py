import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | NP PP | Det N Conj NP | NP Adv | Det AdjP N
PP -> P NP
VP -> V | V NP | V PP | VP Adv | VP Conj VP
AdjP -> Adj | Adj AdjP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # tokenize the sentence
    words = nltk.tokenize.word_tokenize(sentence)

    # filter out words that don't contain alphabetic characters
    filtered_words = []

    for word in words:
        # if there is at least one alphabetic character in the word
        has_alphabetic = any(character.isalpha() for character in word)
    
        if has_alphabetic:
            lowercase_word = word.lower()
            filtered_words.append(lowercase_word)

    return filtered_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            # check whether the NP subtree contains other NP subtrees
            contains_np = False
            for sub_subtree in subtree.subtrees():
                if sub_subtree != subtree and sub_subtree.label() == 'NP':
                    contains_np = True
                    break
            if not contains_np:
                np_chunks.append(subtree)

    return np_chunks


if __name__ == "__main__":
    main()
