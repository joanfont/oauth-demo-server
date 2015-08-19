import json

from flask import request, session, render_template, Response, redirect, url_for
from flask.views import MethodView

from werkzeug.security import gen_salt

from api import db
from api import models
from api.helpers import get_current_user


class APIView(MethodView):
    @staticmethod
    def get_data():
        return request.args

    @staticmethod
    def post_data():
        return dict(
            (key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for
            key in request.form.keys())

    @staticmethod
    def files_data():
        return dict(
            (key, request.files.getlist(key) if len(request.files.getlist(key)) > 1 else request.files.getlist(key)[0])
            for key in request.files.keys())

    @staticmethod
    def current_user():
        return get_current_user()

    @staticmethod
    def jsonify(data):
        response = json.dumps(data)
        return Response(response, content_type='application/json')

    @staticmethod
    def redirect_view(view_name):
        return redirect(url_for(view_name))


class HomeView(APIView):
    def get(self, *args, **kwargs):
        user = self.current_user()
        return render_template('index.html', user=user)

    def post(self, *args, **kwargs):
        post_data = self.post_data()
        username = post_data.get('username')
        user = models.User.query.filter_by(username=username).first()
        if not user:
            user = models.User(username=username)
            db.session.add(user)
            db.session.commit()

        session['id'] = user.id
        return self.redirect_view('home')


class ClientView(APIView):
    def get(self, *args, **kwargs):
        user = self.current_user()

        if not user:
            return self.redirect_view('home')

        client = models.Client(
            client_id=gen_salt(40),
            client_secret=gen_salt(50),
            _redirect_uris=' '.join([
                'http://localhost:8000/authorized/',
                'http://127.0.0.1:8000/authorized/',
                'http://127.0.1:8000/authorized/',
                'http://127.1:8000/authorized/',
            ]),
            _default_scopes='email',
            user_id=user.id,
        )

        db.session.add(client)
        db.session.commit()

        return self.jsonify({
            'client_id': client.client_id,
            'client_secret': client.client_secret,
        })


class MeView(APIView):
    def get(self, *args, **kwargs):
        user = request.oauth.user
        return self.jsonify({
            'username': user.username
        })


class AuthorizeView(APIView):
    def before_request(self):
        if not self.current_user():
            self.redirect_view('/')

    def get(self, *args, **kwargs):
        self.before_request()
        get_data = self.get_data()
        client_id = get_data.get('client_id')
        kwargs['client'] = models.Client.query.filter_by(client_id=client_id).first()
        kwargs['user'] = self.current_user()

        return render_template('authorize.html', **kwargs)

    def post(self, *args, **kwargs):
        self.before_request()
        post_data = self.post_data()
        confirm = post_data.get('confirm', 'no')
        return confirm == 'yes'


class AccessTokenView(APIView):
    def get(self, *args, **kwargs):
        return self.common()

    def post(self, *args, **kwargs):
        return self.common()

    @staticmethod
    def common():
        return {}
