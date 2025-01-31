from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Оформление заказа"),
     KeyboardButton(text="Информация о заказе")],
    [KeyboardButton(text="Связь с поддержкой"),
     KeyboardButton(text="Часто задаваемые вопросы")],
     [KeyboardButton(text="Отзывы"), KeyboardButton(text="Корзина")]
    , [KeyboardButton(text="Изменить адрес доставки")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите опцию"
)

make_order_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Найти товар", callback_data="find_product"),
     InlineKeyboardButton(text="Оформить заказ", callback_data="checkout_order")],
])
make_order_continue_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Продолжить оформление заказа", callback_data="make_order_continue")]
])

add_to_cart = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Добавить в корзину")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите опцию"
)

edit_personal_data_information = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить адрес доставки", callback_data="change_address")],
        [InlineKeyboardButton(text="Продолжить оформление заказа", callback_data="make_order_continue")],
    ]
)
choose_delivery_method = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Доставка курьером", callback_data="currier_delivery")],
        [InlineKeyboardButton(text="Доставка в постомат", callback_data="postomat_delivery")],
    ]
)
come_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Назад")]], resize_keyboard=True)


reviews = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оставить отзыв", callback_data="post_review"),
        InlineKeyboardButton(text="Посмотреть отзывы", callback_data="check_reviews")],
        [InlineKeyboardButton(text="Назад", callback_data="find_product")]
    ]
)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню поиска товара
find_product_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Нижнее белье", callback_data="category_underwear")],
    [InlineKeyboardButton(text="Купальники и пляжная одежда", callback_data="category_swimwear")],
    [InlineKeyboardButton(text="Женская одежда", callback_data="category_womenswear")],
    [InlineKeyboardButton(text="Мужская одежда", callback_data="category_menswear")],
    [InlineKeyboardButton(text="Женские аксессуары", callback_data="category_women_accessories")],
    [InlineKeyboardButton(text="Мужские аксессуары", callback_data="category_men_accessories")],
    [InlineKeyboardButton(text="Женская обувь", callback_data="category_women_shoes")],
    [InlineKeyboardButton(text="Мужская обувь", callback_data="category_men_shoes")],
    [InlineKeyboardButton(text="Поиск по названию", callback_data="search_by_name")],
])

womenwear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Платья", callback_data="category_women_dresses")],
    [InlineKeyboardButton(text="Юбки", callback_data="category_women_skirts")],
    [InlineKeyboardButton(text="Блузы и рубашки", callback_data="category_women_blouses")],
    [InlineKeyboardButton(text="Топы и майки", callback_data="category_women_tops")],
    [InlineKeyboardButton(text="Футболки и лонгсливы", callback_data="category_women_tshirts")],
    [InlineKeyboardButton(text="Свитеры и кардиганы", callback_data="category_women_sweaters")],
    [InlineKeyboardButton(text="Женские худи и толстовки", callback_data="category_women_hoodies")],
    [InlineKeyboardButton(text="Жакеты и пиджаки", callback_data="category_women_jackets")],
    [InlineKeyboardButton(text="Женские куртки и пальто", callback_data="category_women_coats")],
    [InlineKeyboardButton(text="Брюки и леггинсы", callback_data="category_women_trousers")],
    [InlineKeyboardButton(text="Женские джинсы", callback_data="category_women_jeans")],
    [InlineKeyboardButton(text="Женские шорты", callback_data="category_women_shorts")],
    [InlineKeyboardButton(text="Костюмы и комбинезоны", callback_data="category_women_suits")],
    [InlineKeyboardButton(text="Женская домашняя одежда", callback_data="category_women_homewear")],
    [InlineKeyboardButton(text="Женская спортивная одежда", callback_data="category_women_sportwear")],
    [InlineKeyboardButton(text="Женское нижнее белье", callback_data="category_women_underwear")],
    [InlineKeyboardButton(text="Купальники и пляжная одежда", callback_data="category_women_swimwear")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

menswear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Футболки и поло", callback_data="menswear_tshirts")],
    [InlineKeyboardButton(text="Рубашки", callback_data="menswear_shirts")],
    [InlineKeyboardButton(text="Свитеры и джемперы", callback_data="menswear_sweaters")],
    [InlineKeyboardButton(text="Худи и толстовки", callback_data="menswear_hoodies")],
    [InlineKeyboardButton(text="Пиджаки и жакеты", callback_data="menswear_jackets")],
    [InlineKeyboardButton(text="Куртки и пальто", callback_data="menswear_coats")],
    [InlineKeyboardButton(text="Брюки и чиносы", callback_data="menswear_trousers")],
    [InlineKeyboardButton(text="Джинсы", callback_data="menswear_jeans")],
    [InlineKeyboardButton(text="Шорты", callback_data="menswear_shorts")],
    [InlineKeyboardButton(text="Костюмы", callback_data="menswear_suits")],
    [InlineKeyboardButton(text="Спортивная одежда", callback_data="menswear_sportwear")],
    [InlineKeyboardButton(text="Домашняя одежда", callback_data="menswear_homewear")],
    [InlineKeyboardButton(text="Нижнее белье", callback_data="menswear_underwear")],
    [InlineKeyboardButton(text="Купальные шорты", callback_data="menswear_swimshorts")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

# Женские аксессуары
women_accessories_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сумки и клатчи", callback_data="women_acc_bags")],
    [InlineKeyboardButton(text="Ремни и пояса", callback_data="women_acc_belts")],
    [InlineKeyboardButton(text="Шарфы и платки", callback_data="women_acc_scarves")],
    [InlineKeyboardButton(text="Головные уборы", callback_data="women_acc_headwear")],
    [InlineKeyboardButton(text="Перчатки", callback_data="women_acc_gloves")],
    [InlineKeyboardButton(text="Украшения", callback_data="women_acc_jewelry")],
    [InlineKeyboardButton(text="Часы", callback_data="women_acc_watches")],
    [InlineKeyboardButton(text="Очки", callback_data="women_acc_glasses")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

# Мужские аксессуары
men_accessories_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ремни", callback_data="men_acc_belts")],
    [InlineKeyboardButton(text="Сумки и рюкзаки", callback_data="men_acc_bags")],
    [InlineKeyboardButton(text="Мужские головные уборы", callback_data="men_acc_headwear")],
    [InlineKeyboardButton(text="Шарфы", callback_data="men_acc_scarves")],
    [InlineKeyboardButton(text="Мужские перчатки", callback_data="men_acc_gloves")],
    [InlineKeyboardButton(text="Мужские часы", callback_data="men_acc_watches")],
    [InlineKeyboardButton(text="Мужские очки", callback_data="men_acc_glasses")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

# Женская обувь
women_shoes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Туфли и лодочки", callback_data="women_shoes_heels")],
    [InlineKeyboardButton(text="Ботильоны и сапоги", callback_data="women_shoes_boots")],
    [InlineKeyboardButton(text="Босоножки и сандалии", callback_data="women_shoes_sandals")],
    [InlineKeyboardButton(text="Кроссовки и кеды", callback_data="women_shoes_sneakers")],
    [InlineKeyboardButton(text="Шлепанцы и тапочки", callback_data="women_shoes_slippers")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

# Мужская обувь
men_shoes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Классическая обувь", callback_data="men_shoes_classic")],
    [InlineKeyboardButton(text="Мужские ботинки и сапоги", callback_data="men_shoes_boots")],
    [InlineKeyboardButton(text="Мужские кроссовки и кеды", callback_data="men_shoes_sneakers")],
    [InlineKeyboardButton(text="Мужские сандалии и шлепанцы", callback_data="men_shoes_sandals")],
    [InlineKeyboardButton(text="Мужская домашняя обувь", callback_data="men_shoes_slippers")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

# Универсальные категории
homewear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мужская домашняя одежда", callback_data="homewear_men")],
    [InlineKeyboardButton(text="Женская домашняя одежда", callback_data="homewear_women")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

sportwear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мужская спортивная одежда", callback_data="sportwear_men")],
    [InlineKeyboardButton(text="Женская спортивная одежда", callback_data="sportwear_women")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

underwear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мужское нижнее белье", callback_data="underwear_men")],
    [InlineKeyboardButton(text="Женское нижнее белье", callback_data="underwear_women")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])

swimwear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мужские купальные шорты", callback_data="swimwear_men")],
    [InlineKeyboardButton(text="Женские купальники и пляжная одежда", callback_data="swimwear_women")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_find_product")]
])
