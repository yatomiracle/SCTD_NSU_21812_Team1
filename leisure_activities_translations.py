from string import punctuation
from moviepy.editor import (VideoFileClip, TextClip,
                            CompositeVideoClip, concatenate_videoclips)
import threading
import sys
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def create_video(text):
    videos = []
    total_dur = 0
    sentence = text.lower().translate(str.maketrans('', '', punctuation))
    new_sent = '_'.join(sentence.split())
    words = sentence.split(" ")
    theme_words = ["действие", "действовать", "делать", "дело", "деятельность",
                   "занятие", "работа", "труд", "выходной",
                   "гулять", "домино", "досуг", "загар", "игра", "играть",
                   "кукла", "бег", "бежать", "отдых", "отпуск", "пляж",
                   "поход", "праздник", "прогул", "прогулка", "путёвка",
                   "развлечение", "сон", "торжество", "турист"]
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    for word in words:
      p = morph.parse(word)[0]
      if p.normal_form in theme_words:
        video = VideoFileClip('/content/drive/MyDrive/Жесты_ПиРСКС/Слова/'+p.normal_form+'.avi')
        total_dur += video.duration
        txt_clip = (TextClip(word, fontsize=45, color='white')
                                .set_position('center')
                                .set_duration(video.duration))
        videos.append(CompositeVideoClip([video, txt_clip]))
      else:
        for i in word:
            print(i)
            if i in alphabet:
                video = VideoFileClip('/content/drive/MyDrive/Жесты_ПиРСКС/Алфавит/'+i+'.avi')
                total_dur += video.duration
                txt_clip = (TextClip(i.upper(), font='Montserrat', fontsize=70, color='white')
                                .set_position('center')
                                .set_duration(video.duration))
                videos.append(CompositeVideoClip([video, txt_clip]))
    try:
        video = concatenate_videoclips(videos)
        txt_clip = (TextClip(text, font='Montserrat', method='caption', color='white', size=(video.size[0], video.size[1]/5))
                    .set_position('bottom')
                    .set_duration(total_dur))
        result = CompositeVideoClip([video, txt_clip])
        result.write_videofile(f"{new_sent}.mp4", fps=25)
    except ValueError:
        print("Пустое слово")

create_video('На выходных поедем на пляж загорать по путевке.')
