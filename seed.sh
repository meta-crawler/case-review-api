#!/bin/bash
source venv/bin/activate

python3 manage.py makemigrations
python3 manage.py migrate

fixtures=$(ls account/seed/)
while IFS= read -r fixture; do
    echo -n "Seeding Accounts..."
    echo $fixture
    python3 manage.py loaddata account/seed/$fixture
done <<< "$fixtures"

deactivate