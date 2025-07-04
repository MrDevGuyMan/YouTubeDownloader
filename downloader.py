import yt_dlp
import os
import base64


def write_cookies_from_env():
    cookies_b64 = os.environ.get("COOKIES_B64")
    if cookies_b64:
        try:
            cookies_decoded = base64.b64decode(cookies_b64).decode("utf-8")
            with open("cookies.txt", "w", encoding="utf-8") as f:
                f.write(cookies_decoded)
            print("✅ cookies.txt written from environment variable")
        except Exception as e:
            print(f"❌ Failed to decode/write cookies.txt: {e}")
    else:
        print("⚠️ No COOKIES_B64 environment variable found")


def download_video(url, format_choice):
    write_cookies_from_env()
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
    }

    if format_choice == 'mp3':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if format_choice == 'mp3':
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        return filename
