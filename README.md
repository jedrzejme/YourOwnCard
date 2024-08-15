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

**What is this?** Web app for creating your own card. Backend is written in Flask (Python framework).

**How to use it?**
* [**Using version hosted by me**](https://your-own-card.jbs.ovh)
* [**Using docker-compose**](https://github.com/jedrzejme/DynamicDNSUsingCloudflare/#using-docker-compose-to-run-your-own-card)

**What did I use?**
* [Python](https://www.python.org/)
* [Python libraries](/requirements.txt)
* [Docker](https://www.docker.com/)
* [Coding](https://code.visualstudio.com/)
* [Git management](https://desktop.github.com/)

## Using docker-compose to run Your Own Card
1) Install docker and docker-compose

2) Create new directory called however you want and enter it

3) Clone this repository:
```
git clone https://github.com/jedrzejme/YourOwnCard.git
```

4) Create docker image:
```
docker build -t your-own-card .
```

5) Edit config.ini

6) Run docker-compose in the same directory (by default it will run on port 5000):
```
docker-compose up -d
```
7) It works!

## Features
* Creating your own card
* Editing your own card with secret phrase protection provided by email
* Option to disable editing after creation
* Option to disable creating new profiles

## Purpose
Simpler and free alternative to popular, similar web apps

## Support
<p><a href="https://support.jedrzej.me/" target="_blank"> <img align="left" src="https://raw.githubusercontent.com/jedrzejme/jedrzejme/main/assets/supportme.svg" height="50" width="210" alt="jedrzejme" /></a></p>