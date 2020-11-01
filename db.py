from peewee import *


db = SqliteDatabase('db.db')

class BaseModel(Model):
    class Meta:
        database = db

class DutyCycle(BaseModel):
    id = IntegerField(unique=True)
    cycle = IntegerField()

    @classmethod
    def get_cycle(self):
        return DutyCycle.select().order_by(DutyCycle.id.desc()).get().cycle

    @classmethod
    def set_cycle(self, cycle: int):
        DutyCycle.create(cycle=cycle)

db.connect()
if __name__ == '__main__':
    db.create_tables([DutyCycle])

