#Import Library yang dibutuhkan
import gradio as gr
import pandas as pd
import re
import sqlite3

# Fungsi Cleansing

# Ubah semua ke huruf kecil
def lowercase(s):
    return s.lower()

# Hapus semua tanda baca dan kata yang tidak di perlukan
def punctuation(s):
    s = re.sub('[^0-9a-zA-Z]+', ' ', s) #menghilangkan semua karakter yang bukan huruf atau angka dan menggantinya dengan spasi.
    s = re.sub('^rt',' ', s) #menghapus awalan rt
    s = re.sub('gue','saya', s) # Mengganti kata "gue" dengan kata "saya"
    s = re.sub(r'\d+', '', s) #menghapus semua angka
    s = re.sub('user',' ', s) #menghapus kata 'user'
    s = re.sub(r':', ' ', s) #menggantikan karakter : dengan spasi
    s = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ', s) #menghapus semua URL 
    s = re.sub(' +', ' ', s) #menggantikan satu atau lebih spasi berturut-turut dengan satu spasi 
    s = re.sub('\n',' ',s) #menggantikan karakter newline (\n) dengan spasi 
    s = re.sub(r'pic.twitter.com.[\w]+', ' ', s) #menghapus semua tautan Twitter (pic.twitter.com)
    return s

# Load data abusive
db = sqlite3.connect('database_abusive.db', check_same_thread=False)
q_abusive = 'SELECT * FROM abusive'
t_abusive = pd.read_sql_query(q_abusive, db)

# Hapus data abusive
def remove_abusive_words(s):
    abusive_words = set(t_abusive['ABUSIVE'])
    words = s.split()
    filtered_words = [word for word in words if word not in abusive_words]
    return ' '.join(filtered_words)

# Load data kamus alay
db = sqlite3.connect('database_alay.db', check_same_thread = False)
q_kamusalay = 'SELECT * FROM kamusalay'
t_kamusalay = pd.read_sql_query(q_kamusalay, db)
alay_dict = dict(zip(t_kamusalay['alay'], t_kamusalay['normal']))

# Replace Kata Alay ke Kata Normal
def alay_to_normal(s):
    for word in alay_dict:
        return ' '.join([alay_dict[word] if word in alay_dict else word for word in s.split(' ')])
    
# Gabungkan Fungsi Cleansing
def cleansing(s):
    s = lowercase(s)
    s = punctuation(s)
    s = remove_abusive_words(s)
    s = alay_to_normal(s)
    return s



# Membuat Interface gradio
iface = gr.Interface(
    fn=cleansing, 
    inputs=gr.inputs.Textbox(label="Masukan Teks"), 
    outputs=gr.outputs.Textbox(label="Hasil Teks Yang sudah di proses"),
    title="API Documentation for Text Processing and Cleansing",
    description="Dapat digunakan untuk memproses teks yang terdapat kata Kasar dan Alay -dibuat oleh Awan",
    theme="vertical",
    layout="responsive",
    width=700,
    height=200,
    fullscreen=True,
    live=True
)

# Launch gradio interface
iface.launch(share=True)