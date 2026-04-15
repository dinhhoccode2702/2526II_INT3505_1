#!/usr/bin/env python3

import connexion
from mongoengine import connect 
from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Book API'}, pythonic_params=True)
    
    # KẾT NỐI MONGODB PHẢI ĐẶT TRƯỚC APP.RUN()
    connect(host="mongodb://localhost:27017/book_manager")
    print("[OK] Da ket noi MongoDB thanh cong!")
    
    app.run(port=8080)

if __name__ == '__main__':
    main()
