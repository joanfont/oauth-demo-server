from os import environ, path
from dotenv import read_dotenv

read_dotenv(path.join(path.dirname(__file__), '../.env'))


SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passw}@{host}:{port}/{name}'.format(user=environ.get('MYSQL_USER'),
                                                                                   passw=environ.get('MYSQL_PASS'),
                                                                                   host=environ.get('MYSQL_HOST'),
                                                                                   port=environ.get('MYSQL_PORT'),
                                                                                   name=environ.get('MYSQL_NAME'))
