from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "secret_key"
oauth = OAuth(app)

github = oauth.register(
    name='github',
    client_id='Ov23lifoC3xoSBs8qItH',
    client_secret='83487dc13714522791d16a910be77c9a9653c12e',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/')
def home():
    return '<a href="/login">Login with GitHub</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    user = github.get('user').json()

    session['user'] = user

    return redirect('/profile')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized", 401

    user = session['user']

    return f"""
    <html>
    <head>
        <title>GitHub Profile</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                text-align: center;
                width: 400px;
            }}

            img {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                margin-bottom: 15px;
            }}

            h1 {{
                margin: 10px 0;
                color: #333;
            }}

            p {{
                color: #666;
                margin: 5px 0;
            }}

            .info {{
                margin-top: 20px;
                text-align: left;
            }}

            .btn {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #24292e;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }}

            .btn:hover {{
                background-color: #444;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            <img src="{user['avatar_url']}" alt="Profile Picture">

            <h1>{user.get('name', 'No Name')}</h1>

            <p>@{user['login']}</p>

            <p>{user.get('bio', 'No bio available')}</p>

            <div class="info">
                <p><strong>Email:</strong> {user.get('email', 'Not Public')}</p>

                <p><strong>Followers:</strong> {user['followers']}</p>

                <p><strong>Following:</strong> {user['following']}</p>

                <p><strong>Public Repositories:</strong> {user['public_repos']}</p>

                <p><strong>GitHub ID:</strong> {user['id']}</p>

                <p><strong>Account Created:</strong> {user['created_at']}</p>
            </div>

            <a class="btn" href="{user['html_url']}" target="_blank">
                View GitHub Profile
            </a>

            <br>

            <a class="btn" href="/logout">
                Logout
            </a>
        </div>
    </body>
    </html>
    """

@app.route('/logout')
def logout():
    session.pop('user', None)
    return "Logged out successfully"

if __name__ == '__main__':
    app.run(debug=True)
