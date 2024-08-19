from flask import Flask, request, jsonify
from deepface import DeepFace
import numpy as np
import cv2
import tempfile
import json
import logging
import os

DB_PATH = 'data_db'
BACKENDS = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe','yolov8','yunet','fastmtcnn']

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/deepface/find', methods=['POST'])
def process():
    logger.debug('process...... ')

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        byte_array = file.read()

        # Convert byte array to numpy array
        nparr = np.frombuffer(byte_array, np.uint8)
        
        # Decode image from numpy array
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_filename = temp_file.name
            cv2.imwrite(temp_filename, img)

        # Perform face recognition using DeepFace
        res , result = indentify(temp_filename)
        logger.debug('result %s', result)

        # Cleanup: remove the temporary file
        os.remove(temp_filename)
        
        if result:
            name = res['identity'].split('\\')[1]
            distance = res['distance']
            logger.debug('indentify %s', name)

            # Process the byte array as needed
            return jsonify({"pid": name, "distance": distance}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def indentify(img):
    try :
        dfs = DeepFace.find(img_path = img, 
            db_path = DB_PATH,
            enforce_detection = False,
            detector_backend = BACKENDS[1],
            model_name='Facenet512',
            silent = True
        )
        logger.debug(dfs)
        logger.debug('---------------')
        if len(dfs[0]['identity']) >=1:
            return dfs[0].iloc[0],True
        else :
            return '',False
    except :
        return '',False

# main driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
