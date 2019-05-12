from models.base_model import BaseModel
import peewee as pw
from models.user import User
from app import app

class Blog(BaseModel):
    parent_user = pw.ForeignKeyField(User , backref='blogs',unique=False)
    title = pw.CharField(unique=False)
    desc = pw.TextField(unique=False)

    def as_dict(self):
        json_obj = {
            'id' : self.id,
            "parent_user" : self.parent_user.username,
            "title" : self.title,
            'desc' : self.desc
        }

        return json_obj