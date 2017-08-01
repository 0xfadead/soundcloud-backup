# soundcloud-backup

A python script (version 3.6.2) that uses SoundCloud's streaming interface to clone all the tracks (sounds?) on a user's page even if a track has downloads disabled or the downloads are maxed out (it just won't work for tracks that only offer previews to free users). The tracks (each mp3s at 128kbps) are saved in a zip archive using deflate. I made the executive decision to go with zip because I'm fairly confident that most SoundCloud users are normies that would flip their shit if they saw a tarball.

## Using the script

```python backup.py backup.py [-h] [-C CLIENT_ID] [-A NAME] [-Z CHUNK_SIZE] [-d DELAY_TIME] url```

```python backup.py https://soundcloud.com/beniceandsettledown --delay-time 3 --chunk-size 2048```

## Options

-C, --client-id&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A custom client id. You should probably specify this if you are getting a 429 response

-A, --name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Name of the archive

-Z, --chunk-size&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The chunk size in which pieces of the mp3 file will be saved (default: 1024)

-d, --delay-time&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify a delay time (in seconds) between each track download

## NOTICES

If you notice that tracks aren't downloading and you are getting a 429 response that means SoundCloud is probably throttling you and you'll need to wait 24 hours because your client id is burned. I haven't tested this, but you should be able to make another account (using a VPN preferably) and just view the network traffic as you download a track to find your new client id.

This script gets up *all* the tracks on a page. If you are looking to download just one or two specific tracks, use [Yan's webpage](https://diracdeltas.github.io/SoundDrop/) (where this script draws its inspiration).
