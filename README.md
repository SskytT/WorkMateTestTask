# CuteCats

CuteCats — это веб-приложение для работы с котятами. Вы можете создавать, изменять, удалять и оценивать котят.

## Технологии
- **Django**
- **Django Rest FrameWork** и дополнительные библиотеки
- **Nginx**
- **Docker**, **Docker-compose**

## Запуск приложения
0. Убедитесь, что **Docker** и **Docker Compose** установлены и запущены на вашей системе.
1. Перейдите в корень проекта (папка с файлом `Dockerfile`).
2. Откройте консоль в этой папке.
3. Выполните команду:
   ```bash
   docker-compose up --build -d
   ```
4. Зайдите на [http://127.0.0.1/swagger/](http://127.0.0.1/swagger/). Там будет описан API, с помощью которого можно взаимодействовать с проектом.

## Минимум данных для проверки работоспособности приложения
- Для админ панели: [http://127.0.0.1/admin/](http://127.0.0.1/admin/)  
  **логин:** admin  
  **пароль:** admin

### Породы котов
- **Бенгальский**: 5
- **Британский короткошёрстный**: 4
- **Шотландский вислоухий**: 3
- **Мейн-кун**: 2
- **Сиамский**: 1

### Аккаунты
- **user1**: user1
- **user2**: user2
- **user3**: user3

Чтобы авторизироваться, нужно выполнить команду:
```bash
POST http://127.0.0.1/api/v1/token
```
В теле запроса укажите:
```json
{
  "username": "string",
  "password": "string"
}
```
Вы получите токены для обновления токенов и для авторизации. Для авторизированных запросов добавьте заголовок:
```
Authorization: Bearer <ваш access токен>
```

### Коты с оценками
- Коты с pk 14, 15, 16 имеют оценки.

## Документация API

### Обзор
Этот API предоставляет конечные точки для управления породами кошек и самими кошками. Он поддерживает регистрацию пользователей и аутентификацию с использованием токенов JWT.

### Базовый URL
```
http://localhost/api/v1
```

Все запросы не касающиеся работы с аккаунтом доступны только авторизированным пользователем. 
Нужен такой заголовок:
```
Authorization: Bearer <ваш access токен>
```

### Конечные точки
1. **Получить породы**
   - **GET** `/breed`

2. **Список кошек**
   - **GET** `/cat/`
   - Параметры(через адресную строку):
     - `breed` (необязательно): Фильтрация по имени породы.
     - `user` (необязательно): Фильтрация по ID пользователя.
   - **Пример** `/cat/?breed=3`

3. **Создать кошку**
   - **POST** `/cat/`
   - Тело запроса:
     ```json
     {
       "color": "string",
       "age": "integer",
       "description": "string",
       "breed": "integer"
     }
     ```

4. **Получить кошку по ID**
   - **GET** `/cat/{id}/`

5. **Обновить кошку**
   - **PUT** `/cat/{id}/`
   - Тело запроса: Структура аналогична созданию кошки.

6. **Частичное обновление кошки**
   - **PATCH** `/cat/{id}/`
   - Тело запроса: Частичный объект кошки.

7. **Удалить кошку**
   - **DELETE** `/cat/{id}/`

8. **Оценить кошку**
   - **POST** `/cat/{id}/rate/`
   - Тело запроса:
     ```json
     {
       "value": "int",
     }
     ```
9. **Получить рейтинг кошки**
   - **GET** `/cat/{id}/rating/`

10. **Регистрация пользователя**
    - **POST** `/register`
    - Тело запроса:
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```

11. **Получить токен**
    - **POST** `/token`
    - Тело запроса:
      ```json
      {
        "username": "string",
        "password": "string"
      }
      ```

12. **Обновить токен**
    - **POST** `/token/refresh`
    - Тело запроса:
      ```json
      {
        "refresh": "string"
      }
      ```

## Модели данных

### Порода
- **ID**: integer (только для чтения)
- **Имя**: string (обязательно, maxLength: 100)

### Кошка
- **ID**: integer (только для чтения)
- **Цвет**: string (обязательно, maxLength: 100)
- **Возраст**: integer (обязательно)
- **Описание**: string (обязательно, maxLength: 1000)
- **Порода**: integer (обязательно)
- **Пользователь**: integer (только для чтения)
- **URL списка рейтингов**: string (только для чтения)
- **Количество рейтингов**: string (только для чтения)
- **Средний рейтинг**: string (только для чтения)

### TokenObtainPair
- **Имя пользователя**: string (обязательно)
- **Пароль**: string (обязательно)

### TokenRefresh
- **Refresh**: string (обязательно)
- **Access**: string (только для чтения)
