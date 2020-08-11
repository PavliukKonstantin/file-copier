# File-Copier

Проба пера на найденном в интернете тестовом задании.

Задание:
На Python реализовать программу, осуществляющую копирование файлов в соответствии с конфигурационным файлом.
Конфигурационный файл должен иметь формат xml.
Для каждого файла в конфигурационном файле должно быть указано его имя, исходный путь и путь, по которому файл требуется скопировать.


Инструкция по запуску:

1) Для того, чтобы каталог виртуального окружения .venv при установке зависимостей создался в корне проекта необходимо ввести команду (poetry соответственно должен быть установлен в системе):

        $ poetry config virtualenvs.in-project true

    Необязательное действие. Это для тех кому как и мне не нравится, что виртуальное окружение создается не пойми где и с каким попало именем.

2) Для установки виртуального окружения и зависимостей запустить:

        $ poetry install

3) Файл конфигурации должен иметь структуру:

        <?xml version="1.0"?>
        <files>
            <file>
                <name>file_one.txt</name>
                <source_path>path_to_source_directory</source_path>
                <destination_path>path_to_destination_directory</destination_path>
            </file>

            <file>
                <name>file_two.txt</name>
                <source_path>path_to_source_directory</source_path>
                <destination_path>path_to_destination_directory</destination_path>
            </file>
        </files>

4) Тесты написаны на _pytest_. Для запуска всех тестов необходимо в терминале выполнить команду:

         $ pytest
