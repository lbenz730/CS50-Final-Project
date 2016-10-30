import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives="positive-words.txt", negatives="negative-words.txt"):
        """Initialize Analyzer."""
        self.positives = "positive-words.txt"
        self.negatives = "negative-words.txt"

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        # load positive and negative word lists
        fileP = open(self.positives, "r")
        fileN = open(self.negatives, "r")
        
        # skip comments and blank line at beginning of text (first 35 lines)
        positive = fileP.readlines()[35:]
        negative = fileN.readlines()[35:]
        fileP.close()
        fileN.close()
        
        # tokenize tweet
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        
        #strip newline characters
        for word in range(len(positive)):
            positive[word] = positive[word][:-1]
        for word in range(len(negative)):
            negative[word] = negative[word][:-1]
        
        # analyze text
        score = 0
        for token in tokens:
            if str.lower(token) in positive:
                score += 1
            if str.lower(token) in negative:
                score -= 1
                
        return score