# DARTH VADER Sentiment Analysis

An extension of VADER Sentiment Analysis. Valence Aware Dictionary and sEntiment Reasoner (VADER) is a lexicon and rule-based sentiment tool designed to measure sentiment of text from social media. DARTH VADER is a tool that utilizes WordNets to learn words that are not contained within the vader lexicon. While VADER is based on a gold-standard lexicon, resulting in sentiments for words dictated by humans, DARTH VADER attempts to create a dynamic lexicon which is able to update and accomodate for words that are not contained within the lexicon. This way, texts that contain words that are not in the lexicon can still be analyzed accurately. This is a double edged sword, since while DARTH VADER can give more accurate results on texts containing words not in the lexicon, it can also assign sentiments that are not very accurate to words not contained in the lexicon. However, the chances of DARTH VADER assigning false sentiments is minimized by controlling DARTH's threshold and determining how DARTH VADER updates the valence of new words.

## Table of Contents
  * [Table of Contents](#table-of-contents)
  * [Introduction](#introduction)
  * [Limitations](#limitations)
  * [Recent Updates](#recent-updates)
  * [Python Demo and Code Examples](#python-demo-and-code-examples)
  * [Contact](#contact)

## Introduction

The VADER Sentiment Tool is a very good tool for assigning sentiment scores to text from social media. However, it does experience limitations. For example, 

* Some words are not in the lexicon. 

For example, "wilt" is not contained in the VADER lexicon. This means VADER believes wilt is a neutral word, whereas it is actually negative.

* It does not consider context of words when assigning sentiment. 

For an example of why this is an issue, consider the word "hard". One definition of hard is "not easy; requiring great physical or mental effort to accomplish or comprehend or endure" (taken from ```wn.synsets("hard")[0].definition()```). Another definition is "resisting weight or pressure" (taken from ```wn.synsets("hard)[2].definition()```). Clearly, these two meanings should be assigned different sentiments. 

Tackling these issues is a difficult task, and DARTH attempts to resolve at least a portion of the issues caused by the above limitations by creating a new lexicon that is not a gold-standard.

## Limitations

DARTH VADER attempts to attack the issue that not all words are contained in the lexicon by adding such words to the lexicon. Currently, it uses a simple learning mechanism that assigns the valance of a new word to be the valance of the closest existing word in the lexicon, assuming that the "closeness" is larger than a certain threshold. The metric for closeness used is the Jiang-Conrath Similarity score along with the Brown Corpus Information Content (```IC_BROWN```). However, the superiority of this metric and ```IC_BROWN``` has not been tested. This is something that must be done in the future.

Another major limitation is that the to the author's knowledge, the VADER lexicon does not specify synset. As a result, words can be assigned to the wrong WordNet synset, and this causes inaccuracies in the sentiments assigned by DARTH. This error is somewhat controlled by setting higher ```_COPY_THRESHOLD```s in darth.py. Future investigation will be directed towards identifying synsets based on context as well as implementing better learning mechanisms. Future investigation will also be directed towards other wordnets as well as SenticNet, which may contain accurate sentiment scores on a larger selection of words.

## Recent Updates

darth.py has been successfully implemented. Scores on certain texts are more accurate, and in general darth is more sensitive to texts since it is able to learn words.

## Python Demo and Code Examples

The following code, contained in ```playground.py```, was run:
```
from vaderSentimentu import SentimentIntensityAnalyzer

import darth as d

# --- examples -------
sentences = ["VADER is smart, handsome, and funny.",  # positive sentence example
             "VADER is smart, handsome, and funny!",  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is very smart, handsome, and funny.", # booster words handled correctly (sentiment intensity adjusted)
             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
             "VADER is VERY SMART, handsome, and FUNNY!!!", # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", # booster words & punctuation make this close to ceiling for score
             "VADER is not smart, handsome, nor funny.",  # negation sentence example
             "The book was good.",  # positive sentence
             "At least it isn't a horrible book.",  # negated negative sentence with contraction
             "The book was only kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
             "Today SUX!",  # negative slang with capitalization emphasis
             "Today only kinda sux! But I'll get by, lol", # mixed sentiment example with slang and constrastive conjunction "but"
             "Make sure you :) or :D today!",  # emoticons handled
             "Catch utf-8 emoji such as such as 💘 and 💋 and 😁",  # emojis handled
             "Not bad at all",  # Capitalized negation
             "Watch the rose wilt." # Word not in the lexicon
             ]

from senticnet.senticnet import SenticNet

def vaderPlayground():
    sn = SenticNet()
    print(sn.polarity_value('love'))

    analyzer = SentimentIntensityAnalyzer()
    for sentence in sentences:
        vs = analyzer.polarity_scores(sentence)
        print("{:-<65} {}".format(sentence, str(vs)))
    return

def darthPlayground():
    darth = d.Darth()
    #print(darth.closest_word("falling", ))

    #print(darth.text_familiarity("wilt"))
    #darth.learn_text_simple("wilt")
    #print(darth.text_familiarity("wilt"))
    #print(darth.vader.polarity_scores("wilt"))

    for sentence in sentences:
        darth.learn_text_simple(sentence)
        vs = darth.vader.polarity_scores(sentence)
        print("{:-<65} {}".format(sentence, str(vs)))
    return

vaderPlayground()
darthPlayground()
```

which resulted in the following output:
```
-------------------------------------------
VADER Performance on Sentences:
-------------------------------------------
VADER is smart, handsome, and funny.----------------------------- {'neg': 0.0, 'neu': 0.254, 'pos': 0.746, 'compound': 0.8316}
VADER is smart, handsome, and funny!----------------------------- {'neg': 0.0, 'neu': 0.248, 'pos': 0.752, 'compound': 0.8439}
VADER is very smart, handsome, and funny.------------------------ {'neg': 0.0, 'neu': 0.299, 'pos': 0.701, 'compound': 0.8545}
VADER is VERY SMART, handsome, and FUNNY.------------------------ {'neg': 0.0, 'neu': 0.246, 'pos': 0.754, 'compound': 0.9227}
VADER is VERY SMART, handsome, and FUNNY!!!---------------------- {'neg': 0.0, 'neu': 0.233, 'pos': 0.767, 'compound': 0.9342}
VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!--------- {'neg': 0.0, 'neu': 0.294, 'pos': 0.706, 'compound': 0.9469}
VADER is not smart, handsome, nor funny.------------------------- {'neg': 0.646, 'neu': 0.354, 'pos': 0.0, 'compound': -0.7424}
The book was good.----------------------------------------------- {'neg': 0.0, 'neu': 0.508, 'pos': 0.492, 'compound': 0.4404}
At least it isn't a horrible book.------------------------------- {'neg': 0.0, 'neu': 0.678, 'pos': 0.322, 'compound': 0.431}
The book was only kind of good.---------------------------------- {'neg': 0.0, 'neu': 0.697, 'pos': 0.303, 'compound': 0.3832}
The plot was good, but the characters are uncompelling and the dialog is not great. {'neg': 0.327, 'neu': 0.579, 'pos': 0.094, 'compound': -0.7042}
Today SUX!------------------------------------------------------- {'neg': 0.779, 'neu': 0.221, 'pos': 0.0, 'compound': -0.5461}
Today only kinda sux! But I'll get by, lol----------------------- {'neg': 0.127, 'neu': 0.556, 'pos': 0.317, 'compound': 0.5249}
Make sure you :) or :D today!------------------------------------ {'neg': 0.0, 'neu': 0.294, 'pos': 0.706, 'compound': 0.8633}
Catch utf-8 emoji such as such as 💘 and 💋 and 😁------------------ {'neg': 0.0, 'neu': 0.615, 'pos': 0.385, 'compound': 0.875}
Not bad at all--------------------------------------------------- {'neg': 0.0, 'neu': 0.513, 'pos': 0.487, 'compound': 0.431}
Watch the rose wilt.--------------------------------------------- {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
-------------------------------------------
DARTH-VADER Performance on Sentences:
-------------------------------------------
VADER is smart, handsome, and funny.----------------------------- {'neg': 0.0, 'neu': 0.254, 'pos': 0.746, 'compound': 0.8316}
VADER is smart, handsome, and funny!----------------------------- {'neg': 0.0, 'neu': 0.248, 'pos': 0.752, 'compound': 0.8439}
VADER is very smart, handsome, and funny.------------------------ {'neg': 0.0, 'neu': 0.299, 'pos': 0.701, 'compound': 0.8545}
VADER is VERY SMART, handsome, and FUNNY.------------------------ {'neg': 0.0, 'neu': 0.246, 'pos': 0.754, 'compound': 0.9227}
VADER is VERY SMART, handsome, and FUNNY!!!---------------------- {'neg': 0.0, 'neu': 0.233, 'pos': 0.767, 'compound': 0.9342}
VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!--------- {'neg': 0.0, 'neu': 0.294, 'pos': 0.706, 'compound': 0.9469}
VADER is not smart, handsome, nor funny.------------------------- {'neg': 0.646, 'neu': 0.354, 'pos': 0.0, 'compound': -0.7424}
The book was good.----------------------------------------------- {'neg': 0.0, 'neu': 0.508, 'pos': 0.492, 'compound': 0.4404}
At least it isn't a horrible book.------------------------------- {'neg': 0.0, 'neu': 0.678, 'pos': 0.322, 'compound': 0.431}
The book was only kind of good.---------------------------------- {'neg': 0.0, 'neu': 0.697, 'pos': 0.303, 'compound': 0.3832}
The plot was good, but the characters are uncompelling and the dialog is not great. {'neg': 0.32, 'neu': 0.519, 'pos': 0.16, 'compound': -0.6587}
Today SUX!------------------------------------------------------- {'neg': 0.779, 'neu': 0.221, 'pos': 0.0, 'compound': -0.5461}
Today only kinda sux! But I'll get by, lol----------------------- {'neg': 0.103, 'neu': 0.385, 'pos': 0.512, 'compound': 0.812}
Make sure you :) or :D today!------------------------------------ {'neg': 0.0, 'neu': 0.187, 'pos': 0.813, 'compound': 0.919}
Catch utf-8 emoji such as such as 💘 and 💋 and 😁------------------ {'neg': 0.0, 'neu': 0.554, 'pos': 0.446, 'compound': 0.9022}
Not bad at all--------------------------------------------------- {'neg': 0.0, 'neu': 0.513, 'pos': 0.487, 'compound': 0.431}
Watch the rose wilt.--------------------------------------------- {'neg': 0.474, 'neu': 0.526, 'pos': 0.0, 'compound': -0.4019}
-------------------------------------------
```

## Contact

To contact me, please email aathreyakadambi@gmail.com.
