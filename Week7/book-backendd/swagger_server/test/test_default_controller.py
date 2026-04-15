# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.book_list_response import BookListResponse  # noqa: E501
from swagger_server.models.book_response import BookResponse  # noqa: E501
from swagger_server.models.create_book_request import CreateBookRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_api_v1_books_book_id_delete(self):
        """Test case for api_v1_books_book_id_delete

        Xóa sách
        """
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_book_id_get(self):
        """Test case for api_v1_books_book_id_get

        Lấy thông tin sách theo id
        """
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_book_id_patch(self):
        """Test case for api_v1_books_book_id_patch

        Cập nhật một phần sách
        """
        body = None
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id=56),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_book_id_put(self):
        """Test case for api_v1_books_book_id_put

        Cập nhật thông tin sách
        """
        body = CreateBookRequest()
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_get(self):
        """Test case for api_v1_books_get

        Lấy danh sách sách
        """
        response = self.client.open(
            '/api/v1/books',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_post(self):
        """Test case for api_v1_books_post

        Tạo sách mới
        """
        body = CreateBookRequest()
        response = self.client.open(
            '/api/v1/books',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_books_search_get(self):
        """Test case for api_v1_books_search_get

        Tìm kiếm sách
        """
        query_string = [('title', 'title_example')]
        response = self.client.open(
            '/api/v1/books/search',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
