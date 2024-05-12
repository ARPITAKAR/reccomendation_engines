from flask import Flask, request, render_template, url_for
import pickle

app = Flask(__name__)

# Load data
df = pickle.load(open('saregama.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommendation(song_df):
    idx = df[df['song'] == song_df].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    
    songs = []
    for m_id in distances[1:6]:
        songs.append(df.iloc[m_id[0]].song)
        
    return songs

@app.route('/', methods=['GET'])
def index():
    names = list(df['song'].values)
    return render_template('index.html', names=names)

@app.route('/recom', methods=['POST'])
def recommendation():
    user_song = request.form['names']
    songs = recommendation(user_song)
    return render_template('recommendation.html', songs=songs)

if __name__ == '__main__':
    app.run(debug=True)
