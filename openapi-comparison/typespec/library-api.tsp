import "@typespec/http";
import "@typespec/rest";

using Http;
using Rest;

@service({
  title: "Library API"
})
namespace Library;

model Book {
  id: int32;
  title: string;
  author: string;
}

model CreateBookRequest {
  title: string;
  author: string;
}

@route("/books")
interface Books {

  @get
  listBooks(): Book[];

  @post
  @statusCode(201)
  createBook(@body body: CreateBookRequest): Book;

  @get
  @route("/{id}")
  getBook(@path id: int32): Book;

  @put
  @route("/{id}")
  updateBook(@path id: int32, @body body: CreateBookRequest): Book;

  @delete
  @route("/{id}")
  @statusCode(204)
  deleteBook(@path id: int32): void;
}