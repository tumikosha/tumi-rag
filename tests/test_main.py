import dataset

from app import util
from app.models import PutQuery


def test_get():
    assert True



# def test_get():
#     # db = dataset.connect('sqlite:///:memory:')
#     db = dataset.connect('sqlite:///mydatabase.db')
#     table = db['sometable']
#     query: PutQuery = PutQuery()
#     url_uuid = str(util.string_to_uuid4(str(query.url)))
#     print(query)
#     row = dict(url_uuid=url_uuid, url=query.url, article=query.article)
#     table.upsert(row, ["url_uuid"], ensure=True)
#     print()
#     for row in table.all():
#         print("***", row)
#
#     res = table.find_one(url_uuid=url_uuid)
#     # print(res)
#
#     assert True
#     assert res['url_uuid'] == url_uuid
