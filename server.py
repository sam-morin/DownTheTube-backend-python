from flask import Flask, request, jsonify, send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Set the default save directory
SAVE_DIR = './downloaded-videos'

CORS_ORGIN = '*'

@app.route('/info', methods=['OPTIONS', 'POST'])
def info_video():
    # Handle preflight (OPTIONS) request
    if request.method == 'OPTIONS':
        response = app.make_response('')
        response.headers.add('Access-Control-Allow-Origin', f'{CORS_ORGIN}')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    # Handle POST request
    data = request.json
    print(data)
    youtube_url = data.get('url')

    if not youtube_url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        print(f"Downloading: {youtube_url}")
        yt = YouTube(youtube_url, on_progress_callback=on_progress)

        # Dictionary to hold itags for video and audio streams
        resolution_itags = {}
        audio_quality_itags = {}

        # Check available streams
        for stream in yt.streams:
            if stream.type == 'video' and stream.resolution:
                resolution = stream.resolution
                itag = stream.itag
                resolution_itags[resolution] = itag
            if stream.type == 'audio' and stream.abr:
                quality = stream.abr
                itag = stream.itag
                audio_quality_itags[quality] = itag
        
        print(f"Video streams: {resolution_itags.keys()}")
        print(f"Audio streams: {audio_quality_itags.keys()}")

        response = jsonify(
            {
                'message': 'Retrieved info successfully.', 
                'title': yt.title, 
                'author': yt.author, 
                'views': yt.views, 
                'length': yt.length, 
                'description': yt.description, 
                'keywords': yt.keywords, 
                'age_restricted': yt.age_restricted, 
                'publish_date': yt.publish_date, 
                'video_streams': resolution_itags, 
                'audio_streams': audio_quality_itags, 
                'thumbnail_url': yt.thumbnail_url,
                'url': youtube_url,
                'channel_url': yt.channel_url,
                'rating': yt.rating,
            }
        )
        response.headers.add('Access-Control-Allow-Origin', f'{CORS_ORGIN}')
        return response, 200

    except Exception as e:
        print(f"Error: {str(e)}")
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', f'{CORS_ORGIN}')
        return response, 500

@app.route('/download', methods=['OPTIONS', 'POST'])
def download_video():
    # Handle preflight (OPTIONS) request
    if request.method == 'OPTIONS':
        response = app.make_response('')
        response.headers.add('Access-Control-Allow-Origin', f'{CORS_ORGIN}')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    # Handle POST request
    data = request.json
    youtube_url = data.get('url')
    download_to_browser_also = data.get('download_to_browser_also', False)
    desired_resolution = data.get('desired_resolution')

    print(f"Desired resolution: {desired_resolution}")

    if not youtube_url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        print(f"Downloading: {youtube_url}")
        yt = YouTube(youtube_url, on_progress_callback=on_progress)

        # Dictionary to hold itags for video and audio streams
        resolution_itags = {}
        audio_quality_itags = {}

        # Check available streams
        for stream in yt.streams:
            if stream.type == 'video' and stream.resolution:
                resolution = stream.resolution
                itag = stream.itag
                resolution_itags[resolution] = itag
            if stream.type == 'audio' and stream.abr:
                quality = stream.abr
                itag = stream.itag
                audio_quality_itags[quality] = itag

        # Download the best available audio
        audio_itag = max(audio_quality_itags.values())

        if not desired_resolution or not audio_itag:
            return jsonify({'error': 'Required streams not found'}), 400

        # Download video
        video_stream = yt.streams.get_by_itag(desired_resolution)
        video_path = os.path.join(SAVE_DIR, 'temp_video.mp4')
        video_stream.download(output_path=SAVE_DIR, filename='temp_video.mp4')

        # Download audio
        audio_stream = yt.streams.get_by_itag(audio_itag)
        audio_path = os.path.join(SAVE_DIR, 'temp_audio.mp3')
        audio_stream.download(output_path=SAVE_DIR, filename='temp_audio.mp3')

        # Merge audio and video using FFmpeg
        merged_path = os.path.join(SAVE_DIR, f'{yt.title}.mp4')
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            merged_path
        ]
        subprocess.run(ffmpeg_cmd, check=True)

        # Clean up temporary files
        os.remove(video_path)
        os.remove(audio_path)

        if download_to_browser_also:
            return send_file(
                merged_path,
                as_attachment=True,
                download_name=f"{yt.title}.mp4",
                mimetype='video/mp4'
            )
        else:
            response = jsonify({'message': 'Video downloaded and merged successfully'})
            response.headers.add('Access-Control-Allow-Origin', f'{CORS_ORGIN}')
            return response, 200

    except Exception as e:
        print(f"Error: {str(e)}")
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', f'{CORS_ORGIN}')
        return response, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
