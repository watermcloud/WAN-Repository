from flask import Flask, jsonify, request
import re
import gradio as gr
import pandas as pd

#data abusive
df_kasar = pd.read_csv('abusive.csv')
kolom_kasar = 'ABUSIVE'

def getData():


# #kamusalay
# # Upload data CSV tanpa header
# df_alay = pd.read_csv('new_kamusalay.csv', header=None)

# # Memberikan nama kolom pada DataFrame
# df.columns = ['ALAY', 'TIDAK ALAY']

# # # # Upload data CSV dengan header
# # # df = pd.read_csv('new_kamusalay.csv', names=['ALAY', 'TIDAK ALAY'])

# #data kamusalay
# kolom_alay = 'ALAY'
# kolom_benar = 'TIDAK ALAY'

def clean_text(text):
    # pola untuk mendeteksi angka
    pola_angka = r"\d+"
    # pola untuk mendeteksi karakter-karakter khusus
    pola_karakter = r"[^\w\s]"
    # pola untuk mendeteksi spasi yang berlebihan
    pola_spasi = r"\s+"
    # pola untuk mendeteksi kata-kata kasar
    pola_kasar = r'\b(' + '|'.join(df[kolom_kasar]) + r')\b'
    # # pola untuk mendeteksi kata-kata alay
    # pola_alay = r'\b(' + '|'.join(df[kolom_alay]) + r')\b'

     # ganti angka dengan spasi
    cleaned_text = re.sub(pola_angka, " ", text)
    # ganti karakter-karakter khusus dengan spasi
    cleaned_text = re.sub(pola_karakter, " ", cleaned_text)
    # ganti spasi yang berlebihan dengan satu spasi
    cleaned_text = re.sub(pola_spasi, " ", cleaned_text)
    # hilangkan spasi di awal dan akhir teks
    cleaned_text = cleaned_text.strip()
    # ganti kata-kata kasar dengan spasi
    cleaned_text = re.sub(pola_kasar, " ", text, flags=re.IGNORECASE)
    # # ganti kata-kata alay dengan kata yang benar
    # cleaned_text = re.sub(pola_alay, " kata tidak alay ", text, flags=re.IGNORECASE)
    # return cleaned_text

app = Flask(__name__)

@app.route('/clean', methods=['POST'])
def clean():
    # ambil teks dari body request
    text = request.json['text']
    # bersihkan teks dari kata-kata kasar
    cleaned_text = clean_text(text)
    # kembalikan teks yang sudah dibersihkan dalam format JSON
    return jsonify({'cleaned_text': cleaned_text})

interface = gr.Interface(
    fn=clean_text,
    inputs=gr.inputs.Textbox(lines=5, label="Masukkan teks yang ingin dibersihkan:"),
    outputs=gr.outputs.Textbox(label="Teks yang sudah dibersihkan:"),
    title="API Cleansing Kata Kasar dan Alay -Awan"
)

if __name__ == '__main__':
    interface.launch()
