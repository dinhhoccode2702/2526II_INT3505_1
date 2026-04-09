import unittest

from flask import json

from OpenAPISpec.models.book_list_response import BookListResponse  # noqa: E501
from OpenAPISpec.models.book_response import BookResponse  # noqa: E501
from OpenAPISpec.models.create_book_request import CreateBookRequest  # noqa: E501
from OpenAPISpec.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_api_v1_books_book_id_delete(self):
        """Test case for api_v1_books_book_id_delete

        Xóa sách
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_book_id_get(self):
        """Test case for api_v1_books_book_id_get

        Lấy thông tin sách theo id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_book_id_patch(self):
        """Test case for api_v1_books_book_id_patch

        Cập nhật một phần sách
        """
        body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id=56),
            method='PATCH',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_book_id_put(self):
        """Test case for api_v1_books_book_id_put

        Cập nhật thông tin sách
        """
        create_book_request = {"published_year":0,"author":"author","price":6.027456183070403,"genre":"genre","title":"title","is_available":True}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(create_book_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_get(self):
        """Test case for api_v1_books_get

        Lấy danh sách sách
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_post(self):
        """Test case for api_v1_books_post

        Tạo sách mới
        """
        create_book_request = {"published_year":0,"author":"author","price":6.027456183070403,"genre":"genre","title":"title","is_available":True}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books',
            method='POST',
            headers=headers,
            data=json.dumps(create_book_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_search_get(self):
        """Test case for api_v1_books_search_get

        Tìm kiếm sách
        """
        query_string = [('title', 'title_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/search',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
