from slackbot.bot import Bot
import os
import sys
def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print "This program must be run as root."
        sys.exit(1)
    else:
        main()
