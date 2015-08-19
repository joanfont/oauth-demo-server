from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from api import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(80))

    name = Column(String(40))

    def to_string(self):
        return u'<User {}>'.format(self.username)

    def __unicode__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


class Client(db.Model):
    client_id = Column(String(40), primary_key=True)
    client_secret = Column(String(55), nullable=False)

    user_id = Column(ForeignKey('user.id'))
    user = relationship('User')

    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Model):
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User')

    client_id = Column(String(40), ForeignKey('client.client_id'), nullable=False)
    client = relationship('Client')

    code = Column(String(255), index=True, nullable=False)

    redirect_uri = Column(String(255))
    expires = Column(DateTime)

    _scopes = Column(Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    id = Column(Integer, primary_key=True)
    client_id = Column(String(40), ForeignKey('client.client_id'), nullable=False)

    client = relationship('Client')

    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User')

    token_type = Column(String(40))

    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    expires = Column(DateTime)
    _scopes = Column(Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
