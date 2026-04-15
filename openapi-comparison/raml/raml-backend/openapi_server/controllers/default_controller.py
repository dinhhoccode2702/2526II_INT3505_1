import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.create_book_request import CreateBookRequest  # noqa: E501
from openapi_server import util


def d_elete_books_id(id):  # noqa: E501
    """d_elete_books_id

    Delete book # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def g_et_books():  # noqa: E501
    """g_et_books

    Get all books # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    return 'do some magic!'


def g_et_books_id(id):  # noqa: E501
    """g_et_books_id

    Get book by ID # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def p_ost_books(body):  # noqa: E501
    """p_ost_books

    Create a new book # noqa: E501

    :param create_book_request: 
    :type create_book_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    create_book_request = body
    if connexion.request.is_json:
        create_book_request = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def p_ut_books_id(id, body):  # noqa: E501
    """p_ut_books_id

    Update book # noqa: E501

    :param id: 
    :type id: int
    :param create_book_request: 
    :type create_book_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    create_book_request = body
    if connexion.request.is_json:
        create_book_request = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
