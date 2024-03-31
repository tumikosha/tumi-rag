from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "RAG app"
    # db_uri: str = 'sqlite:///mydatabase.db'
    db_uri: str = 'postgresql://postgres:20_Meet_24#@localhost:5432/meetbook_dev_db'
    table_name: str = 'articles'
    addr: str = "0.0.0.0"
    port: int = 8899
    debug: bool = False
    verbose: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

#    'default': {
#    'ENGINE': 'django.db.backends.postgresql',

#         'NAME': 'meetbook_prod_db',
#         'USER': "postgres",
#         'PASSWORD': "20_Meet_24#",
# ? test                      #
# 'HOST': "localhost",
# 'HOST': "postgres",  # this host added to /etc/hos
#         'PORT': 5432,                                         }
