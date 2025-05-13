from flask import Flask, render_template, request, send_file
import qrcode
import os
import time

app = Flask(_name_)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_created = False
    error = None
    qr_filename = None
    if request.method == 'POST':
        data = request.form.get('data')
        if not data:
            error = "Please enter some data to generate QR code."
        else:
            try:
                if not os.path.exists('static'):
                    os.makedirs('static')
                qr_filename = f"qr_code_{int(time.time())}.png"
                img = qrcode.make(data)
                img.save(os.path.join('static', qr_filename))
                qr_created = True
            except Exception as e:
                error = f"Failed to generate QR code: {str(e)}"
    return render_template('index.html', qr_created=qr_created, error=error, qr_filename=qr_filename)

@app.route('/download/<filename>')
def download_qr(filename):
    path = os.path.join("static", filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "No QR code found."

if _name_ == '_main_':
    app.run(debug=True)
