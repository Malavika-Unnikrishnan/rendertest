import os
import instaloader
from flask import Flask, render_template

app = Flask(__name__)
L = instaloader.Instaloader()

# Ensure the directory for storing profile pictures exists
os.makedirs('static/imgs/instagram_profile_pictures', exist_ok=True)

@app.route('/')
def home():
    return '''
    <h1>Welcome to the Instagram Profile Picture Downloader</h1>
    <p>To download a profile picture, visit <code>/profilepic/&lt;username&gt;</code>.</p>
    '''

@app.route('/profilepic/<username>')
def profilepic(username: str):
    try:
        # Get profile info from Instagram
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Define the file path for saving the profile picture
        file_path = f'static/imgs/instagram_profile_pictures/{username}.jpg'
        
        # Download and save the profile picture
        L.context.get_and_write_raw(profile.profile_pic_url, file_path)
        
        return render_template('profilepic.html', username=username)
    except Exception as e:
        return f"<h1>Error:</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    # Run the app on the specified port (for deployment compatibility)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
