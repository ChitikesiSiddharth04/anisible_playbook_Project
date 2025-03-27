from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, I am Siddharth Chitikesi, Roll No: BCD21 ,this is my simple web app deployed with Ansible and Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
