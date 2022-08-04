from peewee import *


db = SqliteDatabase('data.db')


class BaseUser(Model):
	class Meta:
		database = db
	mode = CharField(max_length=50)


class VkUser(BaseUser):
	class Meta:
		db_table = 'VkUsers'
	vk_id = IntegerField(unique=True)

	def get_vk_name(self, vk_session):
		return vk_session.method('users.get', {'user_ids': self.vk_id})[0]['first_name']


class TgUser(BaseUser):
	class Meta:
		db_table = 'TgUsers'
	vk_id = IntegerField(unique=True)


class BaseOrder(Model):
	class Meta:
		database = db

	place_x = FloatField()
	place_y = FloatField()
	price = FloatField()


class Category(Model):
	class Meta:
		database = db
		db_table = 'Categories'

	name = CharField(max_length=100, unique=True)


class Product(Model):
	class Meta:
		database = db
		db_table = 'Products'

	name = CharField(max_length=250, unique=True)
	photo_path = CharField(max_length=150)
	price = FloatField()
	count = IntegerField()
	category = ForeignKeyField(Category)


class VkOrder(BaseOrder):
	class Meta:
		db_table = 'VkOrders'
	user = ForeignKeyField(VkUser)
	product = ForeignKeyField(Product)


class TgOrder(BaseOrder):
	class Meta:
		db_table = 'TgOrders'
	user = ForeignKeyField(TgUser)
	product = ForeignKeyField(Product)


if __name__ == '__main__':
	db.create_tables([VkUser, VkOrder, TgUser, TgOrder, Product, Category])
