#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

from peewee import *


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase('tracked_products.sqlite', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    title = TextField()
    url = TextField(unique=True)

    def get_last_price(self):
        last_price = self.prices.order_by(Price.date.desc()).first()
        if not last_price:
            return

        return last_price.value

    def append_price(self, value):
        Price.create(product=self, value=value)

    def __str__(self):
        return f'Product(title={repr(self.title)}, last_price={self.get_last_price()}, url={repr(self.url)})'


class Price(BaseModel):
    value = DecimalField(null=True)
    date = DateField(default=DT.datetime.now)
    product = ForeignKeyField(Product, backref='prices')

    class Meta:
        indexes = (
            (("product_id", "date"), True),
        )

    def __str__(self):
        return f'Price(value={self.value}, date={self.date}, product_id={self.product.id})'


db.connect()
db.create_tables([Product, Price])


if __name__ == '__main__':
    for product in Product.select():
        print(product)

        for p in product.prices.select():
            print('   ', p)

        print()