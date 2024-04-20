from flask import Flask, Blueprint
from flask import jsonify
from flask import request
from flask import abort
from helpers import swagger
from flask_cors import CORS, cross_origin
from infrastructure.repositories import book_repository, user_repository

name = 'BookStore-API'

app = Flask(name, static_url_path= '/src/static')
CORS(app)

@app.route('/book/getall', methods = ['GET'])
def obter_livros() :
    books = book_repository.getAllBooks()
    return jsonify(books)

@app.route('/book/getbyid/<int:id>', methods = ['GET'])
def obter_livro_por_id(id) :
    book = book_repository.getBookById(id)
    return jsonify(book)
        
@app.route('/book/put/<int:id>', methods = ['PUT'])
def editar_livro_por_id(id) :
    livro_alterado = request.get_json() 
    book = book_repository.updateBook(livro_alterado, id)
    return jsonify(book)
        
@app.route('/book/post', methods = ['POST'])
def incluir_novo_livro() : 
    novo_livro = request.get_json() 
    book_repository.insertBook(novo_livro)
    return jsonify({})

@app.route('/book/delete/<int:id>', methods = ['DELETE'])
def deletar_livro(id) : 
    book_repository.deleteBook(id)
    return jsonify({})

@app.route('/user/auth', methods = ['POST'])
def autenticar_usuario() :
    autenticar_request = request.get_json()
    user = user_repository.autenticateUser(autenticar_request)
    
    if user is None:
        abort()
    
    return jsonify(user)
       
@app.route('/user/post', methods = ['POST'])
def incluir_novo_usuario() : 
    novo_usuario = request.get_json()
    user = user_repository.insertUser(novo_usuario)
    return jsonify({})

swagger.swagger_config(name, app)

app.run(port=5000,host='localhost',debug='true')
