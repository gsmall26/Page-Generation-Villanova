from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    image_path = 'image.png'  # Path to your image file
    return render_template('index.html', image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
