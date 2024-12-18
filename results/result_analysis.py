import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


def plot_results(data):
    # TODO can easily extend this with the rest of the columns
    values = [data['confidence'].tolist(), data['interesting'].tolist()]
    plt.boxplot(values)
    plt.xticks(ticks=[1,2],labels=['confidence', 'interesting'])
    plt.show()


def group_results(data, attribute):
    group_data, group_labels = [], []
    for val in data[attribute].unique():
        group_labels.append(val)
        group_data.append(data[data[attribute] == val])

    fig, axs = plt.subplots(1, len(group_labels), figsize=(30, 10))
    for i, age_group in enumerate(group_data):
    # TODO can easily extend this with the rest of the columns
        values = [age_group['confidence'].tolist(), age_group['interesting'].tolist()]
        axs[i].boxplot(values)
        axs[i].set_xticks(ticks=[1,2],labels=['confidence', 'interesting'])
        axs[i].set_title(group_labels[i])
    
    plt.show()


if __name__ == "__main__":
    short_col_names = {'Tijdstempel': 'time', 'Participant number': 'pid', 'What is your age?': 'age', 'How often do you perform some form of physical activity? (at least half an hour of e.g., exercise, running, dancing)': 'activity_level',\
                        'Which of these statements is most fitting for you?': 'dancing', 'I enjoyed dancing with NAO': 'enjoy_dance_nao', 'Learning dances with NAO was fun': 'learning_fun',\
                        'I would like to dance with NAO again': 'dance_again', 'I found the dance activities interesting': 'interesting', "I felt I was able to follow NAO's dance instructions well": 'follow_instructions', \
                        'I felt confident while dancing with NAO': 'confidence', 'I improved at dancing during the session': 'improvement', "NAO's movements were natural and easy to follow": 'natural_moves', \
                        'NAO was responsive to my actions': 'responsive', 'I felt NAO understood how well I was doing': 'nao_understands', "NAO's instructions were clear and helpful": 'clear_instructions', \
                        'I felt comfortable dancing with NAO': 'comfort', 'I felt safe while interacting with NAO': 'safety', "NAO's movements were predictable": 'predictable',\
                        'I put effort into learning the dances': 'effort', 'I think dancing with NAO is a good way to be more active': 'nao_good_active', 'I would recommend dancing with NAO to others': 'recommend'}
    raw_data = pd.read_csv('participant_data.csv')
    data = raw_data.rename(columns=short_col_names)

    # full results
    # plot_results(data)

    # results split on the three personal attributes
    # group_results(data, 'age')
    # group_results(data, 'dancing')
    group_results(data, 'activity_level')