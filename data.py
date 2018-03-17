import os

from requests import get
from tqdm import tqdm
from datetime import datetime
import pickle
import tbapy


class Store:

    FILE_EXTENSION = "-event_matches.p"

    def __init__(self, years):
        """Create the Store class for the specified years.

        Args:
            years (list): Of years to use for Store."""

        def _new_get(self, url):
            """This is used to be able to use the last modified header."""
            r = get(self.URL_PRE + url, headers={"X-TBA-Auth-Key": self.auth_key, "If-Modified-Since": self.last_modified})
            if r.status_code == 200:
                self.last_modified_request = r.headers["Last-Modified"]
                return r.json()
            else:
                return {}

        tbapy.TBA._get = _new_get

        key = open("key.txt").read().strip("\n")

        self.years = years
        self.matches = {}

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
        self.matches[year] = []
        r = self.tbapy.events(year, simple=True)

        events_sorted = [e for e in sorted(r, key=lambda b: b["start_date"]) if e.event_type < 99]

        for event in tqdm(events_sorted, unit=" event"):
            matches = self.tbapy.event_matches(event.key, simple=True)
            for match in matches:
                self.matches[year].append({"key": match.key,
                                           "red_alliance": match.alliances["red"]["team_keys"],
                                           "blue_alliance": match.alliances["blue"]["team_keys"],
                                           "red_score": match.alliances["red"]["score"],
                                           "blue_score": match.alliances["blue"]["score"]})
                                        # "last_modified": self.tbapy.last_modified})

        pickle.dump(self.matches, open("cache/" + str(year) + self.FILE_EXTENSION, "wb"))

    def check_for_update(self, year):
        print("checkign ")
        """Check if a cached year is up to date and update if possible.

        Args:
            year (int): Year to check for update.
        """
        loaded_cache = pickle.load(open("cache/" + str(year) + self.FILE_EXTENSION, "rb"))
        self.matches[year] = loaded_cache[year]
        # print(loaded_cache)

        current_year = datetime.now().year

        # if year != current_year:
        # #     return

        r = self.tbapy.events(year, simple=True)
        events_sorted = [e for e in sorted(r, key=lambda b: b["start_date"]) if e.event_type < 99]

        for event in events_sorted:
            for match in self.tbapy.event_matches(event.key, simple=True):
                print(type(self.matches[year][0]))
