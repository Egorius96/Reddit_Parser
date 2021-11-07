# Reddit_Parser
iTechArt_Lab_Task1

Написать Python-скрипт с использованием библиотеки Beautiful Soup по сбору данных с сайта www.reddit.com по постам в категории Top -> This Month . Результат построчно (одна строка = один пост) сложить в текстовый файл с именем reddit-YYYYMMDDHHMM.txt в следующем формате:

UNIQUE_ID;post URL;username;user karma;user cake day;post karma;comment karma;post date;number of comments;number of votes;post category

UNIQUE_ID - буквенно-цифровой уникальный цифровой идентификатор записи длиной 32 символа, формируется при помощи функции uuid1() библиотеки uuid с параметром hex.

Содержимое выходного файла должно формироваться на момент запуска программы за один раз. В имени выходного файла: YYYY - год, например, 2020; MM - месяц, 12; DD - день; HH - часы; mm - минуты. В случае наличия файла reddit-YYYYMMDDHHmm.txt , содержимое существующего файла удаляется, файл формируется заново.

Выходной файл должен содержать 100 записей заданного формата. В случае, если по причине ограничений reddit.com по конкретному посту не удается собрать данные в нужном формате и полном объеме - пост игнорируется.

Скрипт должен логгировать все значимые события с использованием стандартной библиотеки logging.

Возможные ограничения reddit.com:

1) пост размещен, а пользователь, разместивший его, удален (пользователя больше не существует)
2) контент страницы недоступен без подтверждения возраста