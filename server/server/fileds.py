import peewee, base64, binascii
import decimal


nullrefs = (
    b'00000000000000000000000000000000',
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    'NO REF!',
)

class DateField(peewee.DateTimeField):

    def __init__(self, *args, **kwargs):
        if not kwargs.get('db_column'):
            kwargs['db_column'] = 'Дата'
        super().__init__(*args, **kwargs)

    def python_value(self, value):
        if value is None:
            return nulldate

        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

        return value.replace(year = value.year - 2000)

    def db_value(self, value):
        return value.replace(year = value.year + 2000)

    def timestamp(self):
        print(self._data)
        return 'AAA'

class BoolField(peewee.BooleanField):

    def __init__(self, *args, **kwargs):
        if kwargs.get('inverted') is not None:
            self.inverted = (kwargs.get('inverted') is True)
            del kwargs['inverted']

        super().__init__(*args, **kwargs)

    def python_value(self, value):
        if getattr(self, 'inverted', False):
            return True if value == b'\x00' else False
        else:
            return True if value == b'\x01' else False

    def db_value(self, value):
        if getattr(self, 'inverted', False):
            return 0x00 if value else 0x01
        else:
            return 0x01 if value else 0x00

class LinkField(peewee.BlobField):

    def __init__(self, *args, **kwargs):
        if not kwargs.get('primary_key'):
            kwargs['primary_key'] = True
        kwargs['db_column'] = 'Ссылка'
        super().__init__(*args, **kwargs)

    def python_value(self, value):
        if value in nullrefs or value is None:
            return None

        return base64.b16encode(value).decode()

    def db_value(self, value):
        if value in nullrefs or value is None:
            return None

        try:
            return base64.b16decode(value.encode())
        except binascii.Error as e:
            return value
        
        pass

class ForeignKey(LinkField, peewee.ForeignKeyField):

    def __init__(self, *args, **kwargs):
        peewee.ForeignKeyField.__init__(self, *args, **kwargs)

