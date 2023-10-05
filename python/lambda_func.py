import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
from datetime import datetime
import boto3


def upload_to_s3(csv_file):
    s3 = boto3.resource('s3')
    bucket_name = 'spotify-data-weekly'
    object = s3.Object(bucket_name, csv_file)
    object.put()



# get song info from the playlist and save it to a CSV file

def retrive_data(results):

    spotify_data_file = f'/tmp/spotify_{datetime.now().strftime("%m_%d_%Y")}.csv'  
    
    with open(spotify_data_file, mode='w', newline='') as csv_file:

        fieldnames = ['Track Name', 'Artist', 'Album', 'Release Date', 'Duration']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for track in results['items']:

            track_info = track['track']

            track_name = track_info['name']

            artists = [track_info['artists'][0]['name']]

            first_artist = artists[0] if artists else 'N/A'  # Take the first artist or use 'N/A' if no artist is found

            album_name = track_info['album']['name']

            release_date = track_info['album']['release_date']

            duration = track_info ['duration_ms']

            writer.writerow({'Track Name': track_name, 'Artist': first_artist, 'Album': album_name, 'Release Date': release_date, 'Duration' : duration})
    
    return spotify_data_file

def upload_to_s3(csv_file_path,bucket_name,s3_key):
    s3 = boto3.client('s3')
    s3.upload_file(csv_file_path,bucket_name,s3_key)




# Function to retrieve song info from a playlist

def get_playlist_tracks(sp):

    playlist_uri = '37i9dQZEVXbMWDif5SCBJq'

    results = sp.playlist_tracks(playlist_uri)

    return results
    

# Initialize Spotipy with credentials

def spotify_API_conn(client_id, client_secret):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp
      


# Lambda Handler Func

def lambda_handler(event, context):
        
        client_id = 'your credentials'
        client_secret = 'your credentials'
        bucket_name = 'spotify-data-weekly'
        s3_key = f'/weekly_data/spotify_{datetime.now().strftime("%m_%d_%y")}.csv'
        sp = spotify_API_conn(client_id,client_secret)
        results = get_playlist_tracks(sp)
        csv_file_path = retrive_data(results)
        
        upload_to_s3(csv_file_path,bucket_name,s3_key)

        #after succefully retrive code
       
        return {

            'statusCode':200,

            'body':'CSV file uploaded to S3'

        }


        


        
         
        
        

        
