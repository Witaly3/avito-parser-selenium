# Парсер сайта объявлений Avito

Парсер с помощью **Selenium** собирает информацию, в том числе и телефон, с частных объявлений категории _"Недвижимость" - "Квартиры в аренду"_ и сохранят в базу данных **SQLite3** и в файл **Excel**. Валюта цены аренды дополнительно меняется на евро по курсу ЦБ РФ на день сохранения в базу данных. 


## Установка и запуск

1. Склонировать репозиторий с Github:

````
git clone git@github.com:Witaly3/avito-parser-selenium.git
````
2. Перейти в директорию проекта

3. Создать виртуальное окружение:

````
python -m venv venv
````

4. Активировать окружение: 

````
source\venv\bin\activate
````
5. В файле config.py изменить город или регион поиска (по умолчанию "Рязань")
 
6. Установка зависимостей:

```
pip install -r requirements.txt
```
7. Установить необходимые драйвера для браузеров: ``` https://losst.ru/ustanovka-selenium-v-linux ```

8. Запустить парсер
```
python avitoparser.py
```
---
При возникновении ошибок от модуля **"Pytesseract"** установить дополнительно: 
```
sudo apt-get install python3-pil tesseract-ocr libtesseract-dev tesseract-ocr-eng tesseract-ocr-script-latn
```
либо следовать другим советам из stackoverflow:

```https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i```
