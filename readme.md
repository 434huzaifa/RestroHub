# RestroHub
#### simple restaurant management backend site with stripe payment. And Swagger UI to interact with API.

### TechStack

- Django
- Django-ninja
- Django-ninja-extra
- Stripe
- JWT
- Sqlite3
- Pipenv

### To run this application locally

```
git clone https://github.com/434huzaifa/RestroHub
```

```
cd RestroHub
```

create `.env` file. follow the `.env.example`. you need `stripe` secret key to use payment method.

if you already have `pipenv` then you dont need this step

```
pip install pipenv
```

```
pipenv shell
```

I am using python3.12 thats why instead of `python` i am writing `py`

```
pipenv sync --bare --clear
```

```
py manage.py migrate
```

if you want to populate database with data

```
py manage.py loaddata data.json
```


```
py manage.py runserver
```