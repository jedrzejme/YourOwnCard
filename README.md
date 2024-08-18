<h1 align = 'center'>
    <img 
        src = '/assets/icon.png' 
        height = '200' 
        width = '200' 
        alt = 'Icon' 
    />
    <br>
    Your Own Card
    <br>
</h1>

<div align = 'center'>
    <a href = 'https://github.com/jedrzejme/YourOwnCard/'>
        <img src = 'https://img.shields.io/github/stars/jedrzejme/YourOwnCard?style=for-the-badge&color=%23cfb002'/>
    </a>
    <a href = 'https://github.com/jedrzejme/YourOwnCard/tags'>
        <img src = 'https://img.shields.io/github/v/tag/jedrzejme/YourOwnCard?style=for-the-badge&label=version'/>
    </a>
    <a href = 'https://github.com/jedrzejme/YourOwnCard/issues'>
        <img src = 'https://img.shields.io/github/issues/jedrzejme/YourOwnCard?style=for-the-badge&color=%23ff6f00'/>
    </a>
    <a href = 'https://github.com/jedrzejme/YourOwnCard/pulls'>
        <img src = 'https://img.shields.io/github/issues-pr/jedrzejme/YourOwnCard?style=for-the-badge'/>
    </a>
</div>

<br>

**❓ What is this?** Web app for creating your own card. Backend is written in Flask (Python framework).

**❓ How to use it?**
* [**Using version hosted by me**](https://your-own-card.jbs.ovh)
* [**Using docker-compose**](#using-docker-compose-to-run-your-own-card)
* [**Using Python**](#using-python-to-run-your-own-card)

**❓ What did I use?**
* [Python](https://www.python.org/)
* [Python libraries](/requirements.txt)
* [Docker](https://www.docker.com/)
* [Coding](https://code.visualstudio.com/)
* [Git management](https://desktop.github.com/)

## 📷 Preview of example profile
[![](/assets/preview.png)](https://your-own-card.jbs.ovh/profile/jedrzej)

## 🐳 Using docker-compose to run Your Own Card
1) Install Docker, docker-compose and Git
2) Clone this repository and enter its directory:
```
git clone https://github.com/jedrzejme/YourOwnCard.git
```
3) Edit config.ini (do not change port in config.ini; if you want to change external port change it in docker-compose.yml)
4) Create docker image:
```
docker build -t your-own-card .
```
5) Run docker-compose (by default it will run on port 5000):
```
docker-compose up -d
```
6) It works!

## 🐍 Using Python to run Your Own Card
1) Install Python
2) Clone this repository and enter its directory:
```
git clone https://github.com/jedrzejme/YourOwnCard.git
```
3) Install requirements.txt:
```
python -m pip install -r requirements.txt
```
4) Edit config.ini
5) Run app.py (by default it will run on port 5000):
```
python app.py
```
6) It works!

## 🚀 Features
* Creating your own card
* Editing your own card with password protection
* Option to disable editing after creation in config.ini
* Option to disable creating new profiles in config.ini
* Option to set different port in config.ini
* Option to set app name in config.ini
* Option to change colors in config.ini

## 🚀 Supported social medias
* Your website
* Instagram
* Facebook
* X
* GitHub
* LinkedIn
* Discord
* Steam

## ❓ Purpose
Simpler and free alternative to popular, similar web apps

## 💲 Support
<p><a href="https://support.jedrzej.me/" target="_blank"> <img align="left" src="https://raw.githubusercontent.com/jedrzejme/jedrzejme/main/assets/supportme.svg" height="50" width="210" alt="jedrzejme" /></a></p>