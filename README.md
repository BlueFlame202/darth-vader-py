# DARTH VADER Sentiment Analysis

An extension of VADER Sentiment Analysis. Valence Aware Dictionary and sEntiment Reasoner (VADER) is a lexicon and rule-based sentiment tool designed to measure sentiment of text from social media. DARTH VADER is a tool that utilizes WordNets to learn words that are not contained within the vader lexicon. While VADER is based on a gold-standard lexicon, resulting in sentiments for words dictated by humans, DARTH VADER attempts to create a dynamic lexicon which is able to update and accomodate for words that are not contained within the lexicon. This way, texts that contain words that are not in the lexicon can still be analyzed accurately. This is a double edged sword, since while DARTH VADER can give more accurate results on texts containing words not in the lexicon, it can also assign sentiments that are not very accurate to words not contained in the lexicon. However, the chances of DARTH VADER assigning false sentiments is minimized by controlling DARTH's threshold and determining how DARTH VADER updates the valence of new words.

## Table of Contents


## Introduction

The VADER Sentiment Tool is a very good tool for assigning sentiment scores to text from social media. However, it does experience limitations. For example, 

* Some words are not in the lexicon. 



* It does not consider context of words when assigning sentiment. 

For an example of why this is an issue, consider the word "hard". One definition of hard is "not easy; requiring great physical or mental effort to accomplish or comprehend or endure" (taken from ```wn.synsets("hard")[0].definition()```). Another definition is "resisting weight or pressure" (taken from ```wn.synsets("hard)[2].definition()```). Clearly, these two meanings should be assigned different sentiments. This is a difficult task, and DARTH attempts to resolve at least a portion of the issues caused by this limitation.

## Recent Updates

darth.py has been successfully implemented. Scores on certain texts are more accurate, and in general darth is more sensitive to texts since it is able to learn words.
