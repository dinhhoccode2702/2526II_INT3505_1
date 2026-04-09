#!/usr/bin/env python3

import connexion
from mongoengine import connect 
from OpenAPISpec import encoder


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Book API'},
                pythonic_params=True)
    # ---- Setup Database MongoDB ----
    # Nếu chạy local: connect(host="mongodb://localhost:27017/product_db")
    connect(host="mongodb://localhost:27017/book_manager")
    print("[OK] Da ket noi MongoDB thanh cong!")
    # --------------------------------            
    app.run(port=8080)


if __name__ == '__main__':
    main()
