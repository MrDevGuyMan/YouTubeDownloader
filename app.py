from flask import Flask, render_template, request, send_file
from downloader import download_video
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        format_choice = request.form['format']
        try:
            filepath = download_video(url, format_choice)
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            return f"Error: {e}"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
