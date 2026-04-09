import connexion
from typing import Dict, Tuple, Union

from OpenAPISpec.models.book_list_response import BookListResponse  # noqa: E501
from OpenAPISpec.models.book_response import BookResponse  # noqa: E501
from OpenAPISpec.models.create_book_request import CreateBookRequest  # noqa: E501
from OpenAPISpec.models.book import Book
from OpenAPISpec import util

from OpenAPISpec.models.book_db import BookDB

def db_to_book(b: BookDB) -> Book:
    return Book(
        id=str(b.id),
        title=b.title,
        author=b.author,
        genre=b.genre,
        published_year=b.published_year,
        price=b.price,
        is_available=b.is_available
    )

def api_v1_books_book_id_delete(book_id):  # noqa: E501
    """Xóa sách"""
    try:
        book = BookDB.objects.get(id=book_id)
        book.delete()
        return '', 204
    except BookDB.DoesNotExist:
        return 'Not Found', 404
    except Exception as e:
        return str(e), 400

def api_v1_books_book_id_get(book_id):  # noqa: E501
    """Lấy thông tin sách theo id"""
    try:
        book = BookDB.objects.get(id=book_id)
        return BookResponse(success=True, data=db_to_book(book), message="Success")
    except BookDB.DoesNotExist:
        return 'Not found', 404
    except Exception as e:
        return str(e), 400

def api_v1_books_book_id_patch(book_id, body=None):  # noqa: E501
    """Cập nhật một phần sách"""
    if not connexion.request.is_json:
        return 'Bad request', 400
    try:
        book = BookDB.objects.get(id=book_id)
        update_data = connexion.request.get_json()
        for key, value in update_data.items():
            if hasattr(book, key) and key != 'id':
                setattr(book, key, value)
        book.save()
        return BookResponse(success=True, data=db_to_book(book), message="Updated successfully")
    except BookDB.DoesNotExist:
        return 'Not found', 404
    except Exception as e:
        return str(e), 400

def api_v1_books_book_id_put(book_id, body):  # noqa: E501
    """Cập nhật thông tin sách"""
    if not connexion.request.is_json:
        return 'Bad request', 400
    try:
        book = BookDB.objects.get(id=book_id)
        update_req = CreateBookRequest.from_dict(connexion.request.get_json())
        book.title = update_req.title
        book.author = update_req.author
        book.genre = update_req.genre
        book.published_year = update_req.published_year
        book.price = update_req.price
        book.is_available = update_req.is_available
        book.save()
        return BookResponse(success=True, data=db_to_book(book), message="Updated successfully")
    except BookDB.DoesNotExist:
        return 'Not found', 404
    except Exception as e:
        return str(e), 400

def api_v1_books_get():  # noqa: E501
    """Lấy danh sách sách"""
    try:
        books_db = BookDB.objects()
        books_list = [db_to_book(b) for b in books_db]
        return BookListResponse(success=True, data=books_list, message="Success")
    except Exception as e:
        return str(e), 500

def api_v1_books_post(body):  # noqa: E501
    """Tạo sách mới"""
    if not connexion.request.is_json:
        return 'Bad request', 400
    try:
        create_req = CreateBookRequest.from_dict(connexion.request.get_json())
        new_book = BookDB(
            title=create_req.title,
            author=create_req.author,
            genre=create_req.genre,
            published_year=create_req.published_year,
            price=create_req.price,
            is_available=create_req.is_available
        )
        new_book.save()
        return BookResponse(success=True, data=db_to_book(new_book), message="Created successfully"), 201
    except Exception as e:
        return str(e), 400

def api_v1_books_search_get(title=None):  # noqa: E501
    """Tìm kiếm sách"""
    try:
        if title:
            books_db = BookDB.objects(title__icontains=title)
        else:
            books_db = BookDB.objects()
        books_list = [db_to_book(b) for b in books_db]
        return BookListResponse(success=True, data=books_list, message="Success")
    except Exception as e:
        return str(e), 500
