import subprocess, time, requests, re, json

##########################
# FILL IN THE INFO FIRST #
##########################
## NGROK(https://ngrok.io)
RDP_PORT = "3389" # This is the default port of RDP
NGROK_LOCATION = "C:\\Example\ngrok.exe" # Execuatble file for ngrok
NGROK_TOKEN = "SomeRandomStringWith_Number" # ngrok requires you to signup for using TCP tunnel
REGION = "us" # Choose the closest one to your location, others like "au", "ap", "eu" are availible

## Telegram
BOT_TOKEN = "12345:somerandomstring" # The token acquired from telegram @BotFather
CHAT_ID = "-123456789" # Chat that is group/channel/pm that the bot has access to

## Misc.
TIMEOUT = 60 * 60 # Interval between restarting a session


def main():
    ngrok = subprocess.Popen([NGROK_LOCATION, "tcp", RDP_PORT, "--authtoken", NGROK_TOKEN, "--region", REGION], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    with requests.session() as s:
        resp = s.get("http://127.0.0.1:4040")
        try:
            link = re.search('tcp://.*?\\\\',resp.text).group(0)[6:-1]
            print(link)
        except AttributeError:
            print("FAILED")
            return
    resp = json.loads(s.get("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + link).text)
    if resp["ok"] == True:
        print("Link sent")
    else:
        print("Failed to send link")
    time.sleep(TIMEOUT)
    ngrok.kill()

if __name__ == "__main__":
    while(True):
        main() 
