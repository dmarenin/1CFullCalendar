import peewee_mssql
import peewee
from server.conf import *
from server.fileds import *


class BaseModel(peewee.Model):

    class Meta:
        database = peewee_mssql.MssqlDatabase(SQL_BASE, host = SQL_HOST, user = SQL_USER, password = SQL_PASS, appname = "ORM Python Module")
        
        primary_key = False

class Task(BaseModel):
    title = peewee.CharField(db_column = 'Наименование')
    description = peewee.CharField(db_column = 'Наименование')
    start = DateField(db_column = 'ДатаНачала')
    end = DateField(db_column = 'ПлановаяДатаВыполнения')
    #end = peewee.DateTimeField(db_column = 'ПлановаяДатаВыполнения')
    complete = BoolField(db_column = 'Выполнена')
    employee = LinkField(db_column = 'Сотрудник')

    #db = peewee.CharField(db_column = 'db')
    #source = CharField(db_column = 'source')
    #srvr = CharField(db_column = 'srvr')

    class Meta:
        db_table = 't_ЗаписьНаСервис'

