import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu as whitney_houston
from scipy.stats import kruskal

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
        axs[i].set_ylabel("Score")
    
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
    #print(data['age'])
    data['age'] = data['age'].map(age_mapping)
    #print(data['age'])

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

def stat_test_condition(data):
    values = data[ALL_QUESTIONS]
    robot_cond = values[data['pid'] < 11]
    video_cond = values[data['pid'] > 10]
    # print('robot:', robot_cond)
    # print('video:', video_cond)
    stats = []
    p_vals = []
    for question in ALL_QUESTIONS:
        #print('QUESTION:', question)
        robot_scores = robot_cond[question].to_list()
        video_scores = video_cond[question].to_list()
        
        stat, p_val = whitney_houston(robot_scores, video_scores)
        stats.append(stat)
        p_vals.append(p_val)

    #print(p_vals)

    return p_vals, stats

def stat_test_activity_level(data):
    values = data[ALL_QUESTIONS]
    group_never = values[data['activity_level'] == 'Never']
    group_once = values[data['activity_level'] == 'Once a week']
    group_23week = values[data['activity_level'] == '2-3 times a week']
    group_4 = values[data['activity_level'] == '4+ times a week']

    stats = []
    p_vals = []
    for question in ALL_QUESTIONS:
        #print('QUESTION:', question)
        never_scores = group_never[question].to_list()
        once_scores = group_once[question].to_list()
        x23week_scores = group_23week[question].to_list()
        x4_scores = group_4[question].to_list()
        
        stat, p_val = kruskal(never_scores, once_scores, x23week_scores, x4_scores)
        stats.append(stat)
        p_vals.append(p_val)

        #print('pval:', p_val)
        # print('--------------------------------')

    #print(p_vals)

    return p_vals, stats

    
def stat_test_dancing(data):
    values = data[ALL_QUESTIONS]
    group_never = values[data['dancing'] == 'I never dance']
    group_rarely = values[data['dancing'] == 'I dance only rarely (at events, parties, etc)']
    group_often = values[data['dancing'] == 'I dance often (at least once a week)']

    stats = []
    p_vals = []
    for question in ALL_QUESTIONS:
        #print('QUESTION:', question)
        never_scores = group_never[question].to_list()
        rarely_scores = group_rarely[question].to_list()
        often_scores = group_often[question].to_list()
        
        stat, p_val = kruskal(never_scores, rarely_scores, often_scores)
        stats.append(stat)
        p_vals.append(p_val)

        #print('pval:', p_val)
        # print('--------------------------------')

    #print(p_vals)

    return p_vals, stats





if __name__ == "__main__":
    short_col_names = {'Tijdstempel': 'time', 'Participant number': 'pid', 'What is your age?': 'age', 'How often do you perform some form of physical activity? (at least half an hour of e.g., exercise, running, dancing)': 'activity_level',\
                        'Which of these statements is most fitting for you?': 'dancing', 'I enjoyed dancing with NAO': 'enjoy_dance_nao', 'Learning dances with NAO was fun': 'learning_fun',\
                        'I would like to dance with NAO again': 'dance_again', 'I found the dance activities interesting': 'interesting', "I felt I was able to follow NAO's dance instructions well": 'follow_instructions', \
                        'I felt confident while dancing with NAO': 'confidence', 'I improved at dancing during the session': 'improvement', "NAO's movements were natural and easy to follow": 'natural_moves', \
                        'NAO was responsive to my actions': 'responsive', 'I felt NAO understood how well I was doing': 'nao_understands', "NAO's instructions were clear and helpful": 'clear_instructions', \
                        'I felt comfortable dancing with NAO': 'comfort', 'I felt safe while interacting with NAO': 'safety', "NAO's movements were predictable": 'predictable',\
                        'I put effort into learning the dances': 'effort', 'I think dancing with NAO is a good way to be more active': 'nao_good_active', 'I would recommend dancing with NAO to others': 'recommend'}
    raw_data = pd.read_csv("C:/Users/luukn/OneDrive/Documenten/RadboudUniversity/Master/Year1/Q1/HRI/robot-jumpstarter-python3-master/robot-jumpstarter-python3-master/python3/results/participant_data.csv")
    data = raw_data.rename(columns=short_col_names)

    # Apply reverse scoring for questions
    for question in ALL_QUESTIONS:
        data[question] = data[question].apply(lambda x: 8 - x if not pd.isna(x) else x)

    # Significance testing
    pvals_cond, stats_cond = stat_test_condition(data)
    pvals_activity, stats_activity = stat_test_activity_level(data)
    pvals_dancing, stats_dancing = stat_test_dancing(data)

    print('pvals based on condition: ', pvals_cond, '\n')
    print('pvals based on activity level: ', pvals_activity, '\n')
    print('pvals based on dancing frequency: ', pvals_dancing, '\n')

    # full results
    plot_results(data)

    # # # results split on the three personal attributes
    group_results(data, 'age')
    group_results(data, 'dancing')
    group_results(data, 'activity_level')
    correlation_heatmap(data)






