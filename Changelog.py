from errbot import BotPlugin, botcmd
import time
import requests

class Changelog(BotPlugin):
    @botcmd
    def cl(self, msg, args):
        """put something into the changelog"""

        # -d "{\"criticality\": 2, \"unix_timestamp\": $WHEN, \"category\": \"puppet\", \"description\": \"$REPO; $REV; $WHODUNIT; $i\"}"

        data = {
                'from': msg.frm.nick,
                'criticality': 2,
                'unix_timestamp': int(time.time()),
                'category': 'user',
                'description': args
        }
        headers = {
                'Content-Type': 'application/json'
        }
        r = requests.post("https://changelog.allizom.org/api/events", headers=headers, json=data)
        return "changelog: from: %s, crit: %d, time: %d, cat: %s, desc: %s" % (data['from'], data['criticality'], data['unix_timestamp'], data['category'], data['description'])
