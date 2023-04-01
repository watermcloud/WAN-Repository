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
    text = re.sub('[^0-9a-zA-Z]+', ' ', text) # Menghapus semua karakter yang bukan angka atau huruf, lalu menggantinya dengan spasi.
    text = re.sub(r':', '', text) # Menghapus semua tanda titik dua (:).
    text = re.sub('\n',' ',text) # Mengganti karakter newline (\n) dengan spasi.
    text = re.sub('rt',' ', text) # Menghapus kata "rt".
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ', text) # Menghapus semua URL.
    text = re.sub(' +', ' ', text) # Mengganti dua atau lebih spasi berturut-turut dengan satu spasi.
    text = re.sub(r'pic.twitter.com.[\w]+', '', text) # Menghapus semua URL dari situs Twitter.
    text = re.sub('user',' ', text) # Menghapus kata "user".
    text = re.sub('gue','saya', text) # Mengganti kata "gue" dengan kata "saya".
    text = re.sub(r'‚Ä¶', '', text) # Menghapus karakter khusus yang tidak dikenali.
    text = re.sub(r'\s+', ' ', text) # Menggantikan satu atau lebih spasi berturut-turut dengan satu spasi
    text = text.strip() # Menghapus spasi di awal dan akhir teks
    text = text.lower() # Mengubah semua teks menjadi huruf kecil

    return text

# Membuat Interface gradio
iface = gr.Interface(
    fn=text_cleansing, 
    inputs=gr.inputs.Textbox(label="Masukan Teks"), 
    outputs=gr.outputs.Textbox(label="Hasil Teks Yang sudah di proses"),
    title="API Pemrosesan Teks Kasar dan ALay",
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