from flask import Flask, render_template, request, abort, redirect, url_for, flash, send_from_directory
import os
import requests
import secrets
import random
import string
import json
import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
msg = MIMEMultipart()
from email.mime.text import MIMEText
from configparser import ConfigParser
config = ConfigParser()

def create_directory_if_it_doesnt_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

create_directory_if_it_doesnt_exist("protected/profiles")
create_directory_if_it_doesnt_exist("protected/tokens")
create_directory_if_it_doesnt_exist("static/profiles")

app = Flask(__name__, static_url_path='/static')
app.config['PROFILES_PICSTURES_FOLDER'] = 'static/profiles/'
max_content_length = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
PROTECTED_DIR = '/protected'

config.read('config.ini')

app_name = config.get('main', 'app_name')
app_url = config.get('main', 'app_url')
port = config.getint('main', 'port')
debug = config.getboolean('main', 'debug')
enable_creation_of_new_profiles = config.getboolean('main', 'enable_creation_of_new_profiles')
enable_editing_after_creation = config.getboolean('main', 'enable_editing_after_creation')
enable_password_resetting = config.getboolean('main', 'enable_password_resetting')

default_background_color = f"#{config.get('colors', 'default_background_color')}"
default_container_color = f"#{config.get('colors', 'default_container_color')}"
default_button_color = f"#{config.get('colors', 'default_button_color')}"
default_button_hover_color = f"#{config.get('colors', 'default_button_hover_color')}"
default_button_text_color = f"#{config.get('colors', 'default_button_text_color')}"
default_input_color = f"#{config.get('colors', 'default_input_color')}"
default_text_color = f"#{config.get('colors', 'default_text_color')}"
default_footer_color = f"#{config.get('colors', 'default_footer_color')}"

smtp_server = config.get('smtp', 'server')
smtp_port = config.getint('smtp', 'port')
smtp_username = config.get('smtp', 'username')
msg['From'] = smtp_username
smtp_password = config.get('smtp', 'password')

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class CustomError(Exception):
    def __init__(self, code, message, previous_page):
        self.code = code
        self.message = message
        self.previous_page = previous_page

@app.errorhandler(CustomError)
def handle_custom_error(error):
    return render_template('error.html', code=error.code, message=error.message, previous_page=error.previous_page, default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color), error.code

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=404, message="Page not found.", previous_page="/", default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color), 404

def load_profile(file_path):
    profile = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                profile[key.strip()] = value.strip()
    return profile

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def sending_email(email, subject, message):
    try:
        # Create a new MIMEMultipart message for each email
        msg = MIMEMultipart()
        msg['From'] = f"{app_name} <{smtp_username}>"
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))

        # Establish connection to the SMTP server and send email
        print(f"Connecting to the server {smtp_server} on port {smtp_port}...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    except Exception as e:
        raise CustomError(500, "An error occurred while sending the email.", "/")

def reset_password(username):
    if os.path.exists(f"protected/profiles/{username}.txt"):
        profile = load_profile(f"protected/profiles/{username}.txt")
        email = profile["email"]
        subject = "Password reset"
        token = f"{''.join(random.choices(string.ascii_letters + string.digits, k=32))}"
        message = render_template('reset-password-email.html', app_name = app_name, app_url = app_url, token=token, username=username)
        sending_email(email, subject, message)
        token_file = open(f"protected/tokens/{username}.txt", "w")
        token_file.write(token)
        token_file.close()
    else:
        raise CustomError(404, "User not found.", "/reset-password")

def create_profile(editing, email, username, password, display_name, background_color, container_color, button_color, button_hover_color, button_text_color, text_color, footer_color, about_me, www, www_name, instagram, instagram_name, facebook, facebook_name, x, x_name, github, github_name, linkedin, linkedin_name, discord, steam, steam_name, profile_picture_path):
    password = password
    if not editing:
        hashed_password = hash_password(password)
    else:
        hashed_password = password
    background_color = background_color or default_background_color
    container_color = container_color or default_container_color
    button_color = button_color or default_button_color
    button_hover_color = button_hover_color or default_button_hover_color
    button_text_color = button_text_color or default_button_text_color
    text_color = text_color or default_text_color
    footer_color = footer_color or default_footer_color
    profile_picture_path = profile_picture_path
    www_name = www_name or www.rstrip('/').split('/')[-1]
    instagram_name = instagram_name or instagram.rstrip('/').split('/')[-1]
    facebook_name = facebook_name or facebook.rstrip('/').split('/')[-1]
    x_name = x_name or x.rstrip('/').split('/')[-1]
    github_name = github_name or github.rstrip('/').split('/')[-1]
    steam_name = steam_name or steam.rstrip('/').split('/')[-1]
    profile_file = open(f"protected/profiles/{username}.txt", "w")
    profile_file.write(f"""email = {email}\nusername = {username}\nhashed_password = {hashed_password}\ndisplay_name = {display_name}\nbackground_color = {background_color}\ncontainer_color = {container_color}\nbutton_color = {button_color}\nbutton_hover_color = {button_hover_color}\nbutton_text_color = {button_text_color}\ntext_color = {text_color}\nfooter_color = {footer_color}\nabout_me = {about_me}\nwww = {www}\nwww_name = {www_name}\ninstagram_name = {instagram_name}\ninstagram = {instagram}\nfacebook_name = {facebook_name}\nfacebook = {facebook}\nx_name = {x_name}\nx = {x}\ngithub_name = {github_name}\ngithub = {github}\nlinkedin_name = {linkedin_name}\nlinkedin = {linkedin}\ndiscord = {discord}\nsteam_name = {steam_name}\nsteam = {steam}\nprofile_picture_path = {profile_picture_path}""")
    profile_file.close()

def create_profile_with_picture(editing, email, username, password, display_name, profile_picture, background_color, container_color, button_color, button_hover_color, button_text_color, text_color, footer_color, about_me, www, www_name, instagram, instagram_name, facebook, facebook_name, x, x_name, github, github_name, linkedin, linkedin_name, discord, steam, steam_name):
    if request.method == "POST":
        display_name = request.form.get("display-name")
        background_color = request.form.get("background-color")
        container_color = request.form.get("container-color")
        button_color = request.form.get("button-color")
        button_hover_color = request.form.get("button-hover-color")
        button_text_color = request.form.get("button-text-color")
        text_color = request.form.get("text-color")
        footer_color = request.form.get("footer-color")
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

        if profile_picture:
            if 'profile-picture' in request.files:
                file = profile_picture
                if allowed_file(file.filename):
                    file.seek(0, os.SEEK_END)
                    file_length = file.tell()
                    file.seek(0)
                    
                    if file_length > max_content_length:
                        raise CustomError(413, "File is too large. Please upload a file smaller than 5MB.", "/create-profile")
                    
                    file_extension = file.filename.rsplit('.', 1)[1].lower()
                    profile_picture_path = os.path.join(app.config['PROFILES_PICSTURES_FOLDER'], f"{username}.{file_extension}")
                    file.save(profile_picture_path)
                    profile_picture_path = f"{username}.{file_extension}"
                else:
                    raise CustomError(400, "File extension not allowed. Please upload a .png, .jpg or .jpeg file.", "/create-profile")
            else:
                return redirect(request.url)
        elif not profile_picture and editing:
            profile_picture_path = load_profile(f"protected/profiles/{username}.txt")["profile_picture_path"]
        elif not profile_picture and not editing:
            profile_picture_path = "default.png"
        create_profile(editing, email, username, password, display_name, background_color, container_color, button_color, button_hover_color, button_text_color, text_color, footer_color, about_me, www, www_name, instagram, instagram_name, facebook, facebook_name, x, x_name, github, github_name, linkedin, linkedin_name, discord, steam, steam_name, profile_picture_path)

@app.route('/')
def index():
    return render_template('index.html', app_name = app_name, default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color, enable_creation_of_new_profiles=enable_creation_of_new_profiles, enable_editing_after_creation=enable_editing_after_creation)

@app.route('/create-profile', methods=['GET', 'POST'])
def create_your_own():
    if enable_creation_of_new_profiles:
        return render_template('create-profile.html', default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color, enable_editing_after_creation=enable_editing_after_creation)

@app.route('/submit-creation-of-profile', methods=['GET', 'POST'])
def submit_creation_of_profile():
    if enable_creation_of_new_profiles:
        username = request.form.get("username")
        if not os.path.exists(f"protected/profiles/{username}.txt") and not username == "default":
            editing = False
            profile_picture = request.files['profile-picture']
            email = request.form.get("email")
            username = request.form.get("username")
            password = request.form.get("""password""")
            display_name = request.form.get("display-name")
            background_color = request.form.get("background-color")
            container_color = request.form.get("container-color")
            button_color = request.form.get("button-color")
            button_hover_color = request.form.get("button-hover-color")
            button_text_color = request.form.get("button-text-color")
            text_color = request.form.get("text-color")
            footer_color = request.form.get("footer-color")
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
            create_profile_with_picture(editing = editing, email=email, username=username, password=password, display_name=display_name, profile_picture=profile_picture, background_color=background_color, container_color=container_color, button_color=button_color, button_hover_color=button_hover_color, button_text_color=button_text_color, text_color=text_color, footer_color=footer_color, about_me=about_me, www=www, www_name=www_name, instagram=instagram, instagram_name=instagram_name, facebook=facebook, facebook_name=facebook_name, x=x, x_name=x_name, github=github, github_name=github_name, linkedin=linkedin, linkedin_name=linkedin_name, discord=discord, steam=steam, steam_name=steam_name)
            return redirect(f"/profile/{username}")
        else:
            raise CustomError(403, "Username already exists.", "/create-profile")
    else:
        raise CustomError(403, "Creation of new profiles is disabled.", "/")

@app.route('/login', methods=['GET', 'POST'])
def edit_profile_auth():
    if enable_editing_after_creation:
        return render_template('login.html', enable_password_resetting = enable_password_resetting, default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color)
    else:
        raise CustomError(403, "Editing of profiles is disabled.", "/")

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    username = request.form.get("username")
    password = request.form.get("""password""")
    if not os.path.exists(f"protected/profiles/{username}.txt"):
        raise CustomError(404, "Profile not found.", "/login")
    profile = load_profile(f"protected/profiles/{username}.txt")
    hashed_password = hash_password(password)
    if profile["""hashed_password"""] == hashed_password:
        return render_template('edit-profile.html', password = hashed_password, default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color, email=profile["email"], username=username, display_name=profile["display_name"], background_color=profile["background_color"], container_color=profile["container_color"], button_color=profile["button_color"], button_hover_color=profile["button_hover_color"], button_text_color=profile["button_text_color"], text_color=profile["text_color"], footer_color=profile["footer_color"], about_me=profile["about_me"], www=profile["www"], www_name=profile["www_name"], instagram=profile["instagram"], instagram_name=profile["instagram_name"], facebook=profile["facebook"], facebook_name=profile["facebook_name"], x=profile["x"], x_name=profile["x_name"], github=profile["github"], github_name=profile["github_name"], linkedin=profile["linkedin"], linkedin_name=profile["linkedin_name"], discord=profile["discord"], steam=profile["steam"], steam_name=profile["steam_name"])
    else:
        raise CustomError(401, "Wrong password.", "/login")

@app.route("""/submit-edition-of-profile/<username>/<password>""", methods=['GET', 'POST'])
def submit_edition_of_profile(username, password):
    if enable_editing_after_creation:
        editing = True
        profile_picture = request.files['profile-picture']
        email = load_profile(f"protected/profiles/{username}.txt")["email"]
        display_name = request.form.get("display-name")
        background_color = request.form.get("background-color")
        container_color = request.form.get("container-color")
        button_color = request.form.get("button-color")
        button_hover_color = request.form.get("button-hover-color")
        button_text_color = request.form.get("button-text-color")
        text_color = request.form.get("text-color")
        footer_color = request.form.get("footer-color")
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
        if profile_picture:
            if 'profile-picture' in request.files:
                file = profile_picture
                if allowed_file(file.filename):
                    file.seek(0, os.SEEK_END)
                    file_length = file.tell()
                    file.seek(0)
                    
                    if file_length > max_content_length:
                        raise CustomError(413, "File is too large. Please upload a file smaller than 5MB.", "/login")
                else:
                    raise CustomError(400, "File extension not allowed. Please upload a .png, .jpg or .jpeg file.", "/login")
            else:
                return redirect(request.url)
        create_profile_with_picture(editing = editing, email=email, username=username, password=password, display_name=display_name, profile_picture=profile_picture, background_color=background_color, container_color=container_color, button_color=button_color, button_hover_color=button_hover_color, button_text_color=button_text_color, text_color=text_color, footer_color=footer_color, about_me=about_me, www=www, www_name=www_name, instagram=instagram, instagram_name=instagram_name, facebook=facebook, facebook_name=facebook_name, x=x, x_name=x_name, github=github, github_name=github_name, linkedin=linkedin, linkedin_name=linkedin_name, discord=discord, steam=steam, steam_name=steam_name)
        return redirect(f"/profile/{username}")
    else:
        raise CustomError(403, "Editing of profiles is disabled.", "/")

@app.route("/reset-password", methods=['GET', 'POST'])
def reset_password_page():
    if enable_password_resetting:
        if request.method == "POST":
            username = request.form.get("username")
            reset_password(username)
            return render_template('reset-password.html', success = True, default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color)
        return render_template('reset-password.html', default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color)
    else:
        raise CustomError(403, "Password resetting is disabled.", "/")

@app.route("/reset-password/<username>/<token>", methods=['GET', 'POST'])
def reseting_password(username, token):
    if enable_password_resetting:
        if not os.path.exists(f"protected/tokens/{username}.txt"):
            raise CustomError(500, "Something went wrong.", "/")
        with open(f"protected/tokens/{username}.txt", 'r') as file:
            token_from_file = file.read()
        if token == token_from_file:
            if request.method == "POST":
                password = request.form.get("password")
                profile = load_profile(f"protected/profiles/{username}.txt")
                create_profile(email=profile["email"], editing=False, password=password, username=username, display_name=profile["display_name"], background_color=profile["background_color"], container_color=profile["container_color"], button_color=profile["button_color"], button_hover_color=profile["button_hover_color"], button_text_color=profile["button_text_color"], text_color=profile["text_color"], footer_color=profile["footer_color"], about_me=profile["about_me"], www=profile["www"], www_name=profile["www_name"], instagram=profile["instagram"], instagram_name=profile["instagram_name"], facebook=profile["facebook"], facebook_name=profile["facebook_name"], x=profile["x"], x_name=profile["x_name"], github=profile["github"], github_name=profile["github_name"], linkedin=profile["linkedin"], linkedin_name=profile["linkedin_name"], discord=profile["discord"], steam=profile["steam"], steam_name=profile["steam_name"], profile_picture_path=profile["profile_picture_path"])
                os.remove(f"protected/tokens/{username}.txt")
                return redirect(f"/login")
        else:
            raise CustomError(403, "Invalid token.", "/")
        return render_template('reset-password.html', success = True, token = True, default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color)
    else:
        raise CustomError(403, "Password resetting is disabled.", "/")

@app.route('/profile/<username>')
def profile(username):
    if not os.path.exists(f"protected/profiles/{username}.txt"):
        raise CustomError(404, "Profile not found.", "/")
    profile = load_profile(f"protected/profiles/{username}.txt")
    return render_template("profile.html",
                        app_name = app_name,
                        **profile)

@app.route('/support')
def support():
    return render_template('support.html', default_background_color=default_background_color, default_container_color=default_container_color, default_button_color=default_button_color, default_button_hover_color = default_button_hover_color, default_button_text_color = default_button_text_color, default_input_color = default_input_color, default_text_color = default_text_color, default_footer_color = default_footer_color)

if __name__ == '__main__':
    app.run(host="localhost", port=port, debug=debug)