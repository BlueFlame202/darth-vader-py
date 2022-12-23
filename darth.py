# coding: utf-8
# Author: Aathreya Kadambi
# Description: A simple file used to prepare text for the VADER sentiment analysis tools
# Improves VADER by adding the ability to improve its own lexicon; gives vader a title

# DARTH is able to update the lexicon for words that do not already exist in the lexicon by searching through synonyms and definitions
# Of course, this means that it will mean that the lexicon used will be modified to not be a gold standard. However,
# In the future, DARTH should also be able to reconsider existing lexicon entries based on human-made sentiment data

# Built Using:
# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
# Sentiment Analysis of Social Media Text. Eighth International Conference on
# Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.'''

import vaderSentimentu as vdrs
from nltk.corpus import wordnet as wn, wordnet_ic as wn_ic, genesis
import nltk


# Issues
# - I'll have to figure out how to deal with words like the being in the lexicon

# File Outline
# - Darth class
#   - CONSTANTS
#     - _TEX_LEX_FILEPATH: Filepath for text lexicon
#     - _EMO_LEX_FILEPATH: Filepath for emoji lexicon
#   - __init__: construct darth
#   - is_known: see if a word is known to darth.vader
#   - text_familiarity: return proportion of words in a string which are known to darth.vader
#   - learn_text: learn text sentiment by analyzing word synonyms and/or definitions (like a human would)

def get_wn_pos(tag):
    """
    return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v) (taken from https://www.programcreek.com/python/example/91607/nltk.corpus.wordnet)
    """

    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('V'):
        return wn.VERB
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    else:
        return None

# Darth class
class Darth(object):
    """
    Learn new words and improve lexicons to elevate VADER's accuracy
    """

    # CONSTANTS
    _TEX_LEX_FILEPATH = 'darth_vader.lex' # use .lex file ending to differentiate lexicon files, and possibly for compression purposes in the future
    _EMO_LEX_FILEPATH = 'emoji_utf8.lex'
    _WORDS = set(wn.all_lemma_names())
    _COPY_THRESHHOLD = 0.15

    IC_BROWN = wn_ic.ic('ic-brown.dat')
    IC_SEMCOR = wn_ic.ic('ic-semcor.dat')
    IC_GENESIS = wn.ic(genesis, False, 0.0)

    def __init__(self, lexicon_file="vaderSentiment/vader_lexicon.txt", emoji_lexicon="vaderSentiment/emoji_utf8_lexicon.txt"):
        self.vader = vdrs.SentimentIntensityAnalyzer('vader_lexicon.txt', 'emoji_utf8_lexicon.txt')
        self.IC = self.IC_BROWN
        # TODO: put self.vader.lexicon and self.vader.emojis into darth_vader.lex and emoji_utf8.lex
    
    def is_known(self, word):
        return (word.lower() in self.vader.lexicon or word.lower() in vdrs.BOOSTER_DICT or word.lower() in vdrs.NEGATE) # TODO: handle words like of or the

    def text_familiarity(self, text): # return proportion of words which are known to the lexicon
        sentitext = vdrs.SentiText(text)
        words_and_emoticons = sentitext.words_and_emoticons
        
        familiarity = 0.0 
        for i, item in enumerate(words_and_emoticons):
            if self.is_known(item):
                familiarity += 1.0
        familiarity /= len(words_and_emoticons)
        return familiarity
    
    def best_synset(self, word, data):
        word = word.lower()
        if word in self._WORDS:
            synsets = wn.synsets(word, pos=get_wn_pos(data))
            if synsets:
                return wn.synset(synsets[0].name())
        return None

    def closest_word(self, word, data):
        word = word.lower()
        best_candidate = word
        max = 0
        for w in self.vader.lexicon:
            if w in self._WORDS and word in self._WORDS and wn.synsets(word, pos=get_wn_pos(data)) and wn.synsets(w, pos=get_wn_pos(data)):
                bsyn1 = self.best_synset(word, data)
                bsyn2 = self.best_synset(w, data)
                if bsyn1.name().split('.')[1] == bsyn2.name().split('.')[1] and bsyn1.name().split('.')[1] != 's' and bsyn1.name().split('.')[1] != 'r' and bsyn1.name().split('.')[1] != 'a':
                    score = bsyn1.jcn_similarity(bsyn2,self.IC)
                    if score > max:
                        max = score
                        best_candidate = w
        return best_candidate, max

    def learn_text_simple(self, text):
        sentitext = vdrs.SentiText(text)
        words_and_emoticons = sentitext.words_and_emoticons
        for item in nltk.pos_tag(words_and_emoticons):
            if not self.is_known(item[0]):
                if (item[0] in self._WORDS and wn.synsets(item[0].lower(), pos=get_wn_pos(item[1])) and (not (".s." in self.best_synset(item[0], item[1]).name()))) or item[0] not in self._WORDS:
                    cand, max = self.closest_word(item[0].lower(), item[1])
                    if max > self._COPY_THRESHHOLD:
                        self.vader.lexicon[item[0].lower()] = self.vader.lexicon[cand]
                        print(item[0].lower() + ' = ' + cand + '?' + ' Confidence: ' + str(max)) # for testing purposes, print when a word is replaced.

    # Uses nltk to learn text
    # future: also use urbandictionary and other things to also handle slang (use a combination)
    # Currently does not work
    def learn_text(self, text):
        learned = False
        sentitext = vdrs.SentiText(text)
        words_and_emoticons = sentitext.words_and_emoticons
        for item in nltk.pos_tag(words_and_emoticons):
            if not self.is_known(item[0]) and not (".s." in self.best_synset(item[0], item[1]).name()):
                for synset in self.best_synset(item[0], item[1]).hypernyms(): # TODO: rather than using [0], find the right definition based on part of speech
                    measure = 0.0
                    for synonym in synset.name().split('_'):
                        if self.is_known(synonym):
                            if synonym.lower() in self.vader.lexicon:
                                measure += self.vader.lexicon[synonym.lower()]
                            elif synonym.lower() in vdrs.BOOSTER_DICT:
                                self.BOOSTER_DICT.append(item) # likely shouldn't execute ever HOPEFULLY
                            elif synonym.lower() in vdrs.NEGATE:
                                vdrs.NEGATE.append(item) # likely shouldn't execute ever HOPEFULLY
                        else:
                            break # TODO: we can redo this without breaks bro dont be lazy
                        self.vader.lexicon[item] = measure
                        learned = True # TODO: Add to lexicon
                if not learned:
                    
                    return # for now, since otherwise we exceed maximum depth

                    self.learn_text(self.best_synset(item[0], item[1]).definition())
                    measure = self.vader.polarity_scores(wn.synset(item).definition())
                    self.vader.lexicon[item] = measure
                    learned = True # might not be the best definition, so in the future darth should be able to question the lexicon


