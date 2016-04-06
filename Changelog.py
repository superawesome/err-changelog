from errbot import BotPlugin, botcmd, re_botcmd
import re
import time
import requests

class Changelog(BotPlugin):
    @re_botcmd(pattern=r"^(.*)(#cl|\[#[0-9]+\])$", prefixed=False, flags=re.IGNORECASE)
    def cl(self, msg, match):
        """put something into the changelog"""

        # -d "{\"criticality\": 2, \"unix_timestamp\": $WHEN, \"category\": \"puppet\", \"description\": \"$REPO; $REV; $WHODUNIT; $i\"}"

        cl_message = match.string.replace('#cl', '').strip()
        data = {
                'criticality': 2,
                'unix_timestamp': int(time.time()),
                'category': 'irc',
                'description': msg.frm.nick + ': ' + cl_message
        }
        headers = {
                'Content-Type': 'application/json'
        }
        r = requests.post("https://changelog.allizom.org/api/events", headers=headers, json=data)
        #munged_name = msg.frm.nick[:1] + '\x030' + msg.frm.nick[1:]  # doesn't work, prints a 0 in the name ... how to do this?
        munged_name = msg.frm.nick  # do nothing for now
        self.send(self.build_identifier('#cl'), "<%s> %s" % (munged_name, cl_message))
        # return "from %s: %s" % (msg.frm.nick, cl_message)


    def check_changelog(self):
        self.log.debug("This is where I should be checking the changelog web app and spewing stuff into #cl")


    def activate(self):
        super(Changelog, self).activate()
        self.start_poller(60, self.check_changelog)
