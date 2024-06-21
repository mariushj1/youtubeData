from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import isodate
import pandas as pd
import re
import os
import scrapetube
import requests

# Definerer kanal id
channel_id = "UCbvwGzSKXa31P6yDRyoNJnA"

# Definerer youtube API nøgle
API_KEY = ""

# Indhente data om kanal fra API
channel_data_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
response = requests.get(channel_data_url)
channel_data = response.json()
channel_title = channel_data['items'][0]['snippet']['title']

# Mappe til at gemme filer
folder_path = os.path.join(os.getcwd(), f"channels/{channel_title}")

# Checker om mappen eksisterer
if not os.path.exists(folder_path):
    # Laver mappe hvis den ikke eksisterer
    os.makedirs(folder_path)
    print("Main folder created successfully.")
else:
    print("Main folder already exists.")


# Laver funktion til at gemme video id's som liste
def get_video_ids(channel_id):
    videos = scrapetube.get_channel(channel_id)
    video_ids = [video['videoId'] for video in videos]
    return video_ids

# Indhenter video URL's for kanal
urls = get_video_ids(channel_id)

# Laver tom dataframe
youtube_data = pd.DataFrame(index = [0], columns=range(8))
youtube_data.columns = ["id", "title", "views", "likes", "comments", "duration", "content", "upload_date"]


# Laver tællere
successful_videos = 0
error_videos = 0

# Looper igennem hvert URL
for url in urls:
    try:
        # Finder video ID 
        video_id = url.split("v=")[-1]
        # Indhenter view, like & comment count
        video_data_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
        response_video_data = requests.get(video_data_url)
        api_video_data = response_video_data.json()
        if 'items' in api_video_data and len(api_video_data['items']) > 0:
            view_count = api_video_data['items'][0]['statistics'].get('viewCount', 0)
            like_count = api_video_data['items'][0]['statistics'].get('likeCount', 0)
            comment_count = api_video_data['items'][0]['statistics'].get('commentCount', 0)
        else:
            raise ValueError("No statistics found for video")
        
        # Indhenter titlen og publishdate
        video_data_url2 = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
        response_video_data2 = requests.get(video_data_url2)
        api_video_data2 = response_video_data2.json()
        if 'items' in api_video_data2 and len(api_video_data2['items']) > 0:
            video_title = api_video_data2['items'][0]['snippet']['title']
            publish_date = api_video_data2['items'][0]['snippet']['publishedAt']
        else:
            raise ValueError("No snippet found for video")
        
        # Indhenter længde på video
        video_data_url3 = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={API_KEY}'
        response_video_data3 = requests.get(video_data_url3)
        api_video_data3 = response_video_data3.json()
        if 'items' in api_video_data3 and len(api_video_data3['items']) > 0:
            duration = api_video_data3['items'][0]['contentDetails']['duration']
            video_duration = isodate.parse_duration(duration)
        else:
            raise ValueError("No content details found for video")
        
        # Indhenter undertekster for video
        captions = YouTubeTranscriptApi.get_transcript(video_id)

        # Formaterer undertekster
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(captions)

        # Renser teksen
        text_formatted = text_formatted.replace("\n", " ")
        text_formatted = re.sub(r'\[.*?\]', '', text_formatted)
        text_formatted = re.sub(r'\b(\w+)\b', lambda match: match.group().lower(), text_formatted)
        text_formatted = re.sub(r'\s+', ' ', text_formatted)

        # Laver en ny række med data
        new_row = [video_id, video_title, view_count, like_count, comment_count, video_duration, text_formatted, publish_date]
        youtube_data.loc[len(youtube_data)] = new_row
        
        print(f"Data saved for video - {video_title}\n")

        # Tæller antal success
        successful_videos += 1

    except Exception as e:
        print(f"Error processing video {video_id}: {e}")
        # Tæller antal videoer med fejl
        error_videos += 1
        continue

# Print summary
print(f"Total videos processed: {len(urls)}\n")
print(f"Videos processed successfully: {successful_videos}\n")
print(f"Videos with errors: {error_videos}\n")

# Fjerner første tomme række i dataframe
youtube_data = youtube_data.dropna()
 
# Gemmer dataframe som csv
file_path_csv = os.path.join(folder_path, "youtube_data.csv")
youtube_data.to_csv(file_path_csv, index=False)

print(f"Channel data for {channel_title} saved at {folder_path}\n")

# Gemmer billede af kanal
url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
# Laver API request
response = requests.get(url)
data = response.json()

# Henter kanal billede URL
image_url = data['items'][0]['snippet']['thumbnails']['high']['url']

# Downloader billedet
image_data = requests.get(image_url).content

# Gemmer billedet som en fil
with open(os.path.join(folder_path, "channel_image.jpg"), 'wb') as f:
    f.write(image_data)

print(f"Channel image for {channel_title} saved")
    