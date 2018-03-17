import os

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
        key = open("key.txt").read().strip("\n")

        self.years = years
        self.matches = {}

        if not os.path.exists("cache/"):
            os.mkdir("cache")

        self.tbapy = tbapy.TBA(key)

        self.load_cached()
        # self.check_for_update(2018)

    def load_cached(self):
        """Iterate through years and cache years if not already and check for
        update for year if in cache."""
        for year in self.years:
            if not os.path.exists("cache/" + str(year) +
                                  self.FILE_EXTENSION):
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
        r = self.tbapy.events(year, simple=True)

        events_sorted = [ev for ev in sorted(r, key=lambda b: b["start_date"])
                         if ev.event_type < 99]

        for event in tqdm(events_sorted, unit=" event"):
            matches = self.tbapy.event_matches(event.key, simple=True)
            for match in matches:
                print(type(event))
                self.matches[year][event.key] = []
                self.matches[year][event.key].append({"key": match.key,
                        "red_alliance": match.alliances["red"]["team_keys"],
                        "blue_alliance": match.alliances["blue"]["team_keys"],
                        "red_score": match.alliances["red"]["score"],
                        "blue_score": match.alliances["blue"]["score"],
                        "last_modified": self.tbapy.last_modified})

        pickle.dump(self.matches, open("cache/" + str(year) +
                    self.FILE_EXTENSION, "wb"))
        self.years = self.matches.keys()

    def check_for_update(self, year):
        """Check if a cached year is up to date and update if possible.

        Args:
            year (int): Year to check for update.
        """
        loaded_cache = pickle.load(open("cache/" + str(year) +
                                   self.FILE_EXTENSION, "rb"))
        self.matches[year] = loaded_cache
        self.years.append(year)

        if year != datetime.now().year:
            return
