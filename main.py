from Function import *
# from flask import Flask, request
from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources=r'/*')


# @app.route('/upload', methods=['GET', 'POST'])
# def main():
#     if request.method == 'POST':
#         print(request.files['file'])
#         file = request.files['file']
#         file.save('testset/input.wav')
#         ReadWaveFromFile('testset/input.wav')
#         return 'ok'
#     else:
#         return 'error'

def main():
    ReadWave()
    SetSize((1024, 1024))
    ImageGenerate()


if __name__ == '__main__':
    # app.run()
    main()
