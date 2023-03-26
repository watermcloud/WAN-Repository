#Import Library yang dibutuhkan
import gradio as gr
import pandas as pd
import re

# Mengambil data abusive dan kamusalay
df_abusive = pd.read_csv("abusive.csv")
df_alay = pd.read_csv('new_kamusalay.csv',encoding='latin-1',names=['alay','normal'])

# Menentukan fungsi Pembersihan Teks 
def text_cleansing(text):
    # Replace kata abusive dengan spasi
    abusive_words = df_abusive["ABUSIVE"].tolist()
    for word in abusive_words:
        text = re.sub(r'\b{}\b'.format(word), ' ', text, flags=re.IGNORECASE)
    
    # Replace kata alay dengan kata normal
    alay_words = df_alay["alay"].tolist()
    normal_words = df_alay["normal"].tolist()
    for i in range(len(alay_words)):
        text = re.sub(r'\b{}\b'.format(alay_words[i]), normal_words[i], text, flags=re.IGNORECASE)
    
    # Membersihkan teks dengan fungsi Regex
    text = re.sub(r'http\S+', '', text) # Menghapus semua URL 
    text = re.sub(r'\B@\w+', '', text) # Menghapus semua mention (kata dengan awalan @)
    text = re.sub(r'<.*?>', '', text) # Menghapus semua tag HTML
    text = re.sub(r'[^\w\s]', '', text) # Menghapus semua karakter selain huruf, angka, dan spasi
    text = re.sub(r'\d+', '', text) # Menghapus semua angka
    text = re.sub(r'\s+', ' ', text) # Menggantikan satu atau lebih spasi berturut-turut dengan satu spasi
    text = text.strip() # Menghapus spasi di awal dan akhir teks

    return text

# Membuat Interface gradio
iface = gr.Interface(
    fn=text_cleansing, 
    inputs=gr.inputs.Textbox(label="Masukan Teks"), 
    outputs=gr.outputs.Textbox(label="Hasil Teks Yang sudah di proses"),
    title="API Pemrosesan Teks Kasar dan ALay",
    description="Dapat digunakan untuk memproses teks yang terdapat kata Kasar dan Alay",
    theme="vertical",
    layout="responsive",
    width=700,
    height=200,
    fullscreen=True,
    live=True
)

# Launch gradio interface
iface.launch()