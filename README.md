# **Reddit_Parser (+ RESTful server)**
Reddit_Parser collects information about users and posts from site www.reddit.com and sends
the data by POST requests to a RESTful server, where the information is processed and stored
in an output file in JSON format.

## Installation:
```
- Install Python 3.9
- Download chromedriver for your chrome version and operating system version at:
https://chromedriver.storage.googleapis.com/index.html
- Unpack chromedriver to the root folder of the script
- git clone https://github.com/Egorius96/Reddit_Parser.git
```

## Preparing to launch app:
```
- virtualenv venv
- sourse vemv/bin/activate
- pip install -r requirements.txt
```

## Using optional arguments:
```
-h, --help     Show this help message and exit
-p, --posts    Enter the number of posts (default 100)
-n, --name     Enter the file name (default YYYYMMDDHHmm.txt)

EXAMPLE:
python reddit_parser.py -p 25 -n 123.txt
```

## Using RESTful api:
```
Using Postman, it is possible to add, delete, modify and receive
data from the output file with data by the UNIQUE_ID key
(The conditions of this task can be found below in iTechArt_Lab_Task2)

Example of a GET request:
URL - http://localhost:8087/posts/

Example of a POST request:
URL - http://localhost:8087/posts/
row - {"UNIQUE_ID": "0a8df849514311ecba36a8a1594f557d", "post URL": "https://www.reddit.com/r/MadeMeSmile/comments/qkq3a2/my_kid_was_a_little_sad_after_not_seeing_any/", "username": "Atillion", "number of comments": "1.3k", "number of votes": "180k", "post category": "MadeMeSmile", "post date": "2021 11 01", "post karma": "57 694", "comment karma": "90 888", "user cake day": "Sat Oct 31 05:41:00 2015"}

Example of a DELETE request:
URL - http://localhost:8087/{UNIQUE_ID}

Example of a PUT request:
URL - http://localhost:8087/{UNIQUE_ID}
row - {Replacement data in JSON format}
```

### iTechArt_Lab_Task1
```
Написать Python-скрипт с использованием библиотеки Beautiful Soup по сбору данных с сайта www.reddit.com
по постам в категории Top -> This Month . Результат построчно (одна строка = один пост) сложить в
текстовый файл с именем reddit-YYYYMMDDHHMM.txt в следующем формате:

UNIQUE_ID;post URL;username;user karma;user cake day;post karma;comment karma;
post date;number of comments;number of votes;post category

UNIQUE_ID - буквенно-цифровой уникальный цифровой идентификатор записи длиной 32 символа, формируется при
помощи функции uuid1() библиотеки uuid с параметром hex.

Содержимое выходного файла должно формироваться на момент запуска программы за один раз. В имени выходного
файла: YYYY - год, например, 2020; MM - месяц, 12; DD - день; HH - часы; mm - минуты. В случае наличия
файла reddit-YYYYMMDDHHmm.txt , содержимое существующего файла удаляется, файл формируется заново.

Выходной файл должен содержать 100 записей заданного формата. В случае, если по причине ограничений reddit
по конкретному посту не удается собрать данные в нужном формате и полном объеме - пост игнорируется.

Скрипт должен логгировать все значимые события с использованием стандартной библиотеки logging.

Возможные ограничения reddit.com:

1) пост размещен, а пользователь, разместивший его, удален (пользователя больше не существует)
2) контент страницы недоступен без подтверждения возраста
```

### iTechArt_Lab_Task2
```
Приложение из задания 1  изменить таким образом, чтобы данные парсера сохранялись не напрямую в файл,
а через отдельный RESTful сервис, доступный на http://localhost:8087/, который в свою очередь
предоставляет простой API по работе с базовыми операциями по работе с файлом. Сервис сохраняет результат
в текстовый файл с именем reddit-YYYYMMDD.txt


Список методов и endpoits сервиса:

1. GET http://localhost:8087/posts/ возвращает содержимое всего файла в JSON формате
2. GET http://localhost:8087/posts/<UNIQUE_ID>/ возвращает содержимое строки с идентификатором UNIQUE_ID
3. POST http://localhost:8087/posts/ добавляет новую строку в файл, при отсутствии файла - создает новый,
   проверяет содержимое файла на отсутствие дубликатов по полю UNIQUE_ID перед созданием строки, в случае
   успеха возвращает код операции 201, а так же JSON формата {""UNIQUE_ID"": номер вставленной строки}
4. DELETE http://localhost:8087/posts/UNIQUE_ID/ удаляет строку файла с идентификатором UNIQUE_ID
5. PUT http://localhost:8087/posts/UNIQUE_ID/ изменяет содержимое строки файла с идентификатором UNIQUE_ID

Если не указано иное, все запросы возвращают код 200 в случае успеха;
те, что ссылаются на номер строки, возвращают 404, если строка с запрашиваемым номером не найдена.
Если не указано иное, содержимое ответа пусто.
Все непустые ответы - в формате JSON. Все действия, выполняющие запрос - в формате JSON.

Для реализации сервера использовать средства стандартной библиотеки Python.
Не использовать сторонние библиотеки и фреймворки.
```