import nltk
import sys
import string

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

# Noun Phrase rules
NP -> Det N | N | Det NP | AP NP | N PP

# Adjective Phrase rule: one or more adjectives
AP -> Adj | Adj AP

# Prepositional Phrase rule
PP -> P NP

# Verb Phrase rules
VP -> V | V NP | V PP | V NP PP | VP Adv | VP Conj VP | Adv VP

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

    if not sentence:
        return []
    
    # Convert to lowercase and split into words
    words = nltk.word_tokenize(sentence.lower()) # ntlk.word_tokenize will remove non-letter automatically
    
    # Keep only words with at least one alphabetic character
    return [word for word in words 
            if any(c.isalpha() for c in word)
        ]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    # The subtrees() method provides an iterator over all subtrees.
    # We can use its filter argument to only consider subtrees labeled "NP".
    for subtree in tree.subtrees(filter=lambda t: t.label() == "NP"):

        # A subtree is a "chunk" if it doesn't contain other NP subtrees.
        # We check this by seeing if any of its immediate children are also NPs.
        if not any(isinstance(child, nltk.Tree) and child.label() == "NP"
                   for child in subtree):
            chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()
