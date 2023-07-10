import io
import yt_dlp
from contextlib import redirect_stdout
from datetime import datetime
from flask import Flask, send_file, jsonify, request

app = Flask(__name__)


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data:
        res = {
            "code": 400,
            "status": "Bad Request",
            "message": "Invalid JSON Data",
        }
        return jsonify(res), 400

    if "video_url" not in data:
        res = {
            "code": 400,
            "status": "Bad Request",
            "message": "Missing required field 'video_url'"
        }
        return jsonify(res), 400

    video_url = data['video_url']

    with yt_dlp.YoutubeDL({}) as yt:
        try:
            vid_info = yt.extract_info(
                video_url,
                download=False,
            )
            message = "Search Completed."
            result = {
                "channel": vid_info['channel'] if 'channel' in vid_info else "",
                "title": vid_info['title'],
                "upload_date": datetime.strptime(vid_info['upload_date'], "%Y%m%d").strftime("%Y-%m-%d"),
                "thumbnail": vid_info['thumbnail'],
                "video_url": video_url,
                "like_count": vid_info['like_count'] if 'like_count' in vid_info else 0,
                "view_count": vid_info['view_count'] if 'view_count' in vid_info else 0
            }
            res = {
                "code": 200,
                "status": "Success",
                "message": message,
                "data": result,
            }
            return jsonify(res), 200
        except Exception as error:
            vid_info = {}
            message = f"{error}"
            res = {
                "code": 404,
                "status": "Not Found",
                "message": message,
                "data": vid_info
            }
            return jsonify(res), 404


@app.route('/download/mp4', methods=['POST'])
def download_video():
    data = request.get_json()
    if not data:
        res = {
            "code": 400,
            "status": "Bad Request",
            "message": "Invalid JSON Data",
        }
        return jsonify(res), 400

    if "video_url" not in data:
        res = {
            "code": 400,
            "status": "Bad Request",
            "message": "Missing required field 'video_url'"
        }
        return jsonify(res), 400

    video_url = data['video_url']
    ctx = {
        'outtmpl': '-',
        'logtostderr': True
    }
    buffer = io.BytesIO()
    with redirect_stdout(buffer), yt_dlp.YoutubeDL(ctx) as foo:
        foo.download([video_url])

    with yt_dlp.YoutubeDL({}) as yt:
        vid_info = yt.extract_info(
            video_url,
            download=False,
        )

    file_path = io.BytesIO(buffer.getvalue())

    return send_file(
        path_or_file=file_path,
        as_attachment=True,
        mimetype=f"{vid_info['title']}.mp4",
        download_name=f"{vid_info['title']}.mp4",
    )


@app.route('/download/mp3', methods=['POST'])
def download_audio():
    data = request.get_json()
    if not data:
        res = {
            "code": 400,
            "status": "Bad Request",
            "message": "Invalid JSON Data",
        }
        return jsonify(res), 400

    if "video_url" not in data:
        res = {
            "code": 400,
            "status": "Bad Request",
            "message": "Missing required field 'video_url'"
        }
        return jsonify(res), 400

    video_url = data['video_url']
    ctx = {
        'outtmpl': '-',
        'logtostderr': True
    }
    buffer = io.BytesIO()
    with redirect_stdout(buffer), yt_dlp.YoutubeDL(ctx) as foo:
        foo.download([video_url])

    with yt_dlp.YoutubeDL({}) as yt:
        vid_info = yt.extract_info(
            video_url,
            download=False,
        )

    file_path = io.BytesIO(buffer.getvalue())

    return send_file(
        path_or_file=file_path,
        as_attachment=True,
        mimetype=f"{vid_info['title']}.mp3",
        download_name=f"{vid_info['title']}.mp3",
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5007)
