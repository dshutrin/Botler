import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from models import *
import settings


class MyLongPoll(VkLongPoll):
	def listen(self):
		while True:
			try:
				for event in self.check():
					yield event
			except Exception as e:
				print(e)


class VkBot:
	def __init__(self):
		self.vk_session = vk_api.VkApi(token=settings.vk_token)
		self.longpoll = MyLongPoll(self.vk_session)

	def sender(self, user_id, msg, key=None):
		if key:
			self.vk_session.method('messages.send',
				{'user_id': user_id, 'message': msg, 'random_id': 0, 'keyboard': key})
		else:
			self.vk_session.method('messages.send',
				{'user_id': user_id, 'message': msg, 'random_id': 0})

	@staticmethod
	def get_vk_user(user_id):
		try:
			return VkUser().get(vk_id=user_id)
		except Exception as e:
			VkUser(
				vk_id=user_id,
				mode='start'
			).save()
			vk_user = VkUser().get(vk_id=user_id)
		return vk_user

	def start(self):
		for event in self.longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW:
				if event.to_me and not event.from_me:

					vk_user = self.get_vk_user(event.user_id)
					msg = event.text.lower()

					if msg == 'начать':
						self.sender(
							vk_user.vk_id,
							f'Привет {vk_user.get_vk_name(self.vk_session)}!\nТы находишься в меню, \
							можешь выбрать любое из предложенных действий!'.replace('\t', ''),
							settings.menu_vk_keyboard
						)
						vk_user.mode = 'menu'

					else:

						if vk_user.mode == 'menu':
							"""Обработка действий в меню"""
							if msg == 'поиск':
								self.sender(vk_user.vk_id, 'Введите запрос для поиска', settings.back_vk_key)
								vk_user.mode = 'find'

							if msg == 'категории':
								cats = [cat.name for cat in Category().select()]
								answer = 'Доступные категории товаров:\n'
								for i in range(len(cats)):
									answer = f'{answer}\n{i+1}) {cats[i]}'
								answer += '\nВведите номер категории, продукты которой вы хотите увидеть'
								self.sender(vk_user.vk_id, answer, settings.back_vk_key)
								vk_user.mode = 'categories'

							if msg == 'корзина':
								user_cart = [
									order.product.name for order in
									VkOrder().select().where(VkOrder().user_id == vk_user.id)
								]
								user_cart_str = "\n".join(user_cart)
								if len(user_cart) > 0:
									self.sender(
										vk_user.vk_id,
										f'Товары в вашей корзине:\n{user_cart_str}',
										settings.cart_vk_key
									)
									vk_user.mode = 'cart'
								else:
									self.sender(
										vk_user.vk_id,
										f'Ваша корзина пуста!',
										settings.menu_vk_keyboard
									)

						elif vk_user.mode == 'categories':
							"""Обработка действий в меню выбора категории товара"""
							if msg == 'назад':
								self.sender(
									vk_user.vk_id,
									f'Привет {vk_user.get_vk_name(self.vk_session)}!\nТы находишься в меню, \
															можешь выбрать любое из предложенных действий!'.replace(
										'\t', ''),
									settings.menu_vk_keyboard
								)
								vk_user.mode = 'menu'

							elif msg.isdigit() and (len([cat.name for cat in Category().select()]) >= int(msg) > 0):
								"""Обработка выбора категории"""
								pass

						elif vk_user.mode == 'cart':
							"""Обработка действий в корзине"""
							if msg == 'назад':
								self.sender(
									vk_user.vk_id,
									f'Привет {vk_user.get_vk_name(self.vk_session)}!\nТы находишься в меню, \
															можешь выбрать любое из предложенных действий!'.replace(
										'\t', ''),
									settings.menu_vk_keyboard
								)
								vk_user.mode = 'menu'

						elif vk_user.mode == 'find':
							"""Обработка действий в поиске"""
							if msg == 'назад':
								self.sender(
									vk_user.vk_id,
									f'Привет {vk_user.get_vk_name(self.vk_session)}!\nТы находишься в меню, \
															можешь выбрать любое из предложенных действий!'.replace(
										'\t', ''),
									settings.menu_vk_keyboard
								)
								vk_user.mode = 'menu'

						settings.user_vk_function(self.vk_session, vk_user, event)

					vk_user.save()


if __name__ == '__main__':
	VkBot().start()
