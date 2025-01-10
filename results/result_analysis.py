import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

ALL_QUESTIONS = ['enjoy_dance_nao', 'learning_fun', 'dance_again', 'interesting', 'follow_instructions', 'confidence', 'improvement', 'natural_moves', 'responsive', 'nao_understands', 'clear_instructions', 'comfort', 'safety', 'predictable', 'effort', 'nao_good_active', 'recommend']
QUESTION_GROUPS = {'enjoyment': ['enjoy_dance_nao', 'learning_fun', 'dance_again', 'interesting'], \
                    'competence': ['follow_instructions', 'confidence', 'improvement'], \
                    'social': ['natural_moves', 'responsive', 'nao_understands', 'clear_instructions'], \
                    'comfort': ['comfort', 'safety', 'predictable'], \
                    'value': ['effort', 'nao_good_active', 'recommend']}

def plot_results(data, group=None):
    if group is not None:
        values = [QUESTION_GROUPS[group]]
    else:
        values = data[ALL_QUESTIONS]

    fig, axs = plt.subplots(2, 1, sharey=True, sharex=True, figsize=(20, 5))

    axs[0].boxplot(values[data['pid'] < 11])
    axs[0].set_title('Questionnaire results for interactive setting')
    axs[0].set_ylabel("Score")  # Y-label for the first subplot

    axs[1].boxplot(values[data['pid'] > 10])
    axs[1].set_title('Questionnaire results for non-interactive setting')
    axs[1].set_ylabel("Score")  # Y-label for the second subplot

    # Set a single x-label for both subplots
    axs[1].set_xlabel("Question number")

    plt.subplots_adjust(hspace=0.3)
    plt.show()


def group_results(data, attribute, group=None):
    group_data, group_labels = [], []
    for val in data[attribute].unique():
        group_labels.append(val)
        group_data.append(data[data[attribute] == val])

    fig, axs = plt.subplots(len(group_labels), 1, sharex=True, figsize=(30, 10))
    for i, age_group in enumerate(group_data):
        values = age_group[ALL_QUESTIONS] #QUESTION_GROUPS[group]]
        axs[i].boxplot(values)
        axs[i].set_title(group_labels[i])
    
    plt.subplots_adjust(hspace=0.3)
    plt.show()

def correlation_heatmap(data):
    # Define mappings
    physical_activity_mapping = {
        "Never": 0,
        "Once a week": 1,
        "2-3 times a week": 2,
        "4+ times a week": 3
    }
    dance_activity_mapping = {
        "I never dance": 0,
        "I dance only rarely (at events, parties, etc)": 1,
        "I dance often (at least once a week)": 2
    }
    age_mapping = {
        '18-20': 0,
        '21-24': 1,
        '25-29': 2,
        '30+': 3
    }

    # Apply mappings to create numerical columns
    data['activity_level'] = data['activity_level'].map(physical_activity_mapping)
    data['dancing'] = data['dancing'].map(dance_activity_mapping)
    print(data['age'])
    data['age'] = data['age'].map(age_mapping)
    print(data['age'])

    # Ensure all columns are numeric for correlation
    correlations = data[['activity_level', 'dancing', 'age'] + ALL_QUESTIONS].corr()

    # Extract correlations of attributes with questionnaire responses
    activity_corr = correlations.loc[['activity_level', 'dancing', 'age'], ALL_QUESTIONS].T

    # Plot the heatmap
    plt.figure(figsize=(10, 12))
    sns.heatmap(activity_corr, annot=True, cmap="coolwarm", cbar=True)
    plt.title("Correlation of Questionnaire Responses with Age, Physical, and Dance Activity")
    plt.xlabel("Attributes (Activity and Age)")
    plt.ylabel("Questions")
    plt.yticks(rotation=0)
    plt.tight_layout()
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

    # Apply reverse scoring for questions
    for question in ALL_QUESTIONS:
        data[question] = data[question].apply(lambda x: 8 - x if not pd.isna(x) else x)

    # full results
    plot_results(data)

    # # results split on the three personal attributes
    # group_results(data, 'age')
    # group_results(data, 'dancing')
    # group_results(data, 'activity_level')
    correlation_heatmap(data)