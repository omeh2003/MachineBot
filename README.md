Telegram Бот для Управления Доступом
Этот Telegram-бот предназначен для управления доступом к функциям бота. Он позволяет администратору добавлять, просматривать и удалять пользователей, которые имеют доступ к боту.

Основные возможности
Добавление пользователя: 
администратор может ввести идентификатор пользователя, которому нужно предоставить доступ к боту. Для этого предоставляется пользовательская клавиатура с числами от 0 до 9, кнопками "Сброс" и "Отправить". Пользовательский идентификатор должен состоять из цифр. Нажатие на кнопку "Сброс" очищает текущий ввод идентификатора, а нажатие на кнопку "Отправить" добавляет пользователя в список разрешенных.

Просмотр списка пользователей: 
администратор может просмотреть список пользователей, которым был предоставлен доступ к боту. В этом списке отображаются идентификаторы пользователей, каждый из которых сопровождается кнопкой для удаления пользователя из списка.
Удаление пользователя: 
администратор может удалить пользователя из списка разрешенных, нажав на кнопку удаления рядом с идентификатором пользователя. Администратор не может удалить себя из списка разрешенных.

Ограничения
Пользователи, которые не были добавлены в список разрешенных администратором, не могут взаимодействовать с ботом.
Бот использует идентификаторы пользователей Telegram для управления доступом.
Бот не предоставляет функциональность для аутентификации администратора или механизм для изменения администратора. Администратор должен быть задан в коде бота.

Использование
Запустите бота, используя ваш API-токен Telegram.
Отправьте команду /start от имени администратора.
Выберите действие (добавить пользователя, просмотреть список пользователей) в меню настроек.
Добавляйте, просматривайте и удаляйте пользователей согласно инструкциям на экране.

Конфигурация
Для настройки бота, замените 'YOUR_TELEGRAM_API_TOKEN' на ваш действительный токен API в коде
