import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import datetime as dt

df = pd.read_csv(r"songs.csv")

df.head()

# Shows the cols
df.columns

from collections import Counter

def top10_artists(data, column_name):
  count = Counter(data[column_name])
  top10 = count.most_common(10)
  return top10

artists = top10_artists(df, column_name='artist')
print("top 10 artists:")
for s, (name, count) in enumerate(artists):
  print(f'{s+1}) {name} ({count} times)')

artist_ms = df.groupby('artist')['duration_ms'].sum().sort_values(ascending=False).reset_index()

# Converts miliseconds to hours
artist_ms['duration_hours'] = (artist_ms['duration_ms'] / (1000 * 60 * 60)).round(1)

top_artists = [name for name, _ in artists]
top_artists_data = artist_ms[artist_ms['artist'].isin(top_artists)]

# Bar Graph
px.bar(top_artists_data, x='artist', y='duration_hours', color='duration_hours', hover_data=['artist', 'duration_hours'],
       color_continuous_scale='pinkyl', title='hours played per artist (top 10 only)')

def top10_genres(data, column_name):
  count = Counter(data[column_name])
  top10 = count.most_common(10)
  return top10

genres = top10_genres(df, column_name='genre')
print('top 10 genres:')
for s, (name, count) in enumerate(genres):
  print(f'{s+1}) {name} ({count} entries)')

genres_ms = df.groupby('genre')['duration_ms'].sum().sort_values(ascending=False).reset_index()
genres_ms['duration_hours'] = (genres_ms['duration_ms'] / (1000 * 60 * 60)).round(2)

top_genres = [name for name, _ in genres]
top_genres_data = genres_ms[genres_ms['genre'].isin(top_genres)]

# Pie Chart
px.pie(top_genres_data, names='genre', values='duration_hours', hole=0.4).update_traces(sort=False).update_layout(
legend_title='genre')

yearly_duration = df.groupby('year')['duration_ms'].mean().reset_index()
yearly_duration['duration_min'] = yearly_duration['duration_ms'] / (1000 * 60)

# Line graph
px.line(yearly_duration, x='year', y='duration_min', title='average song duration over the years (in minutes)')

# Scatter Plot
px.scatter(df, x='danceability', y='popularity', color='genre', title='relationship between danceability and popularity',
hover_data=['artist', 'song'])