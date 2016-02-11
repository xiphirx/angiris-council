import praw
import time
import json
from . import time_utils
from string import Template


class Itherael(object):
    WIKI_BLUETRACKER = 'bluetracker'
    WIKI_BLUETRACKER_NOCS = 'bluetracker_nocs'
    WIKI_BLUETRACKER_CONFIG = 'bluetracker_config'

    def __init__(self, reddit, subreddit):
        self.reddit = reddit
        self.subreddit = subreddit
        self.header = Template("""
Viewing all Blizzard representatives.
[Exclude customer service](/r/$r/wiki/$wiki_page).\n\n
        """)

        self.header_nocs = Template("""
Excluding customer service representatives.
[View all](/r/$r/wiki/$wiki_page).\n\n
        """)

    def _merge_dict_lists(self, a, b):
        c = a.copy()
        for key, value in b.items():
            if key in c.keys():
                c[key].extend(value)

        return c

    def _get_config(self):
        subreddit = self.reddit.get_subreddit(self.subreddit)
        config_json = subreddit.get_wiki_page(
            self.WIKI_BLUETRACKER_CONFIG).content_md
        config = json.loads(config_json)
        config['subreddits'] = [x.lower() for x in config['subreddits']]
        return config

    def track_blues(self, staging=False, logging=False):
        staging_mod = "_staging"
        page = self.WIKI_BLUETRACKER
        page = page + staging_mod if staging else page

        page_nocs = self.WIKI_BLUETRACKER_NOCS
        page_nocs = page_nocs + staging_mod if staging else page_nocs

        if logging:
            print('Retrieving configuration...')

        config = self._get_config()

        if logging:
            print('Gathering lore [1/2]...')

        lore = self.gather_lore(config['users'], config['subreddits'])
        if logging:
            print('Gathering lore [2/2]...')
        lore_cs = self.gather_lore(config['users_cs'], config['subreddits'])

        subreddit = self.reddit.get_subreddit(self.subreddit)

        # Everyone
        if logging:
            print('Scribing [1/2]...')
        script = [self.header.substitute(
            r=self.subreddit, wiki_page=self.WIKI_BLUETRACKER_NOCS)]
        script.append(self.scribe(self._merge_dict_lists(lore, lore_cs)))
        subreddit.edit_wiki_page(page=page, content=''.join(script))

        # No customer service
        if logging:
            print('Scribing [2/2]...')
        script = [self.header.substitute(
            r=self.subreddit, wiki_page=self.WIKI_BLUETRACKER)]
        script.append(self.scribe(lore))
        subreddit.edit_wiki_page(page=page_nocs, content=''.join(script))

        if logging:
            print('Done')

    def scribe(self, lore):
        script = []
        for topic in sorted(lore.keys()):
            script.append("\n#%s\n\n" % topic)
            sortedData = sorted(lore[topic], key=lambda x: -x.created_utc)
            for datum in sortedData:
                link = "%s?context=3" % datum.permalink
                script.append(
                    "* /u/%s (%s ago) [%s](%s) by /u/%s\n\n  >%s\n\n" %
                    (datum.author,
                     time_utils.time_ago(datum.created_utc),
                     datum.link_title,
                     link,
                     datum.link_author,
                     datum.body.replace("#", "&#35;").replace("\n", "\n>")))

        return ''.join(script)

    def gather_lore(self, subjects, topics):
        comment_limit = 10
        lore = {}
        now = time.time()
        for name in subjects:
            user = self.reddit.get_redditor(name)
            for datum in user.get_comments(limit=comment_limit):
                if now - datum.created_utc >= 60 * 60 * 24 * 10:  # Ten days
                    continue

                topic = datum.subreddit.display_name.lower()
                if topic not in topics:
                    continue

                lore.setdefault(topic, []).append(datum)

        return lore
