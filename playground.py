from vaderSentimentu import SentimentIntensityAnalyzer
    #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
    #from vaderSentiment import SentimentIntensityAnalyzer

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

# ISSUES WITH USING VADER FOR SENTIMENT ANALYSIS
# --------------------------------------------------------------------------
# 1: the VADER model is pretty simplistic and doesn't account for lots of sentence structures that may change the meaning of a message 
#       other than 'but', and too many sentence structures are simply hardcoded in... VADER isn't dynamic and is very stiff
# 2: the 'compound' measure isn't always the best because it sums up positive and negative values so a very polar message could have a
#       compound score of zero. It is a much better idea to maybe take (pos**2 + neg**2) or (pos + neg) as an overall
#       message intensity score. High intensity with low compound could be an indicator of a human message
# 3: Some words, such as 'Wilt', are not in the lexicon, making it not the best model
# 4: A message like "Tesla to deliver China-made Model Y SUVs this month $TSLA" is neutral to a machine which has no goal, but to a human
#       interested in investing in Tesla, a message with neutral words can be positive or negative (in this case positive)
# 5: Overall, using a better trained model might be a much better alternative 

# Look at this snippet:
# # discriminate between positive, negative and neutral sentiment scores
#            pos_sum, neg_sum, neu_count = self._sift_sentiment_scores(sentiments)
#
#            if pos_sum > math.fabs(neg_sum):
#                pos_sum += punct_emph_amplifier
#            elif pos_sum < math.fabs(neg_sum):
#                neg_sum -= punct_emph_amplifier
#
#            total = pos_sum + math.fabs(neg_sum) + neu_count
#            pos = math.fabs(pos_sum / total)
#            neg = math.fabs(neg_sum / total)
#            neu = math.fabs(neu_count / total)
# THERE ARE WAYYY MORE NEUTRAL WORDS IN ANY PIECE OF TEXT! The lexicon itself is very small, so pos and negative values get heavily 
# weighed down in relatively longer messages. This is why VADER may have performed better in very short tweets, but likely doesn't generalize
# instead, it's possible to try a modified vaderSentiment where we don't consider a neutrality score. compound is already a good neutrality
# score! We don't need another one.

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

# words that aren't in the lexicon: fall, wilt, falling
# best_synset is a double edged sword
# vader-lexicon is optimized for social media but since these are like headlines it isn't necessarily optimal!

vaderPlayground()
print
darthPlayground()
