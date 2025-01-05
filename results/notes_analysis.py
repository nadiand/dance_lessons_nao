import re
import matplotlib.pyplot as plt
import pandas as pd
from nltk import ngrams, download, FreqDist
from nltk.probability import MLEProbDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
download('stopwords')

stop_words = stopwords.words('english')
stop_words.extend(['bit', 'seems', 'participant', 'robot', 'seem', 'Participant'])

def plot_dist_as_cloud(word_dist):
    prob_dist = MLEProbDist(word_dist)
    viz_dict = {}
    for word_tuple in word_dist:
        string = ' '.join(word_tuple)
        viz_dict[string] = prob_dist.prob(word_tuple)

    cloud = WordCloud(width=400,height=200).generate_from_frequencies(viz_dict)
    
    plt.figure(figsize = (25,25))
    plt.imshow(cloud, interpolation='bilinear')

    plt.axis("off")


def extract_ngram_freqs(token_list, n):
    cleaned_tokens = []
    for word in token_list:
        if word not in stop_words:
            cleaned_tokens.append(word)
    grams = list(ngrams(cleaned_tokens, n))
    return grams


def notes_ngrams(participants, n):
    all_ngrams = []
    punctuations = [',', '.', ':D', '(', ')']

    for notes in participants:
        tokens = notes.split(' ')
        tokens = [re.sub(r'[^\w\s]', '', x) for x in tokens]
        tokens = [t for t in tokens if t != '']
        tokens = [t for t in tokens if t not in punctuations]
        tokens = [x.replace("'", "") for x in tokens]

        x_ngrams = extract_ngram_freqs(tokens, n=n)
        x_ngrams = [x for x in x_ngrams if not ';' in x]
        all_ngrams.append(x_ngrams)

    return all_ngrams


def find_ngrams_and_plot(fanwork_ngrams, n):
    word_dist = FreqDist()
    for grams in fanwork_ngrams:
      word_dist.update(FreqDist(grams))
    print(f'Found {len(word_dist)} unique n-grams for n = {n}')

    most_common = word_dist.most_common(25)
    for word_tuple in most_common:
      print(word_tuple)
    plot_dist_as_cloud(word_dist)

n = 2
notes = pd.read_csv('participant_notes.csv')
# notes = notes[notes['pid'] < 11]
all_ngrams = notes_ngrams(notes['notes'], n)
find_ngrams_and_plot(all_ngrams, n)