from mongoengine import Document, StringField, FloatField, IntField, BooleanField

class BookDB(Document):
    title = StringField(required=True)
    author = StringField()
    genre = StringField()
    published_year = IntField()
    price = FloatField()
    is_available = BooleanField(default=True)

    meta = {'collection': 'books'} # Tên bảng trong database
