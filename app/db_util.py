import base64

from app import util, examples
from app.settings import Settings
import zlib
import binascii

import dataset as dataset

settings = Settings()

STD_VECTOR_SIZE = 384

from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2")


def make_table(db, table_name="articles"):
    try:
        result = db.query('CREATE EXTENSION vector;')
    except Exception as err:
        pass
        # print(err)
    try:
        # result = db.query('CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));')
        # result = db.query("CREATE TABLE items2 id TEXT NOT NULL DEFAULT 'tag_' PRIMARY KEY, embedding vector(3));")
        result = db.query(
            f'CREATE TABLE {table_name} (id varchar(36) NOT NULL, embedding vector({STD_VECTOR_SIZE}),  PRIMARY KEY (id));')
    except Exception as err:
        pass
        # print(err)
    print(db.tables)


def insert_row(db, url, article, table_name="articles"):
    vector = encoder.encode(article).tolist()
    row = {
        "id": str(util.string_to_uuid4(url)),
        "url": url,
        "embedding": vector,
        "article": article
    }
    db[table_name].upsert(row, ['id'])


def search(db, query_text, table_name="articles", limit=10):
    vector = encoder.encode(query_text).tolist()
    res = db.query(f"SELECT * FROM articles ORDER BY embedding <-> '{vector}' LIMIT {limit};")
    out = []
    for row in res:
        del row['embedding']
        out.append(row)
    return out


def compress_text(text):
    text_bytes = text.encode('utf-8')
    compressed_data = zlib.compress(text_bytes)
    # compressed_base64 = compressed_data.hex()
    compressed_base64 = base64.b64encode(compressed_data)
    return "CMP:" + str(compressed_base64)


def decompress_text(compressed_text):
    # compressed_data = bytes.fromhex(compressed_text)
    compressed_data = base64.b64decode(compressed_text[3:])
    decompressed_data = zlib.decompress(compressed_data)
    decompressed_text = decompressed_data.decode('utf-8')
    return decompressed_text


# Example text
original_text = "This is a sample text to compress and decompress."
original_text = examples.gagauz

# Compress text
compressed_text = compress_text(original_text)
print("Compressed Text (Base64):", len(compressed_text), compressed_text)

# Decompress text
decompressed_text = decompress_text(compressed_text)
print("Decompressed Text:", len(decompressed_text))

#
# def zip(teststr):
#     # return zlib.compress(teststr.encode('utf-8'))
#     return binascii.hexlify(zlib.compress(teststr.encode('utf-8')))
#     # uncmpstr = zlib.decompress(cmpstr)
#     #
#     # fmt = '{:>8}: (length {}) {!r}'
#     # print(fmt.format('teststr', len(teststr), teststr))
#     # print(fmt.format('cmpstr', len(cmpstr), cmpstr))
#     # print(fmt.format('uncmpstr', len(uncmpstr), uncmpstr))

# with TRIAL:
#     app.table = app.db.query("ALTER TABLE articles ADD COLUMN embeddings public.vector;")
# app.table = app.db.query("ALTER TABLE articles ADD COLUMN embedding public.vector(1024);")
# app.table.upsert(dict(id=1, embeddings=[]), ["id"], ensure=True)
#
# db = dataset.connect(settings.db_uri)
# make_table(db)
# search(db, "examples")
# s = zip("Hello world!")
# print(s)
