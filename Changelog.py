from errbot import BotPlugin, botcmd, re_botcmd
import re
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


    def check_changelog(self):
        self.log.debug("This is where I should be checking the changelog web app and spewing stuff into #cl")


    def activate(self):
        super().activate()
        self.start_poller(60, self.check_changelog)
