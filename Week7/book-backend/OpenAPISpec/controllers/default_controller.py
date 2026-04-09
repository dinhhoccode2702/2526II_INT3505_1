import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from OpenAPISpec.models.book_list_response import BookListResponse  # noqa: E501
from OpenAPISpec.models.book_response import BookResponse  # noqa: E501
from OpenAPISpec.models.create_book_request import CreateBookRequest  # noqa: E501
from OpenAPISpec import util


def api_v1_books_book_id_delete(book_id):  # noqa: E501
    """Xóa sách

     # noqa: E501

    :param book_id: 
    :type book_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def api_v1_books_book_id_get(book_id):  # noqa: E501
    """Lấy thông tin sách theo id

     # noqa: E501

    :param book_id: 
    :type book_id: int

    :rtype: Union[BookResponse, Tuple[BookResponse, int], Tuple[BookResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def api_v1_books_book_id_patch(book_id, body=None):  # noqa: E501
    """Cập nhật một phần sách

     # noqa: E501

    :param book_id: 
    :type book_id: int
    :param body: 
    :type body: 

    :rtype: Union[BookResponse, Tuple[BookResponse, int], Tuple[BookResponse, int, Dict[str, str]]
    """
    body = body
    return 'do some magic!'


def api_v1_books_book_id_put(book_id, body):  # noqa: E501
    """Cập nhật thông tin sách

     # noqa: E501

    :param book_id: 
    :type book_id: int
    :param create_book_request: 
    :type create_book_request: dict | bytes

    :rtype: Union[BookResponse, Tuple[BookResponse, int], Tuple[BookResponse, int, Dict[str, str]]
    """
    create_book_request = body
    if connexion.request.is_json:
        create_book_request = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_v1_books_get():  # noqa: E501
    """Lấy danh sách sách

     # noqa: E501


    :rtype: Union[BookListResponse, Tuple[BookListResponse, int], Tuple[BookListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def api_v1_books_post(body):  # noqa: E501
    """Tạo sách mới

     # noqa: E501

    :param create_book_request: 
    :type create_book_request: dict | bytes

    :rtype: Union[BookResponse, Tuple[BookResponse, int], Tuple[BookResponse, int, Dict[str, str]]
    """
    create_book_request = body
    if connexion.request.is_json:
        create_book_request = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_v1_books_search_get(title=None):  # noqa: E501
    """Tìm kiếm sách

     # noqa: E501

    :param title: Tìm kiếm theo tiêu đề sách
    :type title: str

    :rtype: Union[BookListResponse, Tuple[BookListResponse, int], Tuple[BookListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'
