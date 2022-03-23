from datetime import datetime

class Role:
    def __init__(self, nome, data, descricao):
        self.nome = nome
        self.data = data
        self.descricao = descricao

therole = Role("sextou na frente da uni", "31/03/2022 00:00:00" , "quem n ficar loco apanha")

print(therole.nome)



format_string = "%d/%m/%Y %H:%M:%S"


data = datetime.strptime(therole.data, format_string)
print(data)

print("It'll be in: "+str(data-datetime.now()))