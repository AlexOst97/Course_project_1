# Приложение для анализа транзакций, которые находятся в Excel-файле

## Цель проекта:

Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.

## Инструкция по установке:

1. Клонировать с GitHab (*git clone https://github.com/AlexOst97/Course_project_1*)
2. Установить зависимости (*pip install -r requirements.txt*)

## Функциональность проекта

- Модуль **views.py**: основные функции для генерации JSON-ответов из модуля *utils.py* по заданной дате;
- Модуль **utils.py**: набор функций, отвечающих за операции по каждой карте, топ-5 транзакций по сумме платежа, курс валют, стоимость акций из S&P500;
- Модуль **services.py**: набор функций для анализа выгодности категорий повышенного кешбэка;
- Модуль **reports.py**: набор функций трат по категориям.

## Тестирование проекта

Тестирование функций проекта осуществляется с помощью фреймворка pytest и метрики code coverage.

*Покрытие всех тестов - 93%*

## Команда проекта:

- Останин Александр (*aostanin97@gmail.com*) - **backend developer** 

## Источники

Программа создана при поддержке онлайн-школы
![Программа создана при поддержке онлайн-школы](https://digital-academy.ru/foto/school/skypro-2.png)