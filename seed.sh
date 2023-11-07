#!/bin/bash
source venv/bin/activate

python3 manage.py makemigrations
python3 manage.py migrate

fixtures=$(ls account/seed/)
while IFS= read -r fixture; do
    echo -n "Seeding Account..."
    echo $fixture
    python3 manage.py loaddata account/seed/$fixture
done <<< "$fixtures"

fixtures=$(ls api/seed/)
while IFS= read -r fixture; do
    echo -n "Seeding Api..."
    echo $fixture
    python3 manage.py loaddata api/seed/$fixture
done <<< "$fixtures"

deactivate