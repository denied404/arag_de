# Project description
A simple scraper for arag.de website which extracts all arag agents information.

# Usage
1. Make sure that you have a `python2` and `virtualenv` installed
2. Make a new virtualenv for this project by running `virtualenv --python=/usr/bin/python2 .venv` in a root folder of the current project
3. Activate a brand new virtualenv by running `source .venv/bin/activate`
4. Install all requirements for this project by running `pip install -r requirements.txt`
5. This scraper uses anti-captcha.com service. Create your account there and after that create an OS environment variable which keeps your anti-captcha.com API key: `export ANTICAPTCHA_API_KEY=your_api_key`

That's it! For running the scraper and getting all the scraped results to `out.csv` file just execute this command:
```
scrapy crawl AragDeSpider -o out.csv -t csv
```
