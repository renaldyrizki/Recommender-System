import csv
from tempfile import TemporaryFile
import spotipy
import spotipy.util as util
import pymongo
from pymongo import MongoClient
client = MongoClient()

idartis = [ '5OZXWMwDhlYBRvoOfcX0sk', '4rUYk0fV0Z4pOtwVbEAyK9', '4cgBCGxtlfap2g6jveB7du', '4ubEZ6sMsrrbQChueyouCC', '2l8I5pWUnfF7bMK1z6EJRk', '2Ooa3TrmlskyBftzenv6xQ',
           '6q87vizIEdEN4NvlR6mjfT', '2owBL6a90fnWufVtP70K8f', '6XyY86QOPPrYVGvF9ch6wz', '3e7awlrlDSwF3iM0WBjGMp', '2MqhkhX4npxDZ62ObR5ELO', '74XFHRwlV6OrjEM0A2NCMF',
            '4AK6F7OLvEQ5QYCBNiQWHq', '18PmEN8ZiHBQlDpxrgR2xs', '0b4XpbAVDPngjDTbcSWH8N', '30qVSJGhPhrZLKG0H9DMA9',
            '0ygQsC5td2maGmglpzd7tp', '3t4MHnVggiFLOuSSh4odBk', '57A85GCAJn0reNAez6Hswt','0hCNtLu0JehylgoiP8L4Gh',
            '2hcsKca6hCfFMwwdbFvenJ','3Nrfpe0tUJi4K4DXYWgMUX','6MDME20pz9RveH9rEXvrOM','6M2wZ9GZgrQXHCFfjv46we','7n2wHs1TKAczGzO7Dd2rGr','6oM1PyiV3LidEUIHKubg3W',
            '2XcOYJZRPtn0BASWE7R66J','5fS7aONqrIhiw6YzgKVOsd','6TIYQ3jFPwQSRmorSezPxX','0du5cEVh5yTK9QJze8zA0C','5DSVjHy2YWufmRUHBM3PLX','6eUKZXaKkcviH0Ku9w2n3V',
            '7zMVPOJPs5jgU8NorRxqJe','6S2OmqARrzebs0tKUEyXyp','04gDigrS5kc9YWfZHwBETP','4gzpq5DPGxSnKTe4SA8HAU','66CXWjxzNUsdJxJ2JdwvnR','0C8ZW7ezQVs4URX5aX7Kqx',
            '1uNFoZAHBGtllmzznpCI3s','06HL4z0CvFAxyc27GXpf02','1hioeMAsVwJ3bvcb9lxBpB']
#artis = [raisa, glenn, afgan, hivi, jkt48, payung teduh]
#idartis1 = ['2l8I5pWUnfF7bMK1z6EJRk']
temp=1;

scope = 'user-library-read'
username = '085799202072'
client_id = '66dbab76ecc446b988fc5639f0068b93'
client_secret = '2545fe02558a4a588cf0a019c8549895'
client_uri = 'https://twitter.com/callback/'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, client_uri)
sp = spotipy.Spotify(auth=token)
database = client.recommender
collection = database.data_lagu
#with open('data_v3.csv', 'w', newline='') as csvfile:
    #fieldnames = ['popularity track', 'tempo track', 'valence track', 'release track', 'track name', 'artist name']
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
b = 0
for j, x in enumerate(idartis):
    results = sp.artist_albums(x, album_type = 'album', limit = 1)
    pop=sp.artist(x)
    for i,t in enumerate(results['items']):
        print (t['name'],'-', t['artists'][0]['name'])
        tracks = sp.album_tracks(t['uri'])
        album = sp.album(t['uri'])
        for k,s in enumerate(tracks['items']):
            pop2=sp.track(s['uri'])
            features=sp.audio_features(s['uri'])
            #print (temp, ' ',s['name'], pop2['popularity'], features[0]['tempo'], features[0]['valence'], album['release_date'][0:4])
            #writer.writerow({'popularity track': pop2['popularity'],'tempo track': features[0]['tempo'], 'valence track' : features[0]['valence'], 'release track' : int(album['release_date'][0:4]), 'track name': s['name'],'artist name': t['artists'][0]['name']})
            #temp=temp+1
            json = {
                'index': b,
                'popularity track': pop2['popularity'],
                'energy': features[0]['energy'],
                'valence' : features[0]['valence'],
                'release date' : album['release_date'][0:4],
                'track name': s['name'],
                'artist name': t['artists'][0]['name']
               }
            b = b + 1
            collection.update({'track name':s['name'],'artist name':t['artists'][0]['name']},
                               json, upsert=True)

            

