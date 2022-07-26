#!/usr/bin/env python
# coding: utf-8

from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
from pprint import pprint


api_key = 'AIzaSyDs6CAMKo4YaEfT0G9X1l2ZsS42cLndPYA'

channel_ids = ['UCMdclmyCrodWWl-OpNAfYLA']

youtube = build('youtube', 'v3', developerKey=api_key)


# ## Function to get channel level statistics

def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    response = request.execute() 
    print(response)
    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    
    return all_data



channel_statistics = get_channel_stats(youtube, channel_ids)



channel_data = pd.DataFrame(channel_statistics)


print('Channel level statistics')
pprint(channel_data)




# ## Function to get video ids




playlist_id = channel_data.loc[channel_data['Channel_name']=='Thermax Limited', 'playlist_id'].iloc[0]


def get_video_ids(youtube, playlist_id):
    
    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 500)
    response = request.execute()
    
    video_ids = []
    
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token)
            response = request.execute()
    
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
        
    return video_ids



video_ids = get_video_ids(youtube, playlist_id)


print('number of videos found across all the channels')
print(len(video_ids))


# ## Function to get video details


def get_video_details(youtube, video_ids):
    all_video_stats = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50]))
        response = request.execute()
        
        for video in response['items']:
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes = video['statistics']['likeCount'],
#                                Dislikes = video['statistics']['dislikeCount'],
                               Comments = video['statistics']['commentCount']
                               )
            all_video_stats.append(video_stats)
    
    return all_video_stats



video_details = get_video_details(youtube, video_ids)



video_data = pd.DataFrame(video_details)

print('Video Data')
pprint(video_data)

# video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
# video_data['Views'] = pd.to_numeric(video_data['Views'])
# video_data['Likes'] = pd.to_numeric(video_data['Likes'])
# # video_data['Dislikes'] = pd.to_numeric(video_data['Dislikes'])
# # video_data['Views'] = pd.to_numeric(video_data['Views'])





# top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)



# top10_videos



# ax1 = sns.barplot(x='Views', y='Title', data=top10_videos)



# video_data



# video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')



# video_data



# videos_per_month = video_data.groupby('Month', as_index=False).size()



# videos_per_month



# sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=sort_order, ordered=True)



# videos_per_month = videos_per_month.sort_index()


# ax2 = sns.barplot(x='Month', y='size', data=videos_per_month)



# video_data.to_csv('Video_Details(Ken Jee).csv')



