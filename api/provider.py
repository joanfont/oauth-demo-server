from datetime import datetime, timedelta
from flask import session
from flask.ext.oauthlib.provider import OAuth2Provider
from api import models


class MyProvider(OAuth2Provider):
    def __init__(self, app=None, db=None):
        super().__init__(app)
        self.db = db

    @property
    def _current_user(self):
        return models.User.query.get(session['id']) if 'id' in session else None

    def _clientgetter(self, client_id):
        print(client_id)
        return models.Client.query.filter_by(client_id=client_id).first()

    def _grantgetter(self, client_id, code):
        return models.Grant.query.filter_by(client_id=client_id, code=code).first()

    def _grantsetter(self, client_id, code, request):
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = models.Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            _scopes=' '.join(request.scopes),
            user=self._current_user,
            expires=expires)
        self.db.session.add(grant)
        self.db.session.commit()
        return grant

    def _tokengetter(self, access_token=None, refresh_token=None):
        if access_token:
            token = models.Token.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            token = models.Token.query.filter_by(refresh_token=refresh_token).first()
        else:
            token = None

        return token

    def _tokensetter(self, token, request):
        tokens = models.Token.query.filter_by(client_id=request.client.client_id, user_id=request.user.id)

        for t in tokens:
            self.db.session.delete(t)

        expires_in = token.pop('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        token = models.Token(
            access_token=token.get('access_token'),
            refresh_token=token.get('refresh_token'),
            token_type=token.get('token_type'),
            _scopes=token.get('scope'),
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user.id,
        )
        self.db.session.add(token)
        self.db.session.commit()
        return token
