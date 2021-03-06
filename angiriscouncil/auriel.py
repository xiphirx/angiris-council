
import praw
import json
import math
from datetime import datetime
from string import Template
from . import time_utils

class Auriel(object):
    WIKI_COUNTDOWN_CONFIG = 'countdown_config'
    KEY_START_TIME = 'start_time'
    KEY_END_TIME = 'end_time'
    PARTS = 10

    def __init__(self, reddit, subreddit):
        self.reddit = reddit
        self.subreddit = subreddit

    def _get_config(self):
        subreddit = self.reddit.subreddit(self.subreddit)
        config_json = subreddit.wiki[self.WIKI_COUNTDOWN_CONFIG].content_md
        return json.loads(config_json)

    def update_countdown(self, logging=False):
        config = self._get_config()
        subreddit = self.reddit.subreddit(self.subreddit)

        countdowns_md = ''
        for countdown_config in config:
            timer_name = countdown_config
            countdown_config = config[countdown_config]
            start_time = countdown_config[self.KEY_START_TIME]
            end_time = countdown_config[self.KEY_END_TIME]
            current_time = time_utils.pacific_time_now().timestamp()

            if logging:
                print("Start %s | Current %s | End %s" % (start_time, current_time, end_time))

            days_left = max(0, int(math.ceil(time_utils.days(end_time - current_time))))
            countdown_md  = "%s, %d days remain\n\n[](#openProg)" % (timer_name, days_left)

            percentage = min(1.0, 
                (current_time - start_time) / (end_time - start_time))
            fill_count = int(percentage * self.PARTS)
            empty_count = self.PARTS - fill_count

            if fill_count == self.PARTS:
                countdown_md += '[](#10p)' * self.PARTS
                countdown_md += '[](#closeFull)'
            else:
                countdown_md += '[](#10p)' * (fill_count - 1)
                countdown_md += '[](#10h)'
                countdown_md += '[](#ep)' * empty_count
                countdown_md += '[](#closeProg)'

            if logging:
                print(countdown_md)

            countdowns_md += countdown_md + '\n\n'

        if logging:
            print("Updating sidebar...")

        current_sidebar = subreddit.description

        # TODO: This is a hack, figure out a good way to sync sidebar updates
        other_sentinel = '[~s~](/s)'
        sentinel_pos = current_sidebar.find(other_sentinel)
        prepend_content = current_sidebar[0:sentinel_pos]

        sentinel = '[~c~](/s)'
        sentinel_pos = current_sidebar.find(sentinel)
        current_sidebar = current_sidebar[sentinel_pos + len(sentinel):]
        tpl = Template(
            "$prepend$other_sentinel\n\n$countdown$sentinel$sidebar")
        new_sidebar = tpl.substitute(
                prepend=prepend_content,
                other_sentinel=other_sentinel,
                countdown=countdowns_md,
                sentinel=sentinel,
                sidebar=current_sidebar)
        subreddit.mod.update(description=new_sidebar)
