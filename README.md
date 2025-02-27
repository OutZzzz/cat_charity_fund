### Фонд QRKot
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Как запустить проект:
Cоздать и активировать виртуальное окружение:

#### для Linux
```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip

```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### для Windows
```
python -m venv env
```

```
source env/Scripts/activate
```

```
python -m pip install --upgrade pip

```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Для запуска
```
uvicorn app.main:app
```
