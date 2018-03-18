import os

from requests import get
from tqdm import tqdm
from datetime import datetime
import pickle
import tbapy
from pprint import pprint


class Store:

    FILE_EXTENSION = "-event_matches.p"

    def __init__(self, years):
        """Create the Store class for the specified years.

        Args:
            years (list): Of years to use for Store."""

        def _new_get(self, url):
            """This is used to be able to use the last modified header."""
            r = get(self.URL_PRE + url, headers={"X-TBA-Auth-Key": self.auth_key,
                                                 "If-Modified-Since": self.last_modified})
            if r.status_code == 200:
                self.last_modified_request = r.headers["Last-Modified"]
                return r.json()
            else:
                return {}

        tbapy.TBA._get = _new_get

        key = open("key.txt").read().strip("\n")

        self.years = years
        self.matches = {}
        self.events = {}

        if not os.path.exists("cache/"):
            os.mkdir("cache")

        self.tbapy = tbapy.TBA(key)
        self.tbapy.last_modified = ""
        self.tbapy.last_modified_request = ""

        self.load_cached()

    def load_cached(self):
        """Iterate through years and cache years if not already and check for
        update for year if in cache."""
        for year in self.years:
            if not os.path.exists("cache/" + str(year) + self.FILE_EXTENSION):
                self.cache_matches(year)
            else:
                # compare last modified tag to of year to one on tba
                self.check_for_update(year)

    def cache_matches(self, year):
        """Cache matches from a specified year.

        Args:
            year (int): Year to cache.
        """
        self.matches[year] = {}
        self.events[year] = {}

        r = self.tbapy.events(year)
        events_sorted = [e for e in sorted(r, key=lambda b: b["start_date"]) if e.event_type < 99]

        for event in tqdm(events_sorted, unit=" event"):
            self.matches[year][event.key] = []
            self.events[year][event.key] = {"end": event.end_date}
            for match in self.tbapy.event_matches(event.key):
                if match.alliances["red"]["score"] != -1:
                    self.matches[year][event.key].append({"key": match.key,
                                               "red_alliance": match.alliances["red"]["team_keys"],
                                               "blue_alliance": match.alliances["blue"]["team_keys"],
                                               "red_score": match.alliances["red"]["score"],
                                               "blue_score": match.alliances["blue"]["score"],
                                               "finish_time": match.post_result_time,
                                               "last_modified": self.tbapy.last_modified_request})

        pickle.dump((self.events[year], self.matches[year]), open("cache/" + str(year) + self.FILE_EXTENSION, "wb"))

    def check_for_update(self, year):
        """Check if a cached year is up to date and update if possible.

        Args:
            year (int): Year to check for update.
        """
        loaded_events, loaded_matches = pickle.load(open("cache/" + str(year) + self.FILE_EXTENSION, "rb"))

        now = datetime.now()
        if year != now.year:
            return

        for event in loaded_events:
            event_end = datetime.strptime(loaded_events[event]["end"], "%Y-%m-%d")
            if event_end > now:
                # print("{} has not finished".format(event))
                self.tbapy.last_modified = str(now)
                # matches = self.tbapy.event_matches(event)
                # for match in matches:
                #     if match.alliances["red"]["score"] != -1:
                #         print(self.tbapy.last_modified_request)
                        # match_list = {"key": match.key, "red_alliance": match.alliances["red"]["team_keys"],
                        #               "blue_alliance": match.alliances["blue"]["team_keys"],
                        #               "red_score": match.alliances["red"]["score"],
                        #               "blue_score": match.alliances["blue"]["score"],
                        #               "finish_time": match.post_result_time,
                        #               "last_modified": self.tbapy.last_modified_request}

        # r = self.tbapy.events(year, simple=True)
        # events_sorted = [e for e in sorted(r, key=lambda b: b["start_date"]) if e.event_type < 99]

        # for event in events_sorted:
        #     for match in self.tbapy.event_matches(event.key, simple=True):
        #         pass

        self.matches[year] = loaded_matches
        self.events[year] = loaded_events
