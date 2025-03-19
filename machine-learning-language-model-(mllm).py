import random
import nltk
import spacy
from nltk import CFG, ChartParser
from nltk import pos_tag, word_tokenize

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


# Word Tokenization and POS Tagging
def analyze_words(text):
    """Tokenize text into words and perform POS tagging."""
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    return pos_tags


# Dependency Parsing
def dependency_parse(text):
    """Parse text to analyze word dependencies."""
    doc = nlp(text)
    dependencies = []
    for token in doc:
        dependencies.append({
            "Word": token.text,
            "POS": token.pos_,
            "Head": token.head.text,
            "Dependency": token.dep_
        })
    return dependencies


# Grammar Rule Parser
def parse_with_grammar(sentence):
    """Parse a sentence using predefined grammar rules."""
    grammar = CFG.fromstring("""
      S -> NP VP
      NP -> DT NN | DT JJ NN
      VP -> VBZ PP | VBZ NP
      PP -> IN NP
      DT -> 'the'
      JJ -> 'quick' | 'brown' | 'lazy'
      NN -> 'fox' | 'dog'
      VBZ -> 'jumps'
      IN -> 'over'
    """)

    parser = ChartParser(grammar)
    sentence_tokens = sentence.split()
    trees = list(parser.parse(sentence_tokens))
    return trees if trees else "The sentence does not match the grammar."


# Markov Chain Training and Generation
def train_markov_chain(text):
    """Train a Markov Chain model from the given text."""
    words = text.split()
    model = {}
    for i in range(len(words) - 1):
        key = words[i]
        next_word = words[i + 1]
        if key not in model:
            model[key] = []
        model[key].append(next_word)
    return model


def generate_sentence(model, start_word, length=10):
    """Generate a sentence using the Markov Chain model."""
    word = start_word
    sentence = [word]
    for _ in range(length - 1):
        next_words = model.get(word, None)
        if not next_words:
            break
        word = random.choice(next_words)
        sentence.append(word)
    return ' '.join(sentence)


# Main Script
if __name__ == "__main__":
    print("Welcome to the Word Analyzer and Sentence Generator!")
    user_input = input("Enter a sentence or text: ")

    # Tokenization and POS Tagging
    print("\n--- Tokenization and POS Tagging ---")
    pos_analysis = analyze_words(user_input)
    for word, tag in pos_analysis:
        print(f"{word}: {tag}")

    # Dependency Parsing
    print("\n--- Dependency Parsing ---")
    dependencies = dependency_parse(user_input)
    for dep in dependencies:
        print(f"Word: {dep['Word']}, POS: {dep['POS']}, Head: {dep['Head']}, Dependency: {dep['Dependency']}")

    # Grammar Rule Parsing
    print("\n--- Grammar Rule Parsing ---")
    grammar_trees = parse_with_grammar(user_input)
    if isinstance(grammar_trees, str):
        print(grammar_trees)
    else:
        for tree in grammar_trees:
            print(tree)

    # Markov Chain Generation
    print("\n--- Markov Chain Sentence Generation ---")
    markov_model = train_markov_chain(user_input)
    start_word = input("Enter a start word for sentence generation: ")
    generated_sentence = generate_sentence(markov_model, start_word)
    print(f"Generated Sentence: {generated_sentence}")
