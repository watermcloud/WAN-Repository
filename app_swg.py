import re
import pandas as pd

from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

swagger_template = {
    'info': {
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    'host': LazyString(lambda: request.host),
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Mengambil data abusive dan kamusalay
df_abusive = pd.read_csv("abusive.csv")
df_alay = pd.read_csv('new_kamusalay.csv', encoding='latin-1', names=['alay', 'normal'])


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


@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    cleaned_text = text_cleansing(text) # Memanggil fungsi text_cleansing
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text, # Menggunakan cleaned_text sebagai output
    }
    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():
    # Uploaded file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df = pd.read_csv(file, encoding='latin-1')

    # Lakukan cleansing pada teks
    cleaned_texts = []
    for text in df['Tweet']:
        cleaned_texts.append(text_cleansing(text))

    df['cleaned_text'] = cleaned_texts

    response_data = df.to_dict('records')

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': response_data
    }

    return jsonify(json_response)

if __name__ == '__main__':
   app.run()
