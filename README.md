# Приложение для трансформирования координат
### Автор Абрамов А.О.
## Системные требования
Для работы приложения требуется Python версии 3.9.7 (минимум 3.9+, для установки pyproj нужной версии)
## Установка пакетов
Перед использованием приложения создать виртуальное окружение с помощью библиотеки virtualenv (гайд по установке https://virtualenv.pypa.io/en/latest/installation.html)
* Переходим в директорию с исходным кодом
* Создаем окружение venv `virtualenv venv`
* Активируем окружение (слева командной строки появится префикс (venv))
  * Для ОС Linux `source venv/bin/activate`
  * Для ОС Windows `venv/Scripts/activate`
* Устанавливаем пакеты с помощью pip `pip install -r requirements.txt`

Для деактивации окружения достаточно написать `deactivate`
## Запуск приложения
* Переходим в директорию с исходным кодом
* В конфигурационном файле _config.yaml_ выбираем порт, на котором стартует сервер
* Активируем окружение (слева командной строки появится префикс (venv))
  * Для ОС Linux `source venv/bin/activate`
  * Для ОС Windows `venv/Scripts/activate`
* Запуск приложения `python main.py`