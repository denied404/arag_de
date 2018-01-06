import re
import os
import requests
from python_anticaptcha import AnticaptchaClient, Proxy, NoCaptchaTaskProxylessTask

api_key = os.getenv('ANTICAPTCHA_API_KEY')
site_key_pattern = 'data-sitekey=["\'](.+?)["\']'
client = AnticaptchaClient(api_key)
session = requests.Session()


def solve_captcha(url):
    html = get_form_html(url)
    return get_token(html, url)


def get_form_html(url):
    return session.get(url).text


def get_token(form_html, url):
    site_key = re.search(site_key_pattern, form_html).group(1)
    task = NoCaptchaTaskProxylessTask(website_url=url,
                                      website_key=site_key)
    job = client.createTask(task)
    job.join()
    return job.get_solution_response()


if __name__ == '__main__':
    print solve_captcha('https://www.arag.de/kontakt/arag-vor-ort/')
