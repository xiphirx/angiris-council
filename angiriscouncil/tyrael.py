import praw
import json
from datetime import datetime
from string import Template
from . import time_utils


class Tyrael(object):
    WIKI_WEEKLY_THREADS_CONFIG = 'weeklythreads_config'
    KEY_TITLE = 'title'
    KEY_TEXT = 'text'
    KEY_POST_NUM = 'post_num'
    KEY_THREAD_ID = 'thread_id'
    KEY_SHORT_NAME = 'short_name'

    def __init__(self, reddit, subreddit):
        self.reddit = reddit
        self.subreddit = subreddit

    def _get_config(self):
        subreddit = self.reddit.get_subreddit(self.subreddit)
        config_json = subreddit.get_wiki_page(
            self.WIKI_WEEKLY_THREADS_CONFIG).content_md
        return json.loads(config_json)

    def post_weekly_thread(self, logging=False):
        config = self._get_config()
        day = time_utils.weekday_word().lower()
        todays_config = config[day]
        if len(todays_config) == 0:
            if logging:
                print("No threads to be posted today (%s)" % day)

            return

        if logging:
            print("Found thread(s) to post, posting...")
        subreddit = self.reddit.get_subreddit(self.subreddit)
        mod_list = []
        for thread_cfg in todays_config:
            title = thread_cfg[self.KEY_TITLE] + (
                " - %s" % time_utils.us_date())
            text = Template(thread_cfg[self.KEY_TEXT])
            post_num = thread_cfg['post_num'] + 1

            thread = subreddit.submit(
                title=title, text=text.substitute(count=post_num))
            thread.set_suggested_sort('new')
            thread.distinguish()

            thread_cfg[self.KEY_POST_NUM] = post_num
            thread_cfg[self.KEY_THREAD_ID] = thread.id
            mod_list.append(thread_cfg)

        if logging:
            print("Updating config wiki page...")
        config[day] = mod_list
        subreddit.edit_wiki_page(
            page=self.WIKI_WEEKLY_THREADS_CONFIG, content=json.dumps(config))

        # TODO: Move this to a different bot when we need real-time sidebar
        # updates
        if logging:
            print("Updating sidebar...")
        subreddit_settings = subreddit.get_settings()
        current_sidebar = subreddit_settings['description']
        sentinel = '[~s~](/s)'
        sentinel_pos = current_sidebar.find(sentinel)
        current_sidebar = current_sidebar[sentinel_pos + len(sentinel):]
        tpl = Template(
            "$lastUpdated\n\n#### Weekly $threads\n\n$sentinel$sidebar")

        thread_links = []
        for day in config:
            for thread_cfg in config[day]:
                thread_links.append("[%s](/%s)" % (
                    thread_cfg[self.KEY_SHORT_NAME],
                    thread_cfg[self.KEY_THREAD_ID]))

        lastUpdated = "[Last updated at " + datetime.now().strftime(
            "%H:%M:%S UTC") + "](/smallText)"
        new_sidebar = tpl.substitute(
            lastUpdated=lastUpdated,
            threads=' '.join(thread_links),
            sentinel=sentinel,
            sidebar=current_sidebar)
        subreddit.update_settings(description=new_sidebar)
