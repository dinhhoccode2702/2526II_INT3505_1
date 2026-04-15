from mongoengine import Document, StringField, FloatField, BooleanField, IntField

class BookDB(Document):
    meta = {'collection': 'books'} # Tên bảng trong MongoDB Compass
    
    title = StringField(required=True)
    author = StringField(required=True)
    genre = StringField()
    published_year = IntField()
    price = FloatField()
    is_available = BooleanField(default=True)