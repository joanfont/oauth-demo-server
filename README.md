OAuth2 demo server & client
===========================

This is a simple OAuth2 demo server and client to test OAuth2 workflow. It's written for Python 3.4 and uses Flask, SQLAlchemy, Flask-OAuthlib and MySQL as database system.

Server
------

To start the server just run: `python app.py`

Client
------

Tu start the client just run: `python client.py`

Configuration
-------------

You must create `.env` file with vars in `env.sample` setted.


Flow
----

1. Run the server
2. Go to `localhost:5000` and type a user name
3. Go to `localhost:5000/client/` and get `client_id` and `client_secret`
4. Open `client.py` and set both vars `CLIENT_ID` and `CLIENT_SECRET` with the values obtained at the previous step
5. Run the client
6. Go to `localhost:8000` (you'll be redirected to a server page)
7. Authorize the application to access to your user data
8. You'll be redirected to a page where you will see an `access_token`
9. Go to `localhost:8000` and you'll see on the screen the user name typed at the second step