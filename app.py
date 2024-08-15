from flask import Flask, render_template, request, abort, redirect, url_for, flash, send_from_directory
import os
import requests
import secrets
import string
import json
from configparser import ConfigParser
config = ConfigParser()

def create_directory_if_it_doesnt_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

create_directory_if_it_doesnt_exist("protected/profiles")
create_directory_if_it_doesnt_exist("static/profiles")

app = Flask(__name__, static_url_path='/static')
app.config['PROFILES_PICSTURES_FOLDER'] = 'static/profiles/'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
PROTECTED_DIR = '/protected'

config.read('config.ini')

app_name = config.get('main', 'app_name')
default_background_color = f"#{config.get('main', 'default_background_color')}"
default_container_color = f"#{config.get('main', 'default_container_color')}"
default_button_color = f"#{config.get('main', 'default_button_color')}"
default_button_hover_color = f"#{config.get('main', 'default_button_hover_color')}"
default_text_color = f"#{config.get('main', 'default_text_color')}"
default_footer_color = f"#{config.get('main', 'default_footer_color')}"
enable_creation_of_new_profiles = config.getboolean('main', 'enable_creation_of_new_profiles')
enable_editing_after_creation = config.getboolean('main', 'enable_editing_after_creation')
mailgun_api_key = config.get('main', 'mailgun_api_key')

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_profile(file_path):
    profile = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                profile[key.strip()] = value.strip()
    return profile

def generate_secret_phrase(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def send_secret_phrase(email, display_name, username, secret_phrase):
    url = "https://api.mailgun.net/v3/sandboxc97bb77629c84370a545633d3715f229.mailgun.org/messages"
    
    mailgun_vars = json.dumps({
        "username": username,
        "secret_phrase": secret_phrase
    })
    
    response = requests.post(
        url,
        auth=("api", f"{mailgun_api_key}"),
        data={
            "from": "Mailgun Sandbox <postmaster@sandboxc97bb77629c84370a545633d3715f229.mailgun.org>",
            "to": f"{display_name} <{email}>",
            "subject": "Your Secret Phrase for Card.io",
            "template": "secret phrase",
            "h:X-Mailgun-Variables": mailgun_vars
        }
    )
    
    return response

def create_profile(username, email, display_name, background_color, container_color, button_color, button_hover_color, text_color, about_me, www, www_name, instagram, instagram_name, facebook, facebook_name, x, x_name, github, github_name linkedin, linkedin_name, discord, steam, steam_name, profile_picture_path):
    secret_phrase = generate_secret_phrase()
    background_color = background_color or default_background_color
    container_color = container_color or default_container_color
    button_color = button_color or default_button_color
    button_hover_color = button_hover_color or default_button_hover_color
    text_color = text_color or default_text_color
    footer_color = default_footer_color
    profile_picture_path = profile_picture_path or "default.jpg"
    www_name = www_name or www.rstrip('/').split('/')[-1]
    instagram_name = instagram_name or instagram.rstrip('/').split('/')[-1]
    facebook_name = facebook_name or facebook.rstrip('/').split('/')[-1]
    x_name = x_name or x.rstrip('/').split('/')[-1]
    github_name = github_name or github.rstrip('/').split('/')[-1]
    linkedin_name = linkedin_name or "LinkedIn"
    steam_name = steam_name or steam.rstrip('/').split('/')[-1]
    profile_file = open(f"protected/profiles/{username}.txt", "w")
    profile_file.write(f"email = {email}\nusername = {username}\ndisplay_name = {display_name}\nbackground_color = {background_color}\ncontainer_color = {container_color}\nbutton_color = {button_color}\nbutton_hover_color = {button_hover_color}\ntext_color = {text_color}\nfooter_color = {footer_color}\nabout_me = {about_me}\nwww = {www}\nwww_name = {www_name}\ninstagram_name = {instagram_name}\ninstagram = {instagram}\nfacebook_name = {facebook_name}\nfacebook = {facebook}\nx_name = {x_name}\nx = {x}\ngithub_name = {github_name}\ngithub = {github}\nlinkedin_name = {linkedin_name}\nlinkedin = {linkedin}\ndiscord = {discord}\nsteam_name = {steam_name}\nsteam = {steam}\nprofile_picture_path = {profile_picture_path}\nsecret_phrase = {secret_phrase}")
    profile_file.close()
    send_secret_phrase(email, display_name, username, secret_phrase)

def create_profile_with_picture():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        display_name = request.form.get("display-name")
        background_color = request.form.get("background-color")
        container_color = request.form.get("container-color")
        button_color = request.form.get("button-color")
        button_hover_color = request.form.get("button-hover-color")
        text_color = request.form.get("text-color")
        about_me = request.form.get("about-me")
        www_name = request.form.get("www-name")
        www = request.form.get("www")
        instagram_name = request.form.get("instagram-name")
        instagram = request.form.get("instagram")
        facebook_name = request.form.get("facebook-name")
        facebook = request.form.get("facebook")
        linkedin_name = request.form.get("linkedin-name")
        linkedin = request.form.get("linkedin")
        discord = request.form.get("discord")
        steam_name = request.form.get("steam-name")
        steam = request.form.get("steam")
        x = request.form.get("x")
        x_name = request.form.get("x-name")
        github = request.form.get("github")
        github_name = request.form.get("github-name")

        profile_picture_path = "default.jpg"

        if 'profile-picture' in request.files:
            file = request.files['profile-picture']
            if allowed_file(file.filename):
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                file.seek(0)
                
                if file_length > app.config['MAX_CONTENT_LENGTH']:
                    return redirect(request.url)
                
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                profile_picture_path = os.path.join(app.config['PROFILES_PICSTURES_FOLDER'], f"{username}.{file_extension}")
                file.save(profile_picture_path)
                profile_picture_path = f"{username}.{file_extension}"
            else:
                return redirect(request.url)
        else:
            return redirect(request.url)

        create_profile(username, email, display_name, background_color, container_color, button_color, button_hover_color, text_color, about_me, www, www_name, instagram, instagram_name, facebook, facebook_name, x, x_name, github, github_name, linkedin, linkedin_name, discord, steam, steam_name, profile_picture_path)
        
        return redirect(f"/profile/{username}")
    
    return redirect(url_for('create_your_own'))

@app.route('/protected/<filename>')
def protected_file(filename):
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(PROTECTED_DIR, safe_filename)
    
    if os.path.isfile(file_path):
        return send_from_directory(PROTECTED_DIR, safe_filename)
    else:
        abort(404)

@app.route('/')
def index():
    return render_template('index.html', app_name = app_name, enable_creation_of_new_profiles=enable_creation_of_new_profiles, enable_editing_after_creation=enable_editing_after_creation)

@app.route('/create-profile', methods=['GET', 'POST'])
def create_your_own():
    if enable_creation_of_new_profiles:
        return render_template('create-profile.html')

@app.route('/submit-creation-of-profile', methods=['GET', 'POST'])
def submit_creation_of_profile():
    if enable_creation_of_new_profiles:
        username = request.form.get("username")
        if not os.path.exists(f"protected/profiles/{username}.txt"):
            create_profile_with_picture()
        else:
            return redirect("/create-profile")
        return redirect(f"/profile/{username}")

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if enable_editing_after_creation:
        return render_template('edit-profile.html')

@app.route('/submit-edition-of-profile', methods=['GET', 'POST'])
def submit_edition_of_profile():
    if enable_editing_after_creation:
        username = request.form.get("username")
        secret_phrase_input = request.form.get("secret-phrase")
        if not os.path.exists(f"protected/profiles/{username}.txt"):
            create_profile_with_picture()
        else:
            profile = load_profile(f"protected/profiles/{username}.txt")
            if profile["secret_phrase"] == secret_phrase_input:
                create_profile_with_picture()
            else:
                return redirect("/edit-profile")
        return redirect(f"/profile/{username}")

@app.route('/profile/<username>')
def profile(username):
    profile = load_profile(f"protected/profiles/{username}.txt")
    return render_template("profile.html",
                        app_name = app_name,
                        **profile)

@app.route('/support')
def support():
    return render_template('support.html')

if __name__ == '__main__':
    app.run(host="localhost", port=5000)