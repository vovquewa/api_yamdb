### Импорт тестовой базы данных
Данные для тестовой базы данных должны быть расположены в каталоге
```
static/data/
```
##### Источники и формат наполнения
	- users.csv [id,username,email,role,bio,first_name,last_name]
	- genre.csv [id,name,slug]
	- category.csv [id,name,slug]
	- titles.csv [id,name,year,category]
	- genre_title.csv [id,title_id,genre_id]
	- review.csv [id,title_id,text,author,score,pub_date]
	- comments.csv [id,review_id,text,author,pub_date]

Для импорта каждого источника подготовалена менеджмент команда:
```python
python manage.py import_from_csv_{имя источника}
```

Пример:
```python
python manage.py import_from_csv_users
```

Комманды следует выполнять в порядке, перечисленом выше