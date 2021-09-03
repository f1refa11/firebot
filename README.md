﻿# FireBot

FireBot - бот, созданный мной на языке программирования Python для моего Discord Сервера, посвящённого мной, FireFall Void.

# Модифицирование и компилирование исходного кода

Лицензия, выбранная для этого проекта, даёт право кому-угодно 

Если вы хотите модифицировать исходный код бота, то вы должны учесть наличие на компьютере, на котором хотите изменять в дальнейшем код, следующие программы:
1. Python версии 3.7.9 или более;
2. Любой текстовый редактор с поддержкой подсветки синтаксиса.
Затем, когда вы правильно установили Python подходящей версии, откройте командную строку любым способом и введите следующую команду: pip install discord.py, youtube-dl.

**ВАЖНО!** Чтобы ваш бот работал, вам надо в файле config вставить токен вашего бота.

Теперь вы можете редактировать текст любым удобным способом.

Если вы хотите скомпилировать изменённый код, вам надо выполнить следующую команду в командной строке: pip install pyinstaller.

Затем, вам надо переместиться в командной строке в папку с вашим ботом и выполнить там команду "pyinstaller -F --windowed main.py"(main.py это основной файл с вашим скриптом). У вас должна появиться папка dist, где находится приложение с расширением .exe . Это и есть ваш код.
