# scrapy-keskisuomalainen-kuntavaalit2021
Fetch all from [Keskisuomalainen Kuntavaalit 2021](https://www.ksml.fi/vaalikone/#/) site

    scrapy crawl kaikki

Fetch single municipality (37=Jyväskylä): 

    scrapy crawl kunta -a id=37

## Requirements

* Python
* [Scrapy](https://scrapy.org/)
