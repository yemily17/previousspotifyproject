import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SPOTIPY_CLIENT_ID='197fbae33fa44ece97dd99538005f422'
SPOTIPY_CLIENT_SECRET='bc8ae1d1be014c38b25f5cba5c41e98d'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:9090/'
SCOPE = "user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))
results = sp.current_user_top_tracks()
top_tracks_alltime = sp.current_user_top_tracks(limit=50, offset=0, time_range="long_term")
def get_track_ids(time_frame):
 track_ids = []
 for song in time_frame['items']:
    track_ids.append(song['id'])
 return track_ids
track_ids = get_track_ids(top_tracks_alltime)
acousticness=[]
danceability=[]
energy=[]
instrumentalness=[]
valence=[]

for i in range(0,len(track_ids)-1):
    track_features=sp.audio_features(track_ids[i])
    acousticness.append(track_features[0].get("acousticness"))
    danceability.append(track_features[0].get("danceability"))
    energy.append(track_features[0].get("energy"))
    instrumentalness.append(track_features[0].get("instrumentalness"))
    valence.append(track_features[0].get("valence"))
# print(acousticness)

labels="Acousticness", "Danceability", "Energy", "Instrumentalness", "Valence"
stats=np.mean(acousticness), np.mean(danceability), np.mean(energy), np.mean(instrumentalness), np.mean(valence)
angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

# close the plot
stats=np.concatenate((stats,[stats[0]]))
angles=np.concatenate((angles,[angles[0]]))

#Size of the figure
fig=plt.figure(figsize = (18,18))

ax = fig.add_subplot(221, polar=True)
ax.plot(angles, stats, 'o-', linewidth=2, label = "Features", color= 'gray')
ax.fill(angles, stats, alpha=0.25, facecolor='gray')
ax.set_thetagrids(angles[0:5] * 180/np.pi, labels , fontsize = 13)


ax.set_rlabel_position(250)
plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
plt.ylim(0,1)

plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

plt.show()