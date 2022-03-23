from time import strftime
import telebot
import random
import pickle
from os.path import exists
from datetime import datetime

# pegando chave API do do documento de texto api_key
with open("api_key", "r") as arquivo:
    APIkey = arquivo.read()
bot = telebot.TeleBot(APIkey)


# ------------------------------------------------------------------
# testes:

# roles

# Exemplos
# /role marcar ficar doidão na uni, 25/03/2022 22:00, trazer mt birita e droga
# /role remarcar ficar doidão na uni, 26/03/2022 22:00, trazer ainda mais birita e droga
# /role desmarcar ficar doidão na uni
# /role consultar
# /role falta_quanto ficar doidão na uni

class Evento:
    def __init__(self, nome, data, descricao):
        self.nome = nome
        self.data = data
        self.descricao = descricao


@bot.message_handler(commands=["role"])
def vamomarcar(mensagem):
    comando = mensagem.text.split()[1]
    msg = mensagem

    #marca um evento
    if(comando == "marcar"):
        msg = msg.text.replace("/role marcar ", "")
        nome, data, desc = msg.split(", ")

        listaRole = getListaRole()
        n_roles = len(listaRole)

        if(n_roles == 0):
            newrole = Evento(nome, data, desc)
            listaRole.append(newrole)
            setListaRole(listaRole)
            bot.reply_to(mensagem, "rolê marcado!")
        else:
            verifyer = 0
            for i in range(n_roles):
                if (listaRole[i].nome == nome):
                    bot.reply_to(mensagem, "rolê já existente! crie um outro rolê com outro nome, ou, se quiser,chame /role remarcar nomerolê")
                    verifyer+=1
                    break
            if verifyer == 0:
                newrole = Evento(nome, data, desc)
                listaRole.append(newrole)
                setListaRole(listaRole)
                bot.reply_to(mensagem, "rolê marcado!")
        
    #sobreescreve um evento
    elif(comando == "remarcar"):
        msg = msg.text.replace("/role remarcar ", "")
        nome, data, desc = msg.split(", ")

        listaRole = getListaRole()
        n_roles = len(listaRole)

        if(n_roles > 0):
            for i in range(n_roles):
                if (listaRole[i].nome == nome):

                    listaRole[i].nome = nome
                    listaRole[i].data = data
                    listaRole[i].descricao = desc
                    setListaRole(listaRole)
                    bot.reply_to(mensagem, "rolê remarcado!")

        else:
            bot.reply_to(mensagem, "rolê nem existe! cria ele ae meu")

    elif(comando == "desmarcar"):
        nome = msg.text.replace("/role desmarcar ", "")

        listaRole = getListaRole()
        n_roles = len(listaRole)

        verifyer = 0
        for i in range(n_roles):
            if (listaRole[i].nome == nome):
                listaRole[i]
                bot.reply_to(mensagem, "role desmarcado, os de vdd eu sei quem são, vlwflw")
                verifyer+=1
                break
        if verifyer == 0:
            bot.reply_to(mensagem, "não achei o role")

    #mostra eventos marcados
    elif(comando == "consultar"):
        listaRole = getListaRole()
        n_roles = len(listaRole)

        if(n_roles > 0):
            str_roles = ""
            for i in range(n_roles):
                str_roles += "  \n"+listaRole[i].nome + "  " + listaRole[i].data

            bot.reply_to(mensagem, "roles marcados:\n"+str_roles)
        else:
            bot.reply_to(mensagem, "não existem rolês marcados")

    #contagem regressiva para evento
    elif(comando == "countdown"):
        nome = msg.text.replace("/role countdown ", "")

        listaRole = getListaRole()
        n_roles = len(listaRole)

        if(n_roles > 0):
            for i in range(n_roles):
                if (listaRole[i].nome == nome):
                    format_string = "%d/%m/%Y %H:%M:%S"
                    data = datetime.strptime(listaRole[i].data, format_string)
                    bot.reply_to(mensagem, "It'll be in: "+str(data-datetime.now()))
                    break
        else:
            bot.reply_to(mensagem, "não achei esse role")
    


def getListaRole():
    if(exists("listaRoles")):
        with open("listaRoles", "rb") as arquivo:
            listaRolePickled = arquivo.read()
        listaRole = pickle.loads(listaRolePickled)
    else:
        listaRole = []

    return listaRole


def setListaRole(listaRole):
    listaRolePickled = pickle.dumps(listaRole)
    with open("listaRoles", "wb+") as arquivo:
        arquivo.write(listaRolePickled)


@bot.message_handler(commands=["ximira"])
def responder(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrm4r4Ow5mWUdGRPkMr-Sht1pknZ2ACCFwt8Mh7-hx0CULjSfFYxmkml5lpuzpk9o7nVg&usqp=CAU')


# ------------------------------------------------------------------
# comandos:

# listar todos os comandos aqui:
@bot.message_handler(commands=["help", "ajuda", "socorro"])
def ajudar(mensagem):
    bot.send_message(mensagem.chat.id, "Olá, eu sou o bot e esses são meus comandos:\n \
        /roll → /roll 1d20 = joga um dado de vinte lados \
        /role →\
        ")

# comando de jogar dados:


@bot.message_handler(commands=["roll"])
def joga_dados(mensagem):
    a, dados = mensagem.text.split(' ')
    quantdados, dado = dados.split('d')
    if int(quantdados) > 42:
        bot.reply_to(mensagem, "NÃO FODE")
    elif int(dado) > 100:
        bot.reply_to(mensagem, "Ta tentando compensar o que?")
    else:
        j = 0
        corda = "dados: "
        for x in range(int(quantdados)):
            a = (random.randint(1, (int(dado))))
            j += a
            corda += str(a)+' '
        bot.reply_to(mensagem, corda+"\n"+"Total: "+str(j))


# ------------------------------------------------------------------
# Reações passivas a coisas:

# sempre que alguem escreve 'o jogo' responde com um 'perdi':
@bot.message_handler(regexp="o jogo")
def ojogo(mensagem):
    bot.reply_to(mensagem, "perdi")

# 20% de chance de falar que o gp é gay ->piada interna do grupo<-


@bot.message_handler(regexp="gay")
def gpfullhomo(mensagem):
    x = random.randint(1, 10)
    if x < 2:
        bot.send_message(mensagem.chat.id, "nossa que grupo mais gay")
    else:
        pass

# 50% de chance de reclamar do danilo falando da multiplique ->piada interna do grupo<-


@bot.message_handler(regexp="Multi")
def antidanilo(mensagem):
    x = random.randint(1, 10)
    if x == 5:
        bot.reply_to(mensagem, "um dia Danilo, um dia")
    elif x == 4:
        bot.reply_to(mensagem, "PARA POR FAVOR")
    elif x < 3:
        bot.reply_to(mensagem, "ainda nisso")
    else:
        pass

# fala que dia da semana é


@bot.message_handler(regexp="semaninha filha da puta")
def semaninha(mensagem):
    date = datetime.now()
    x = date.weekday()
    if x == 0:
        dia = "segunda"
    elif x == 1:
        dia = "terça"
    elif x == 2:
        dia = "quarta"
    elif x == 3:
        dia = "quinta"
    if x < 4:
        bot.reply_to(mensagem, "capitão, ainda é "+dia)
    else:
        pass


bot.polling()
