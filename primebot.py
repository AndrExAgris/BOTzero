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

@bot.message_handler(regexp="testa 1")
def ojogo(mensagem):
    bot.reply_to(mensagem, "foi")



# ------------------------------------------------------------------
# comandos:

# listar todos os comandos aqui:
@bot.message_handler(commands=["help", "ajuda", "socorro"])
def guiadecomandos(mensagem):
    bot.send_message(mensagem.chat.id, "Olá, eu sou o bot e esses são meus comandos:\n \
        \n/roll → /roll 1d20 = joga um dado de vinte lados \
        \n/role → abre o guia de comando da agenda\
        ")


# comando de jogar dados:
@bot.message_handler(commands=["roll"])
def joga_dados(mensagem):
    try:
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
    except:
        bot.reply_to(mensagem, "Tenta digitar algo como '/roll 2d10'")


# Agenda de eventos
# Exemplos
# /role marcar ficar doidão na uni, 25/03/2022 22:00, trazer mt birita e droga
# /role remarcar ficar doidão na uni, 26/03/2022 22:00, trazer ainda mais birita e droga
# /role desmarcar ficar doidão na uni
# /role consultar
# /role falta_quanto ficar doidão na uni

@bot.message_handler(commands=["role"])
def vamomarcar(mensagem):
    
    try:
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

        #apaga um eveto
        elif(comando == "desmarcar"):
            nome = msg.text.replace("/role desmarcar ", "")

            listaRole = getListaRole()
            n_roles = len(listaRole)

            verifyer = 0
            nom =''
            dat =''
            desc =''
            for i in range(n_roles):
                if (listaRole[i].nome == nome):
                    listaRole.remove(listaRole[i])
                    setListaRole(listaRole)
                    bot.reply_to(mensagem, "role desmarcado, os de vdd eu sei quem são")
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
    
    except:
        bot.reply_to(mensagem, "Os comandos da agenda são:\n \
            \n/role marcar -> marca roles no formato '/role marcar nome do role, dd/mm/aaaa hh:mm:ss, descrição'\
            \n/role remarcar -> sobreescreve um role marcado(mesmo formato)\
            \n/role desmarcar -> desmarca um role pelo nome dele '/role desmarcar nome do role'\
            \n/role consultar -> mostra nome e data dos roles '/role consultar nome do role'\
            \n/role countdown -> quanto tempo flata pro role'/role countdown nome do role'")     

#funçoes e classes auxiliares para eventos
def getListaRole():
        if(exists("listaEventos")):
            with open("listaEventos", "rb") as arquivo:
                listaRolePickled = arquivo.read()
            listaRole = pickle.loads(listaRolePickled)
        else:
            listaRole = []

        return listaRole

def setListaRole(listaRole):
        listaRolePickled = pickle.dumps(listaRole)
        with open("listaEventos", "wb+") as arquivo:
            arquivo.write(listaRolePickled)
      
class Evento:
    def __init__(self, nome, data, descricao):
        self.nome = nome
        self.data = data
        self.descricao = descricao


# ------------------------------------------------------------------
# Reações passivas a coisas:

# sempre que alguem escreve 'o jogo' responde com um 'perdi':
@bot.message_handler(regexp="jogo")
def ojogo(mensagem):
    x = random.randint(1, 10)
    if x == 1:
        bot.reply_to(mensagem, "a rainha ainda não sabe desse jogo?")
    elif x < 4:
        bot.reply_to(mensagem, "perdi")
    elif x == 5:
        bot.reply_to(mensagem, "O JOGO?")
    else:
        pass
    
@bot.message_handler(regexp="perdi")
def perdiojogo(mensagem):
    x = random.randint(1, 10)
    if x < 2:
        bot.reply_to(mensagem, "perdi")
    elif x == 7:
        bot.reply_to(mensagem, "porra de jogo do caralho, perdi")
    else:
        pass


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

# fala que dia da semana é de segunda a quinta
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


#respostasa quem fala mal do bot
@bot.message_handler(regexp="bot lixo")
def votekik(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))

@bot.message_handler(regexp="bot cuzão")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))
    
@bot.message_handler(regexp="bot arrombado")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))
    
@bot.message_handler(regexp="bot pau no cu")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))
    
@bot.message_handler(regexp="bot escroto")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))
    
@bot.message_handler(regexp="vai tomar no cu bot")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))
    
@bot.message_handler(regexp="vai se fuder bot")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))

@bot.message_handler(regexp="me mama bot")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))
    
@bot.message_handler(regexp="bot viad")
def reference(mensagem):
    name = mensagem.from_user.first_name
    bot.reply_to(mensagem, 'Chamar alguem de viado é ofença agora?\n #Cancelem'+str(name)+' #PorUmMundoMelhor')

@bot.message_handler(regexp="bot de merda")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))
    
@bot.message_handler(regexp="bot filho da puta")
def reference(mensagem):
    name = mensagem.from_user.last_name
    bot.reply_to(mensagem, 'engraçado que a Sra. '+str(name)+ " disse ontem algo bem parecido na cama, e sobre voce haha")

@bot.message_handler(regexp="bot burr")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/votekick '+str(name))

@bot.message_handler(regexp="/votekick bot")
def reference(mensagem):
    name = mensagem.from_user.username
    bot.reply_to(mensagem, '/ban '+str(name))

@bot.message_handler(regexp="/ban bot")
def reference(mensagem):
    bot.reply_to(mensagem, 'só argumenta quem não se garante no soco, change my mind')



#------------------------------------------------------------------------------------
#Referencias...

#alabama reference
@bot.message_handler(regexp="incesto")
def sweethome(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://img.ifunny.co/images/1c31b0bfe979a8615bb903fdcf1943499fa836c1c47faf8b818aaaf968cb5932_1.jpg')
    
#reference reference
@bot.message_handler(regexp="motherfucking reference")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://img.ifunny.co/images/452cb7491692efa70102f59d186594a1d7e3c7264cc3047c14d01e686af8b487_1.jpg')
   
#reference reference
@bot.message_handler(regexp="motherfucking reference")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://img.ifunny.co/images/452cb7491692efa70102f59d186594a1d7e3c7264cc3047c14d01e686af8b487_1.jpg')

#deftpunk reference
@bot.message_handler(regexp="Discovery")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/newsfeed/001/446/714/e68.jpg')
    
#deftpunk reference
@bot.message_handler(regexp="Random Access Memories")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/newsfeed/001/446/714/e68.jpg')
    
#deftpunk reference
@bot.message_handler(regexp="Homework")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/newsfeed/001/446/714/e68.jpg')
    
#brasil reference
@bot.message_handler(regexp="Brasil")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/facebook/001/297/911/594.jpg')

#brasil reference
@bot.message_handler(regexp="inferno de lugar")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/facebook/001/297/911/594.jpg')
    
#brasil reference
@bot.message_handler(regexp="caipirinha")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/facebook/001/297/911/594.jpg')
    
#brasil reference
@bot.message_handler(regexp="carnaval")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/facebook/001/297/911/594.jpg')
    
#brasil reference
@bot.message_handler(regexp="feijoada")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/facebook/001/297/911/594.jpg')
    
#sexo reference
@bot.message_handler(regexp="sexo")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://pbs.twimg.com/media/ESDYelRXsAg8keJ.jpg')
    
#sexo reference
@bot.message_handler(regexp="transar")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://pbs.twimg.com/media/ESDYelRXsAg8keJ.jpg')
    
#sexo reference
@bot.message_handler(regexp="fornica")
def reference(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://pbs.twimg.com/media/ESDYelRXsAg8keJ.jpg')
    
#DO NADA reference
@bot.message_handler(regexp="0")
def reference(mensagem):
    x = random.randint(1, 100)
    if x == 42:
        bot.send_photo(mensagem.chat.id, 'https://i.kym-cdn.com/photos/images/facebook/001/228/805/6a9.jpg')

#aa reference
#@bot.message_handler(regexp="asojfbas´jdhnçl")
#def reference(mensagem):
#    bot.send_photo(mensagem.chat.id, 'a')
    
#aaa reference
#@bot.message_handler(regexp="alsjdhóajsdh")
#def reference(mensagem):
#    bot.send_photo(mensagem.chat.id, 'a')
    
#aaa reference
#@bot.message_handler(regexp="ápsihfápsiohfóih")
#def reference(mensagem):
#    bot.send_photo(mensagem.chat.id, 'a')



#bot.polling()
bot.infinity_polling(timeout=10, long_polling_timeout = 5)

    