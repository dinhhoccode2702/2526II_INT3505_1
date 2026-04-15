import connexion
import six

from swagger_server.models.book_list_response import BookListResponse  # noqa: E501
from swagger_server.models.book_response import BookResponse  # noqa: E501
from swagger_server.models.create_book_request import CreateBookRequest  # noqa: E501
from swagger_server.models.book import Book  # noqa: E501
from swagger_server import util

# IMPORT MONGODB MODEL
from swagger_server.models.book_db import BookDB

def db_to_swagger_book(mongodb_book):
    return Book(
        id=str(mongodb_book.id),
        title=mongodb_book.title,
        author=mongodb_book.author,
        genre=mongodb_book.genre,
        published_year=mongodb_book.published_year,
        price=mongodb_book.price,
        is_available=mongodb_book.is_available
    )

def api_v1_books_book_id_delete(book_id):  # noqa: E501
    try:
        book = BookDB.objects.get(id=book_id)
        book.delete()
        return 'Deleted', 204
    except BookDB.DoesNotExist:
        return 'Not Found', 404
    except Exception as e:
        return str(e), 400

def api_v1_books_book_id_get(book_id):  # noqa: E501
    try:
        book = BookDB.objects.get(id=book_id)
        return BookResponse(success=True, data=db_to_swagger_book(book), message="Success")
    except BookDB.DoesNotExist:
        return 'Not found', 404
    except Exception as e:
        return str(e), 400

def api_v1_books_book_id_patch(book_id, body=None):  # noqa: E501
    if connexion.request.is_json:
        update_data = connexion.request.get_json()
        try:
            book = BookDB.objects.get(id=book_id)
            for key, value in update_data.items():
                if hasattr(book, key) and key != 'id':
                    setattr(book, key, value)
            book.save()
            return BookResponse(success=True, data=db_to_swagger_book(book), message="Updated successfully")
        except BookDB.DoesNotExist:
            return 'Not found', 404
        except Exception as e:
            return str(e), 400
    return 'Invalid data', 400

def api_v1_books_book_id_put(body, book_id):  # noqa: E501
    if connexion.request.is_json:
        req = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
        try:
            book = BookDB.objects.get(id=book_id)
            book.title = req.title
            book.author = req.author
            book.genre = req.genre
            book.published_year = req.published_year
            book.price = req.price
            book.is_available = req.is_available
            book.save()
            return BookResponse(success=True, data=db_to_swagger_book(book), message="Updated successfully")
        except BookDB.DoesNotExist:
            return 'Not found', 404
        except Exception as e:
            return str(e), 400
    return 'Invalid data', 400

def api_v1_books_get():  # noqa: E501
    try:
        books_db = BookDB.objects()
        books_list = [db_to_swagger_book(b) for b in books_db]
        return BookListResponse(success=True, data=books_list, message="Success")
    except Exception as e:
        return str(e), 500

def api_v1_books_post(body):  # noqa: E501
    print(body)
    if connexion.request.is_json:
        req = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
        try:
            new_book = BookDB(
                title=getattr(req, 'title', None) or body.get('title'),
                author=getattr(req, 'author', None) or body.get('author'),
                genre=getattr(req, 'genre', None) or body.get('genre'),
                published_year=getattr(req, 'published_year', None) or body.get('published_year'),
                price=getattr(req, 'price', None) or body.get('price'),
                is_available=getattr(req, 'is_available', True)
            )
            new_book.save()
            return BookResponse(success=True, data=db_to_swagger_book(new_book), message="Created successfully"), 201
        except Exception as e:
            return str(e), 400
    return 'Invalid input', 400

def api_v1_books_search_get(title=None):  # noqa: E501
    try:
        if title:
            books_db = BookDB.objects(title__icontains=title)
        else:
            books_db = BookDB.objects()
        books_list = [db_to_swagger_book(b) for b in books_db]
        return BookListResponse(success=True, data=books_list, message="Success")
    except Exception as e:
        return str(e), 500
