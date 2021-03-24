#!usr/bin/env python

import requests

# Get url and download file


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "w") as out_file:
        out_file.write(get_response.content)


download("url")
