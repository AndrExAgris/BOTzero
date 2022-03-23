import telebot
import random
from datetime import datetime

#pegando chave API do do documento de texto api_key
with open ("api_key", "r") as arquivo:
    APIkey = arquivo.read()
bot = telebot.TeleBot(APIkey)

#listar todos os comandos aqui:
@bot.message_handler(commands=["help", "ajuda", "socorro"])
def ajudar(mensagem):
    bot.send_message(mensagem.chat.id,"Olá, eu sou o bot e esses são meus comandos:\n \
        /roll → /roll 1d20 = joga um dado de vinte lados \
        ")


@bot.message_handler(commands=["vamo_marcar"])
def responder(mensagem):
    bot.send_photo(mensagem.chat.id, "")



#teste de envio de imagem 
@bot.message_handler(commands=["ximira"])
def responder(mensagem):
    bot.send_photo(mensagem.chat.id, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrm4r4Ow5mWUdGRPkMr-Sht1pknZ2ACCFwt8Mh7-hx0CULjSfFYxmkml5lpuzpk9o7nVg&usqp=CAU')
    

#comandos:

#comando de jogar dados:
@bot.message_handler(commands=["roll"])
def joga_dados(mensagem):
    a,dados = mensagem.text.split(' ')
    quantdados, dado = dados.split('d')
    if int(quantdados)>42:
        bot.reply_to(mensagem, "NÃO FODE")
    elif int(dado)>100:
        bot.reply_to(mensagem, "Ta tentando compensar o que?")
    else:
        j=0
        corda = "dados: "
        for x in range(int(quantdados)):
            a = (random.randint(1, (int(dado))))
            j+= a
            corda+= str(a)+' '
        bot.reply_to(mensagem, corda+"\n"+"Total: "+str(j))


#Reações passivas a coisas:

#sempre que alguem escreve 'o jogo' responde com um 'perdi':
@bot.message_handler(regexp="o jogo")
def ojogo(mensagem):
    bot.reply_to(mensagem, "perdi")

#20% de chance de falar que o gp é gay ->piada interna do grupo<- 
@bot.message_handler(regexp="gay")
def gpfullhomo(mensagem):
    x=random.randint(1, 10)
    if x < 2:
        bot.send_message(mensagem.chat.id, "nossa que grupo mais gay")
    else:
        pass

#50% de chance de reclamar do danilo falando da multiplique ->piada interna do grupo<- 
@bot.message_handler(regexp="Multi")
def antidanilo(mensagem):
    x=random.randint(1, 10)
    if x == 5:
        bot.reply_to(mensagem, "um dia Danilo, um dia")
    elif x == 4:
        bot.reply_to(mensagem, "PARA POR FAVOR")
    elif x < 3:
        bot.reply_to(mensagem, "ainda nisso")
    else: pass

#fala que dia da semana é
@bot.message_handler(regexp="semaninha filha da puta")
def semaninha(mensagem):
    date = datetime.now()
    x= date.weekday()
    if x == 0: dia = "segunda"
    elif x == 1: dia = "terça"
    elif x == 2: dia = "quarta"
    elif x == 3: dia = "quinta"
    if x<4 : 
        bot.reply_to(mensagem, "capitão, ainda é "+dia) 
    else: pass      


    
bot.polling()