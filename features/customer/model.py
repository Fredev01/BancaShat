from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from features import db


class Customer(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
    address = Column(String(255))

    def get_data(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'phone':self.phone,
            'address':self.address
        }

