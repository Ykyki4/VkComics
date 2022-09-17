# VkComics

## Установка

Дабы установить скрипт, следует установить [Python3](https://dvmn.org/encyclopedia/what-you-need-to-know/python_basics_install_python/), затем прописать эту комманду в терминал, чтобы установить все зависимые пакеты проекта:

```pip install -r requirements.txt```

Также вам нужно установить эти переменные окружения:
* CLIENT_ID - ид вашего приложения в вк.
* VK_ACCESS_TOKEN - токен доступа к вашему аккаунту.

Всё это вы можете получить на сайте [разработчиков вк](https://vk.com/dev)

Переменные устанавливаются по пакету [environs](https://pypi.org/project/environs/), вам нужно создать файл ```.env``` в папке со скриптом, и установить все переменные в формате ```ПЕРЕМЕННАЯ=значение```.

## Что делает скрипт?

Данный скрипт используется для автоматического размещения комиксов автора [xkcd](https://xkcd.com/) в вашу группу вконтакте.

Для запуска скрипта, используйте команду:

```python vkcomics.py```

### Функции скрипта:

#### get_image_url:
Принимает в себя ссылку на информацию о рандомном комиксе в формате json, делает запрос, и возвращает её.

#### request_upload_url:
Принимает в себя ссылку на метод api вк, который возвращает ссылку принадлежащую владельцу access_token-a, с помощью которой можно разместить данные на сервер вк, и возвращает её.

#### post_image_to_server:
Принимает в себя ссылку на картинку комикса, скачивает её в папку images(если её ещё не было), делает запрос на ссылку полученную в прошлой функции с картинкой комикса, загружает картинку на сервер вк, удаляет картинку, и возвращает ответ полученный с запроса.

#### post_image_to_album:
Принимает в себя ответ предыдущей функции, делает запрос на ссылку метода photos.saveWallPhoto с ответом полученным в предыдущей функции, и загружает картинку в альбом, после чего возвращает полученный ответ.

#### post_image_to_wall:
Принимает в себя ответ предыдущей функции, делает запрос на ссылку метода wall.post с ответом полученным в предыдущей функции, и загружает картинку на стену, вместе с комментарием автора комикса.
