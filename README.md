### E-diamond

## requirements
django>=3.0
python>=3.5

## run
1. pip3 install -r requirements.txt
2. python3 manage.py makemigrations
3. python3 manage.py migrate
4. python3 manage.py runserver

## Clear the migration
1. python3 manage.py showmigrations
2. python3 manage.py migrate --fake user zero
3. python3 manage.py migrate --fake qa_admin zero
4. python3 manage.py migrate --fake advertiser zero
5. python3 manage.py migrate --fake publisher zero
6. find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
7. find . -path "*/migrations/*.pyc"  -delete
8. python3 manage.py makemigrations
9. python3 manage.py migrate --fake-initial

## Clear the migration(second way)
1. find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
2. find . -path "*/migrations/*.pyc"  -delete
3. Drop the current database
4. python3 manage.py makemigrations
5. python3 manage.py migrate


