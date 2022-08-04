from utils import *

vk_token = 'vk1.a.DoA8kCkegyHxWMrjvrng6VBbrz0ao4TB3VAjfgYpz_SmUov2U7i1sdXtJ2xfbQA4UWzc1RrPXUmIj63DMN6WjwGR7hEtPVj6JMp5Atm8bs5LWIQfj4n6QXm5lRJCR1PJZaBcCL8uTotJ-aYoVIj6HqqzfxuBRNktL5V5MPwqKn8D3bVfdihqLqGqI0blR7e7'
tg_token = ''

vk_admins_ids = []
tg_admins_ids = []

clear_vk_key = get_vk_keyboard([])
back_vk_key = get_vk_keyboard([[('Назад', 'синий')]])
cart_vk_key = get_vk_keyboard([[('Назад', 'синий'), ('Заказать', 'зеленый')]])
menu_vk_keyboard = get_vk_keyboard([
	[('Поиск', 'синий'), ('Категории', 'зеленый'), ('Корзина', 'синий')]
])

user_vk_function = vk_addition
