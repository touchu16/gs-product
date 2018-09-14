from flask import Flask, redirect, request, jsonify
# from keras import models
# import numpy as np
from PIL import Image
import io


app = Flask(__name__)
model = None

# ここにgoogle AutoML Model https://console.cloud.google.com/storage/browser/gga-product-vcm
# def load_model():
#     global model
#     model = models.load_model('')
#     model.summary()
#     print('Loaded the model')


@app.route('/')
def index():
    return redirect('/static/index.html')


@app.
