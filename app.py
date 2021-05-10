from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse
from textblob import TextBlob as tb

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST': 

        link = request.form['link']
        a = urlparse(link)
        a.query
        s = a.query[2:]

        URL = "https://www.googleapis.com/youtube/v3/commentThreads"
        API_KEY = "AIzaSyB0I8Q2IStQGr9u9uml827V6oqxcS8x5Lg"
        VIDEO_ID = s

        response = requests.get(f"{URL}?key={API_KEY}&videoId={VIDEO_ID}&part=snippet")
        response_json = response.json()

        # print(response_json)

        comments = []
        komen = []
        penulis = []
        i = 0
        for item in response_json["items"]:
            if i <= 5:
                author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                content = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                # comments.append({
                #     "author": author,
                #     "content": content,
                #     "published_at": published_at
                # })
                penulis.append(author)
                komen.append(content)
                # print(f"ngambil dari: {author}")
                i += 1
            else :
                break
        
        mood = []
        for i in komen:
            sentimen = tb(i).sentiment.polarity
            if sentimen < 0:
                mood.append("Komenan jahat nih ( negatif )")
            elif sentimen == 0:
                mood.append("Komenan standar lah ( normal )")
            else :
                mood.append("Buset seneng bet ni komenan diliat liat ( positif ) ")
        # print(f"\n\n\ncomments:\n{comments}")
        # print(f"\n\n\ncomments no satu :\n{komen[0]}")
        # print(f"\n\n\nhasil blob:\n{sentimen}")
        # print(f"count comment: {len(comments)}")
        # print("finished.")
        return render_template('index.html', link = link, mood = mood, penulis = penulis, komen = komen)
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
