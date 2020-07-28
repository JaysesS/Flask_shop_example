# Flask_shop_example

*This project was written for summary and practice purposes.*

### Tech

- [Flask](https://flask.palletsprojects.com/) - Python framework
- [Sqlite3](https://www.sqlite.org) - SQL database engine
- [Docker](https://www.docker.com/)

### What does this app do?

For user:
- SingUp
- SingIn
- Set info in account
- Add product to cart
- Make order

For admin:
- View/Change user info
- View/Change product info
- View/Change order info
- Refill the products in shop using a file (*flask/app/products.json*)
- Delete all products in shop

### Installation


*Run in docker:*
```sh
$ git clone https://github.com/JaysesS/Flask_shop_example.git && cd Flask_shop_example
$ docker-compose build
$ docker-compose up
127.0.0.1:80
```
*Run local:*
```sh
$ git clone https://github.com/JaysesS/Flask_shop_example.git && cd Flask_shop_example
```
Setup path to database.db in config.py
```sh
$ python3 flask/run.py
127.0.0.1:5000
```

Admin login / passwd : **jayse** / **privetpoka**
or  **Create new user with username admin**