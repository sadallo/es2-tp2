import os, requests
from flask import Flask, request, json
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
	return "Light Twitter - Modulo de Timeline - Gabriel Almeida, Gabriel Soares, Henrique Fonseca e Sadallo Andere"


# requisita ao modulo de Usuarios os usuarios seguidos por um determinado usuario
# auxiliar da funcao debaixo
def getSeguidos(usuario):
	seguidos = requests.get('http://es2-usr.herokuapp.com/getfollowed/{}'.format(usuario)).json()
	return str(seguidos)


#requisita ao modulo de mensagens as mensagens dos seguidos de um determinado usuario
@app.route('/home/<usuario>')
def getMensagensSeguidos(usuario):
	seguidos_por_usuario = requests.get('http://es2-usr.herokuapp.com/getfollowed/{}'.format(usuario)).json()[usuario]
	mensagens = "{}<br><br>Essas sao as mensagens de quem sigo:<br>".format(getMensagensUsuario(usuario))
	for i in range(0, len(seguidos_por_usuario)):
		mensagens_seguido = (requests.get('http://es2-message.herokuapp.com/getmessagebyuserid/{}'.format(seguidos_por_usuario[i])).json())
		mensagens = "{}<br>{}".format(mensagens, mensagens_seguido)

	return mensagens

#requisita ao modulo de mensagens de um determinado usuario
@app.route('/posts/<usuario>')
def getMensagensUsuario(usuario):
	mensagens = requests.get('http://es2-message.herokuapp.com/getmessagebyuserid/{}'.format(usuario)).json()[usuario]
	return "Sou o usuario {} essas sao as minhas mensagens:<br><br>{}".format(usuario, mensagens)




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)