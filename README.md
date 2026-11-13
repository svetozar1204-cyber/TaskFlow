# TaskFlow

## 1. Описание на проекта

TaskFlow е уеб приложение за управление на проекти и задачи. То позволява на потребителите да създават, преглеждат, редактират и изтриват проекти и задачи.

Проектът е разработен като учебен проект с Flask, PostgreSQL и Docker Compose.

## 2. Използвани технологии

- Python 3.12
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- Nginx
- HTML и CSS
- Pytest

## 3. Основни функционалности

- Създаване, редактиране и изтриване на проекти
- Създаване, редактиране и изтриване на задачи
- Управление на статуса на задачите
- Табло със статистика
- Системна страница за мониторинг
- Разпределяне на HTTP заявките чрез Nginx Load Balancer
- HTTPS със самоподписан сертификат

## 4. Архитектура

Приложението използва Docker Compose и се състои от следните компоненти:

- PostgreSQL – база данни
- Flask Web 1 – първа инстанция на приложението
- Flask Web 2 – втора инстанция на приложението
- Nginx – Load Balancer, който разпределя заявките между двете инстанции

## 5. Структура на проекта

```text
TaskFlow/
├── app/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── docs/
│   ├── architecture.md
│   └── class-diagram.md
├── nginx/
│   ├── certs/
│   └── nginx.conf
├── tests/
│   └── test_app.py
├── .devcontainer/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
```

## 6. Изисквания за стартиране

Необходимо е да имате инсталирани:

- Docker
- Docker Compose

## 7. Стартиране на проекта

1. Клонирайте хранилището:

```bash
git clone https://github.com/svetozar1204-cyber/TaskFlow.git
cd TaskFlow
```

2. Създайте `.env` файл на базата на примерния файл:

```bash
cp .env.example .env
```

3. Стартирайте контейнерите:

```bash
docker compose up -d --build
```

4. Проверете състоянието им:

```bash
docker compose ps
```

## 8. Достъп до приложението

- Основно приложение: http://localhost:5000
- Мониторинг: http://localhost:5000/monitoring
- HTTPS: https://localhost:5443

HTTPS използва самоподписан сертификат. Браузърът може да покаже предупреждение за сигурност.

## 9. Проверка на Load Balancer

Изпълнете следната команда:

```bash
for i in $(seq 1 10); do
  curl -s http://localhost:5000/health
done
```

Заявките трябва да се разпределят между `web1` и `web2`.

## 10. Проверка на HTTPS

Изпълнете:

```bash
curl -k https://localhost:5443/health
```

Опцията `-k` позволява проверка със самоподписан сертификат.

## 11. Автоматизирани тестове

Тестовете се намират в директорията `tests/`.

За изпълнение:

```bash
docker compose exec web1 python -m pytest -v
```

## 12. UML диаграма

Диаграмата на класовете се намира в:

`docs/class-diagram.md`

Тя представя класовете `Project` и `Task` и връзката между тях.

## 13. Автор

Учебен проект TaskFlow.