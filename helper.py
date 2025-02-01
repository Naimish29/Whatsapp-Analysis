from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selected_user, df):
    # Filter messages based on selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove media messages
    df = df[df['message'].str.strip() != '<Media omitted>']

    # Fetch the number of messages
    num_messages = df.shape[0]

    # Fetch the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    return num_messages, len(words), num_media_messages


def most_busy_users(df):
    x = df['user'].value_counts().head()
    user_counts = df['user'].value_counts() / df.shape[0] * 100  # Calculate the percentage
    percent_df = round(user_counts, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})  # Round and rename columns

    return x, percent_df


def create_wordcloud(selected_user, df):
    # Filter the DataFrame for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove media messages
    df = df[df['message'].str.strip() != '<Media omitted>']

    # Convert all messages to strings and drop missing (NaN) values
    df['message'] = df['message'].astype(str).fillna('')

    # Generate the word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc



def most_common_words(selected_user, df):
    # Read stop words from the file
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = [word.strip().lower() for word in f.read().splitlines()]  # Ensure uniform formatting

    # Filter messages based on selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notifications and media messages
    temp = df[(df['user'] != 'group_notification') & (df['message'].str.strip() != '<Media omitted>')]

    # Create a list of words excluding stop words
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Create a DataFrame for the most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap