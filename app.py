from flask import Flask, request, send_file
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

key = Fernet.generate_key()
cipher = Fernet(key)

UPLOAD_FOLDER = "files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    data = file.read()
    
    encrypted_data = cipher.encrypt(data)
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as f:
        f.write(encrypted_data)
    
    return "File uploaded securely!"

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, "rb") as f:
        encrypted_data = f.read()
    
    decrypted_data = cipher.decrypt(encrypted_data)
    
    temp_path = "temp_" + filename
    with open(temp_path, "wb") as f:
        f.write(decrypted_data)
    
    return send_file(temp_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
