import random

class Token:
    def generate_token(self, request):
        token = ""
        #ID Number
        token += str(random.randint(100, 300))
        token += request.POST['role'][:4]
        token += request.POST['sector'][:4]
        token += str(random.randint(500, 800))
        token += request.POST['name'][:4]

        return token
    
    def validate_token(self, token):
        id_number = int(token[:3])
        role = token[3:7]
        sector = token[7:11]
        noise = int(token[11:14])
        name = token[14:18]
        if id_number >= 100 and id_number < 300:
            if role == "GERE" or role=="ASSE" or role=="CONS" or role=="DIRE" or role=="PRES" or role=="TRAI":
                if sector=="CIVI" or sector=="TECN" or sector=="COME" or sector=="RECU" or sector=="ADMN" or sector=="EXEC":
                    if noise >= 500 and noise < 800:
                        if len(token) == 18:
                            return True
        
        return False



