from datetime import datetime
from sqlalchemy import event
from models import Product, Brand, Category


# Definire le funzioni di callback
def before_insert(mapper, connection, target):
    print(f"Before Insert: {target}")


def before_update(mapper, connection, target):
    print(f"Before Update: {target}")
    if hasattr(target, 'updated_at'):
        target.updated_at = datetime.now()


def before_delete(mapper, connection, target):
    print(f"Before Delete: {target}")


# Collegare le funzioni di callback agli eventi
event.listen(Product, 'before_insert', before_insert)
event.listen(Product, 'before_update', before_update)
event.listen(Product, 'before_delete', before_delete)
