from models.base_model import BaseModel
import peewee as pw
from app import app
from models.user import User

class Blog(BaseModel):
    parent_user = pw.ForeignKeyField(User , backref='blogs',unique=False)
    d = pw.TextField(unique=False)
    title = pw.CharField(unique=False)

    def as_dict(self):
        json_obj = {
            "parent_user" : self.parent_user,
            "title" : self.title,
            'id' : self.id,
            'd' : self.d
        }

        return json_obj