from flask import Flask, render_template, request, send_from_directory
from moviepy import VideoFileClip, concatenate_videoclips
import os
import string
import pymorphy2

app = Flask(__name__)
morph = pymorphy2.MorphAnalyzer()
UPLOAD_FOLDER = 'static/videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Список тематических слов
theme_words = ["действие", "действовать", "делать", "дело", "деятельность",
               "занятие", "работа", "труд", "выходной", "гулять", "домино",
               "досуг", "загар", "игра", "играть", "кукла", "бег", "бежать",
               "отдых", "отпуск", "пляж", "поход", "праздник", "прогул",
               "прогулка", "путёвка", "развлечение", "сон", "торжество", "турист"]

# Алфавит
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def create_video(text):
    videos = []
    sentence = text.lower().translate(str.maketrans('', '', string.punctuation))
    new_sent = '_'.join(sentence.split())
    words = sentence.split(" ")
    
    for word in words:
        p = morph.parse(word)[0]
        if p.normal_form in theme_words:
            video = VideoFileClip(f'Gestures/Words/{p.normal_form}.avi')
            videos.append(video)
        else:
            for char in word:
                if char in alphabet:
                    video = VideoFileClip(f'Gestures/Alphabet/{char}.avi')
                    videos.append(video)
    
    if videos:
        result = concatenate_videoclips(videos)
        output_path = os.path.join(UPLOAD_FOLDER, f"{new_sent}.mp4")
        result.write_videofile(output_path, fps=25)
        return output_path
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        video_path = create_video(text)
        if video_path:
            return render_template("index.html", video_path=video_path, text=text)
        else:
            return render_template("index.html", error="Не удалось создать видео. Проверьте ввод.")
    return render_template("index.html")

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
