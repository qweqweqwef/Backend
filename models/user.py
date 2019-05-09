from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True)
    password = pw.CharField(index=True)
    email = pw.CharField(unique=True,index=True)
    

    def as_dict(self):
        json_obj = {
            'id' : self.id,
            'username':self.username,
            'email' : self.email,
             
        }

        return json_obj

