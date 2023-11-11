# Case Review System V3 Api

### Used Technical Stacks

- Django
- Django REST Framework
- Postgre SQL

### Database Migration

You can reference `.env.example`.

```
DB_NAME=case_review
DB_USER=***
DB_PASSWORD=***
DB_HOST=localhost
DB_PORT=5432
```

You need to change `DB_USER` and `DB_PASSWORD` for your PostgreSQL Database.

Then make `.env` in `case_review` directory.

### 1. Clone Repo

If you want to clone this repo, go to the command line and run:

```bash
git clone git@github.com:meta-crawler/case-review-api.git
cd case-review-api
```

### 2. Install Dependencies

Add python virtual env:

```bash
python3 -m venv venv # virtualenv venv
```

To active python virtual env:

```bash
source venv/bin/activate
```

Install Django dependencies:

```bash
pip3 install -r requirements.txt # pip install -r requirements.txt
```

### 3. Seed database

To seed database, open new terminal and please run:

```bash
bash seed.sh
```

### 4. Run Development Environment

In virtual env terminal, please run:

```bash
python3 manage.py runserver
```
