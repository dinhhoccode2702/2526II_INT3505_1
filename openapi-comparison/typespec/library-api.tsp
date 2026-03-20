import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;
using TypeSpec.OpenAPI;

@doc("API quản lý sách đơn giản sử dụng Flask.")
@info(#{
  version: "1.0.0"
})
@service(#{
  title: "Library API"
})
@server("http://localhost:5000", "Local server")
namespace LibraryAPI;

model Book {
  id: int32;
  title: string;
  author: string;
}

model NewBook {
  title: string;
  author: string;
}

@route("/books")
interface Books {
  @get
  @summary("Lấy danh sách toàn bộ sách")
  getBooks(): Book[];

  @post
  @summary("Thêm sách mới")
  createBook(@body book: NewBook): {
    @statusCode statusCode: 201;
    @body body: Book;
  } | {
    @statusCode statusCode: 400;
    @body error: string;
  };

  @get
  @route("/{id}")
  @summary("Lấy thông tin một cuốn sách")
  getBook(@path id: int32): Book | {
    @statusCode statusCode: 404;
    @body error: string;
  };

  @put
  @route("/{id}")
  @summary("Cập nhật thông tin sách")
  updateBook(@path id: int32, @body book: NewBook): Book | {
    @statusCode statusCode: 400;
    @body error: string;
  } | {
    @statusCode statusCode: 404;
    @body error: string;
  };

  @delete
  @route("/{id}")
  @summary("Xóa sách")
  deleteBook(@path id: int32): {
    @statusCode statusCode: 204;
  } | {
    @statusCode statusCode: 404;
    @body error: string;
  };
}