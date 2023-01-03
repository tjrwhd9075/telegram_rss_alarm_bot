echo "Cloning Repo...."
git clone https://github.com/tjrwhd9075/telegram_rss_alarm_bot /rsstelbot
cd /rsstelbot
pip3 install -r requirements.txt
echo "Starting Bot...."
python3 rss_telbot.py