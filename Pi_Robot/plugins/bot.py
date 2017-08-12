from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
from tuling import get_response
import socket
import time

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/pi_robot.d")

@respond_to('tuling (.*)', re.IGNORECASE)
def tuling(message, something):
    message.reply(get_response(something))

@respond_to('pie', re.IGNORECASE)
def raspberry(message):
    sock.send('pie')
    message.reply(str(sock.recv(1024)))

@respond_to('home', re.IGNORECASE)
def home(message):
    sock.send('home')
    message.reply(str(sock.recv(1024)))