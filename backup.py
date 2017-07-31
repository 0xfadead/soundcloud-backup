import requests
import zipfile
import tempfile
import sys
import argparse
import os
import json

CLIENT_ID = 'JlZIsxg2hY5WnBgtn3jfS0UYCl0K8DOg'
INFO_BASE_URL = 'https://api.soundcloud.com/resolve.json'
TRACKS_BASE_URL = 'https://api.soundcloud.com/users/{:d}/tracks'

ARCHIVE_SKELETON = '{:s}-{:s}.zip'
# SoundCloud streamable tracks are transcoded
# at 128 kbps and are in mp3 format
STREAM_SKELETON = '{:s}.mp3'

def error(msg):
    print(msg, file=sys.stderr)

def json_request(scurl, payload):
    try:
        r = requests.get(scurl, params=payload) 
        if r.status_code != requests.codes.ok:
            error('Could not reach: {}'.format(str(r.status_code)))
            return {}
        return r.json()
    except requests.exceptions.RequestException as e:
        error(e)
        return {}

def user_info(scurl):
    data = json_request(
        INFO_BASE_URL, {
            'url': scurl, # encode (?)
            'client_id': CLIENT_ID
        })
    if not bool(data): 
        return [None for _ in range(3)] 
    return data.get('id'), data.get('username'), data.get('permalink')

def user_tracks(userid):
    # todo: downloadable + download_url (?)
    target_keys = ('id', 'streamable', 'stream_url', 'permalink')
    data = json_request(
        TRACKS_BASE_URL.format(userid), 
        {'client_id': CLIENT_ID})
    return [{k: unfiltered.get(k) for k in target_keys} 
                for unfiltered in data ]

def save_audio_stream(fout, streamurl):
    r = requests.get(streamurl, 
        {'client_id' : CLIENT_ID},
        stream=True)
    if r.status_code != requests.codes.ok:
        error('Could not reach: {}'.format(str(r.status_code)))
        return False
    for chunk in r.iter_content(chunk_size=1024):
        if chunk: 
            fout.write(chunk)
    return True

def main():
    # Get command line args.
    # Everyone's favorite thing about coding...
    parser = argparse.ArgumentParser()

    parser.add_argument('url', 
            type=str,
            help="Url of SoundCloud profile you'd like to backup"
    ) 
    parser.add_argument('-A', '--name',
            type=str,
            help="Name of the archive"
    )

    args = parser.parse_args()

    url = args.url
    if ('soundcloud.com' not in url or
            not url.startswith('https://')):
        print('Please use a valid HTTPS Soundcloud Url')
        return

    uid, uname, ulink = user_info(url)
    if uid is None:
        print('Could not locate: {}'.format(artist_url))
        return

    tracks = user_tracks(uid)
    if not bool(tracks):
        print('{} has no songs!'.format(artist_url))
        return
    
    zipname = (ARCHIVE_SKELETON.format(uname, ulink) 
            if args.name is None else args.name)

    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as archive:
        for track in tracks:
            if track['streamable']:
                with tempfile.NamedTemporaryFile('wb') as f:
                    if save_audio_stream(f, track['stream_url']):
                        archive.write(f.name, arcname=STREAM_SKELETON
                                .format(track['permalink']))
                    else:
                        print('Could not download: {}'.format(track['permalink']))

if __name__ == '__main__':
    main()

