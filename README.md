
<div align="center">
  <img src="./play-button-4210.svg" alt="Logo" width="220">

  <h1 align="center">DownTheTube | Backend</h1>

  [![Docker Image CI](https://github.com/sam-morin/ArcorOCR-frontend/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/sam-morin/ArcorOCR-frontend/actions/workflows/docker-image.yml)
[![Known Vulnerabilities](https://snyk.io/test/github/dwyl/hapi-auth-jwt2/badge.svg?targetFile=package.json&style=flat-square)](https://snyk.io/test/github/dwyl/hapi-auth-jwt2?targetFile=package.json)
[![Production Status](https://img.shields.io/badge/Production_Status-active-green)](https://arcorocr.com)

  <p align="center">
    <h3>A simple YouTube download web GUI | <a href="https://github.com/sam-morin/DownTheTube">Frontend Repo</a></h3>
    <a href="https://github.com/sam-morin/DownTheTube-backend-python/issues">Report Bug</a>
    ·
    <a href="https://github.com/sam-morin/DownTheTube-backend-python/issues">Request Feature</a>
    .
    <a href="#running">Build/Develop</a>
  </p>
</div>

<br/>

The Python backend for a basic YouTube viderooo downloader web GUI that runs in a docker container

### Background:
There aren't really any self-hosted YouTube video downloader web applications that I was able to find on Github. I only searched for a few minutes though, so I'm sure there are some out there, maybe.

## Objectives:
- Query: 
    Query a video via a YouTube URL and return information about the video.
- Download:
    Download a video to either the server or the server and the browser. Allow choosing the quality.


## Implemented:
- Query:
    Query a video via a YouTube URL and return information about the video.
- Download:
    Download a video to either the server or the server and the browser. Allows for choosing the quality.
    None of the available stream resolutions were progressive except for 360p. Bummer.
    1. Download video stream at the requested resolution
    2. Download the highest quality audio stream
    3. Stitch these friends together using ffmpeg
    4. Leave the video on the server in the `./downloaded-videos` folder
    5. Pass it back to the browser if requested

# Running

## For anything other than development, you'd probably be better off using Docker Compose
<a href="https://github.com/sam-morin/DownTheTube-docker-compose">Go to DownTheTube Docker Compose repo</a>


### Production

1. Clone the source and CD
```shell
git clone https://github.com/sam-morin/DownTheTub-backend-python.git && cd DownTheTub-backend-python
```

2. Build image
```shell
docker build . -t downthetube-backend
```

3. Run the image
```shell
docker run -d --restart unless-stopped -p SOME_PUBLIC_PORT:5001 -v $(pwd)/server/downloaded-videos:/app/downloaded-videos downthetube-backend
```

### Development

1. Clone the source and CD
```shell
git clone https://github.com/sam-morin/DownTheTube-backend-python.git && cd DownTheTube-backend-python
```

2. Install required pip modules
```shell
pip install -r requirements.txt
```

3. Run the server using Flask
```shell
python server.py
```