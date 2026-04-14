# Marketplace Sales Aggregator API

Сервис для агрегации данных о продажах с различных маркетплейсов (Ozon, Wildberries, Яндекс.Маркет).

## Технологический стек
- **FastAPI**: Основной фреймворк.
- **Pandas**: Обработка данных и расчет метрик.
- **Pydantic V2**: Валидация данных и настроек.
- **Docker & Docker Compose**: Контейнеризация.
- **Pytest**: Автоматизированное тестирование.

## Как запустить

### Создайте файл .env в корневом каталоге (см. файл .env.example)

### С помощью Docker (рекомендуется)
```bash
docker-compose up --build

### ССылки 
http://localhost:8000
http://localhost:8000/docs