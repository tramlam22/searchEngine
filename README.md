#Installation
Create and activate your virtual environment
```bash
pip instal virtualenv
virtualenv env
source env/Scripts/activate
```

Then install all necessary packages from requirements.txt
```bash
pip install -r requirements.txt
```

#Running Haikyuu Search Engine
Begin the crawling process so that all data is extracted
```bash
python manage.py crawl
python manage.py runserver
```

The application will be found on your local host on port 8000 unless entered otherwise
```bash
http://localhost:8000/
```


