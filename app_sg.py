import re
import sqlite3
import pandas as pd

from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

#Template Interface Swagger
swagger_template = {
    'info': {
        'title': LazyString(lambda: 'API Documentation for Text Processing and Cleansing'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Teks Processing dan Cleansing'),
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

# Endpoint landing page
@swag_from("docs/landingpage.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'status_code': 200,
        'description': "DSC 7 - API Text Processing & Cleansing",
        'data': "HERMAWAN",
    }

    response_data = jsonify(json_response)
    return response_data

# Endpoint Text Processing
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    cleaned_text = cleansing(text) # Memanggil fungsi text_cleansing
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text, # Menggunakan cleaned_text sebagai output
    }
    response_data = jsonify(json_response)
    return response_data

# Endpoint Text Processing File
@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    # Upladed file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df = pd.read_csv(file, encoding='latin-1')

    # Ambil teks yang akan diproses dalam format list
    # texts = df.text.to_list()

    # Lakukan cleansing pada teks
    cleaned_text = []
    for text in df['Tweet']:
        cleaned_text.append(cleansing(text))

    df['cleaned_text'] = cleaned_text

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text
    }

    response_data = jsonify(json_response)
    return response_data


if __name__ == '__main__':
   app.run()