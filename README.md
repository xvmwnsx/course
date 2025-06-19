# Веб-приложение успеваемости вуза

**Разработка веб-приложения с Python, Django, PostgreSql «Веб-приложение успеваемости вуза»**

На этой странице история проекта разработки веб-приложения расписания занятий которое позволит автоматизировать процесс составления, обновления и просмотра расписания для учебных заведений.


docker compose build --no-cache
docker compose up -d 

// Для миграций
docker compose exec -it student_infobase-python bash
python manage.py migrate