<h1 align="center">Лабораторная №2 по дисциплине "Технологии программирования"</h1>

## Изучение фреймворка MVC

### Цели:
1. Познакомиться c моделью MVC, ее сущностью и основными фреймворками на ее основе.
2. Разобраться с сущностями «модель», «контроллер», «представление», их функциональным
назначением.
3. Получить навыки разработки веб-приложений с использованием MVC-фреймворков.

### Постановка задачи:
1. Выберите для Вашего проекта тип лицензии и добавьте файл с лицензией в проект.
2. Доработайте проект магазина, добавив в него новую функциональность и информацию в базу
данных в соответствии с типом магазина (согласно индивидуальному варианту, см. таблицу). Составьте
модульные тесты к проекту, постарайтесь покрыть тестами максимально возможный объем кода. Для
работы с этим заданием создайте новую ветку кода на основе главной и фиксируйте в нее весь
программный код в процессе разработки. Добейтесь выполнения всех тестов проекта, после чего
объедините текущую ветку кода с главной.
3. Проанализируйте полученные результаты и сделайте выводы.

### Краткое описание проекта:
Проект представляет собой веб-приложение для интернет-магазина, где пользователи могут просматривать товары и совершать покупки с возможностью накопительной скидки. Приложение построено с использованием MVT (Model-View-Template) архитектуры, типичной для Django, которая позволяет отделить бизнес-логику от пользовательского интерфейса и обеспечивать эффективное управление данными.

### Индивидуальное задание:

<h1 align="center">4 вариант</h1>

<p>**Тип магазина:** Магазин товаров для быта</p> 
**Функциональность приложения:** Магазин должен вести учет покупателей и делать накопительную скидку. Величина скидки зависит от количества покупок любых товаров.

**Было разработано:**
* 3 модели: 
<p>Customer – модель для хранения информации о пользователе (имя, электронная почта, количество покупок).</p>
<p>Product – модель для представления информации о товаре (название, цена).</p>
<p>Purchase – модель для записи информации о каждой покупке (товар, покупатель, дата, адрес и итоговая цена с учетом скидки).</p>

* 1 контроллер:
<p>PurchaseController – основной контроллер для обработки логики покупок, накопительных скидок и формирования чека.</p>

* 6 представлений:
<p>index – отображает главную страницу с приветствием и списком доступных товаров.</p>
<p>product_detail – отображает детальную информацию о товаре.</p>
<p>purchase_form – выводит форму для ввода данных о покупке (имя покупателя, адрес).</p>
<p>purchase_create – обрабатывает отправку формы и создает новую запись о покупке.</p>
<p>receipt – выводит чек с информацией о покупке, включая скидку и итоговую стоимость.</p>
<p>customer_purchases – показывает историю покупок конкретного пользователя с информацией о скидках.</p>

### Используемые языки / библиотеки / технологии:
<p>Языки: Python3.8, HTML, Tailwind CSS</p>
<p>Фреймворки: Django</p>
<p>Базы данных: PostgreSQL </p>

### ERD-диаграмма:
![image](https://github.com/Lucky357231/PTLab2/blob/main/img/photo_2024-11-08_17-11-30.jpg?raw=true)

### Выводы:
Было разработано веб-приложение согласно индивидуальному заданию, протестировано разработанное веб-приложение, проблем выявено не было.

**В процессе данной разработки я познакомился с:**
* Моделью MVT, ее сущностью и основными фреймворками на ее основе.
* Сущностями «модель», «контроллер», «представление», их функциональным назначением в модели MVC.  

**Также я получил:**
* Навыки разработки веб-приложений с использованием MVC-фреймворков.
  
<h1 align="center">Лабораторная №3 по дисциплине "Технологии программирования"</h1>

## Постановка задачи:
**Цели:**
* Изучение модульного тестирования приложений.

### Индивидуальное задание:
* Написание юнит-тестов к проекту, разработанному в рамках лабораторной работы № 2.

### Краткое описание проекта:
Разработанное веб-приложение позволяет осуществлять модульное тестирование методов контроллера(т.к. логика работы приложения содержится в нем) проекта лабораторной работы № 2.

**Было разработано:**
### Тесты моделей:
- **Product**: проверка типов и значений полей.
- **Customer**: проверка типов и значений полей, таких как `name`, `email`, и `total_purchases`.
- **Purchase**: проверка правильного заполнения поля `date` и корректности расчета скидки.

### Тесты представлений (Views):
- **IndexViewTests**: проверка кода состояния, корректности шаблона и контекста главной страницы.
- **PurchaseCreateViewTests**: 
  - **GET-запрос**: проверка отображения формы покупки и правильной передачи контекста.
  - **POST-запрос**: проверка создания новой покупки, применения скидки, отображения данных в чеке, обновления информации о покупателе и записи данных в базу.

### Используемые языки / библиотеки / технологии:
<p>Язык проекта - Python</p>
Технологии - Django Test Framework

### Выполнение тестов:
![image](https://github.com/Lucky357231/PTLab2/raw/main/img/photo_2024-11-08_17-11-19.jpg)


### Выводы:
Было разработано веб-приложение осуществляющее модульное тестирование методов. Этот проект демонстрирует основы создания веб-приложений на Django с применением модели MVT. Реализованы базовые функции интернет-магазина, включая учет товаров, клиентов и заказов, с накопительной системой скидок. Тесты обеспечивают корректную работу основных функциональностей.контроллер проекта лабораторной работы № 2. Все тесты были успешно пройдены. В процессе данной разработки я изучил процесс модульного тестирования приложений.
