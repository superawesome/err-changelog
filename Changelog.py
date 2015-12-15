from errbot import BotPlugin, botcmd
import time
import requests

class Changelog(BotPlugin):
    @re_botcmd(pattern=r"^.*#cl.*$", prefixed=False, flags=re.IGNORECASE)
    def cl(self, msg, match):
        """put something into the changelog"""

        # -d "{\"criticality\": 2, \"unix_timestamp\": $WHEN, \"category\": \"puppet\", \"description\": \"$REPO; $REV; $WHODUNIT; $i\"}"

        data = {
                'criticality': 2,
                'unix_timestamp': int(time.time()),
                'category': 'irc',
                'description': msg.frm.nick + ': ' + match
        }
        headers = {
                'Content-Type': 'application/json'
        }
        r = requests.post("https://changelog.allizom.org/api/events", headers=headers, json=data)
        return "changelog: from: %s, crit: %d, time: %d, cat: %s, desc: %s" % (msg.frm.nick, data['criticality'], data['unix_timestamp'], data['category'], data['description'])
