from flask import Flask, request, send_file, render_template
import cv2
import numpy as np
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_resize():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            # Baca gambar ke array numpy
            file_bytes = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            # Ambil ukuran asli
            h, w = img.shape[:2]
            new_width = 500
            ratio = new_width / w
            new_height = int(h * ratio)

            # Resize pakai OpenCV
            resized = cv2.resize(img, (new_width, new_height))

            # Encode kembali ke JPEG
            _, buffer = cv2.imencode('.jpg', resized)
            io_buf = io.BytesIO(buffer)

            return send_file(io_buf, mimetype='image/jpeg', as_attachment=True, download_name='resized.jpg')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
