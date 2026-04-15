import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.new_book import NewBook  # noqa: E501
from openapi_server import util


def books_create_book(body):  # noqa: E501
    """Thêm sách mới

     # noqa: E501

    :param new_book: 
    :type new_book: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    new_book = body
    if connexion.request.is_json:
        new_book = NewBook.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def books_delete_book(id):  # noqa: E501
    """Xóa sách

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_get_book(id):  # noqa: E501
    """Lấy thông tin một cuốn sách

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_get_books():  # noqa: E501
    """Lấy danh sách toàn bộ sách

     # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    return 'do some magic!'


def books_update_book(id, body):  # noqa: E501
    """Cập nhật thông tin sách

     # noqa: E501

    :param id: 
    :type id: int
    :param new_book: 
    :type new_book: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    new_book = body
    if connexion.request.is_json:
        new_book = NewBook.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
