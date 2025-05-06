
# Graph Operating API

Проект реализует REST API для создания, хранения и управления направленными ациклическими графами (DAG) с использованием FastAPI, SQLAlchemy и PostgreSQL.

## Функционал:

- Создание графа с вершинами и рёбрами
- Получение информации о графе
- Получение списков смежности и обратной смежности
- Удаление вершины из графа
- Проверка графа на корректность:
  - Ацикличность
  - Отсутствие петель
  - Уникальность узлов и рёбер
  - Соответствие ограничениям по имени
  - Удаление в случае опустошения

## Стек

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker + Docker Compose
- Pytest + TestClient (99% покрытие тестами)

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone <URL>
cd Graph_Operating_FastAPI
```

### 2. Настройте переменные окружения

Создайте файл .env:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/graph_db
```

### 3. Запуск Docker

```bash
docker-compose up -d --build
```

После запуска приложение будет доступно по адресу:

```
http://localhost:8080
```


## Тестирование

### Запуск тестов (после запуска контейнера через Docker)

```bash
docker-compose exec web pytest --cov=app --cov-report=term-missing
```
