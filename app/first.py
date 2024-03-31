# pip install dataset
# https://github.com/pudo/dataset/blob/master/docs/quickstart.rst
# https://dataset.readthedocs.io/_/downloads/en/latest/pdf/
import uuid
import hashlib
import dataset
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2")

STD_VECTOR_SIZE = 384

# from stuf import stuf

# db = dataset.connect('sqlite:///:memory:')
# mysql = dataset.connect('mysql://airflow:airflow123@localhost/fixiegen')
# db = dataset.connect('postgresql://scott:tiger@localhost:5432/mydatabase')
# db = dataset.connect('postgresql+psycopg2://postgres:20_Meet_24#@localhost/tumi_storage', row_type=stuf)
# db = dataset.connect('postgresql://postgres:20_Meet_24#@localhost/tumi_storage')
db = dataset.connect('postgresql://postgres:20_Meet_24#@localhost:5432/meetbook_dev_db')


# create_table(table_name, primary_id=None, primary_type=None, primary_increment=None)

# id = int(hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest(), 16) % (10 ** 4)


def url_to_uuid(url, size=36):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, url))


def random_uuid():
    return str(uuid.uuid4())


print(random_uuid())


def hash_url(url, size=36):
    return hashlib.shake_256(url.encode('utf-8')).hexdigest(int(size / 2))


txt_4_vector = "this is text"

# table = db['articles']
url = "http://dirs.info/aaa/bbb?zzz=xxxx*ccc=vvvv"
vector = encoder.encode(txt_4_vector).tolist()  # !!!!!!!!!!!!!!!!

row = {
    "id": random_uuid(),
    # "id": url_to_uuid(url),
    "url": url,
    "zone": "main",
    "text": "main",
    "lang": "ru",
    "summary_en": "main",
    "summary_ru": "main",
    "summary_ro": "main",
    "pers": ["Veaceslav"],
    "locs": ["Moldova"],
    "orgs": ["House"],
    "embedding": vector,
}
try:
    result = db.query('CREATE EXTENSION vector;')
except Exception as err:
    print(err)
try:
    # result = db.query('CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));')
    # result = db.query("CREATE TABLE items2 id TEXT NOT NULL DEFAULT 'tag_' PRIMARY KEY, embedding vector(3));")
    result = db.query(
        f'CREATE TABLE articles (id varchar(36) NOT NULL, embedding vector({STD_VECTOR_SIZE}),  PRIMARY KEY (id));')
except Exception as err:
    print(err)

table = db['articles']
# table = db.create_table('articles', primary_id='id', primary_type=db.types.string(36)
#                         # primary_id=False,
#                         # primary_type=db.types.text,
#                         )
# table.create_column('created_at', db.types.datetime)
# table.create_column('embeddings', db.types.)
# table = db.load_table('articles')
print(db.tables)
table.insert(row)
# john = table.find_one(name='John Doe')
# SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
# result = db.query(f"SELECT * FROM articles ORDER BY embedding <-> '[3,1,2]' LIMIT 5;")
result = db.query(f"SELECT * FROM articles ORDER BY embedding <-> '{vector}' LIMIT 5;")
for row in result:
    print(row['url'], row['text'])

# print(db.tables)
# print(table.columns)
#
# print(url_to_uuid("http://dirs.info/aaa/bbb?qwr&weqwe=1"))
# print(url_to_uuid("http://dirs.info/aaa/bbb?qwr&weqwe=2&nbsp;111"))
# print(len(url_to_uuid("http://dirs.info/aaa/bbb?qwr&weqwe=2&nbsp;111")))
