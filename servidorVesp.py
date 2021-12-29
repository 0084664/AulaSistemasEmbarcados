import flask
import socket
from flask import request, jsonify
from mysql.connector import connect,Error
import pygame as pg
import time
import sys
import os

try:
    connection = connect(
        host="localhost",
        user="ds403",
        password="cotuca",
        database = 'ds403')
except:
    print('Banco de dados não conectado')
    exist(1)

app = flask.Flask(__name__)

app.config["DEBUG"] = True

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


@app.route("/")

def index():
   return "<form><h1>Lista de Espera</h1><p><h3>Lista completa de nomes</h3><p><a href= 'getLista'>Clique aqui</a>"

@app.route("/insere", methods=['POST'])
def insere():
    parametroJson = request.get_json()
    if(not(parametroJson)):#entra se o parametro json for null(none)
        return jsonify(
            {
                "cod": 0,
                "status": "nenhum json passado"
            }
        )
   
    if((not('nome' in parametroJson)) or (not('data' in parametroJson))):
        return jsonify({
                "cod": 0,
                "status": "necessário passar todos os parâmetros"
        })
   
    if(len(parametroJson["data"]) != 10):
        return jsonify({
                "cod": 0,
                "status": "inserir 10 caracteres"
        })
   
    consulta    = "insert into lista values(%s, %s, %s)"
    informacoes = (int(parametroJson['id']), parametroJson['nome'], parametroJson['data'])
    try:
        cursor = connection.cursor()#acessa bd
        cursor.execute(consulta, informacoes)
        cursor.execute("commit")
    except:
        return jsonify(
            {
                "cod": 0,
                "status": "Nao inserido"
            }
        )
       
    return jsonify(
        {
            "cod": 1,
            "status": "Inserido"
        }
    )
   
@app.route("/getLista")
def ListaInteira():
    try:
        cursor = connection.cursor()
        cursor.execute("select * from lista")
        nomesTuplas = cursor.fetchall()
       
        listaNomes = []
        for nomeTupla in nomesTuplas:
            listaNomes.append(
                {"id": nomeTupla[0], "nome": nomeTupla[1]}
            )
    except:
        return jsonify(
            {
                "cod": 0,
                "status": "Problemas ao trazer a lista"
            }    
        )
    return jsonify({"cod":1,"dados":listaNomes})
   
@app.route("/getDetalhe")
def DetalehaDeUmaPessoa():
    parametro = request.args.get('id')
   
    if(not(parametro)):
        return jsonify({
            "cod": 0,
            "status": "passe um id existente"
        })

    try:
        parametro = int(parametro)
    except:
        return jsonify({
            "cod": 0,
            "status": "passe um ID do tipo inteiro"
        })
    cursor = connection.cursor()
    cursor.execute("select * from lista where id = {}".format(parametro))
    nome = cursor.fetchone()
    try:
        return jsonify({"cod":1,"dados":{
            "id":   nome[0],
            "nome": nome[1],
            "data": nome[2]      
        }})

    except:
        return jsonify({
            "cod": 0,
            "status": "Id não existente"
        })
   
@app.route("/apagaID", methods=['DELETE'])
def apagar():
    parametro = request.args.get('id')

    if(not(parametro)):
        return jsonify({
            "cod": 0,
            "status": "Passe um parametro id"
        })

    try:
        parametro = int(parametro)

    except:
        return jsonify({
            "cod": 0,
            "status": "Passe um ID do tipo inteiro"
        })
   
    cursor = connection.cursor()
   
    cursor.execute("select * from lista where id = {}".format(parametro))

    usuarioDeletado = cursor.fetchone()
   
    print(usuarioDeletado)
   
    pg.init()
   
    pg.font.init()
   
    white = (255,255,255)
    red = (255,0,0)
    screen_width = 600
    screen_height = 400
   
    screen = pg.display.set_mode((screen_width,screen_height) ,pg.RESIZABLE)
   
    font = pg.font.SysFont('Comic Sans MS', 32)
    text = font.render(usuarioDeletado[1] + usuarioDeletado[2], True, white, red)
   
    textRect = text.get_rect()
    textRect.center = (screen_width/2 - 15, screen_height/2 - 15)
   
    screen.fill(white)
   
    screen.blit(
        text,
        textRect
    )
   
    pg.display.flip()
   
    time.sleep(4)
   
    try:
        cursor = connection.cursor()
        cursor.execute("delete from lista where id = {}".format(parametro))
        cursor.execute("commit")
    except:
        return jsonify({
            "cod": 0,
            "status": "Nao apagou"
        })
   
    return jsonify({
            "cod": 1,
            "status": "Apagou"
        })
   

if __name__ == '__main__':
    app.run(host=local_ip, port= 8080)