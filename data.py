import os

from requests import get
from requests import Session
from tqdm import tqdm
from datetime import datetime
from collections import namedtuple
import pickle
import tbapy
from pprint import pprint

Event = namedtuple("Event", ["end_date", "key"])
Match = namedtuple("Match", ["key", "red_alliance", "blue_alliance", "red_score", "blue_score"])


class Store:

    FILE_EXTENSION = "-event_matches.p"

    def __init__(self, years):
        """Create the Store class for the specified years.

        Args:
            years (list): Of years to use for Store."""

        key = open("key.txt").read().strip("\n")

        self.years = years
        self.matches = {}
        self.events = {}

        if not os.path.exists("cache/"):
            os.mkdir("cache")

        self.tbapy = tbapy.TBA(key)

        for year in self.years:
            # cache year if does not exist
            if not os.path.exists("cache/" + str(year) + self.FILE_EXTENSION):
                self.cache_matches(year)
            # check for update of year if it does exist
            else:
                self.check_for_update(year)

    def cache_matches(self, year):
        """Cache matches from a specified year.

        Args:
            year (int): Year to cache.
        """
        self.matches[year] = {}
        self.events[year] = []

        # make tbapy request and only use events that are actual events
        r = self.tbapy.events(year)
        events_sorted = [e for e in sorted(r, key=lambda b: b["start_date"]) if e.event_type < 99]

        # iterate through events with a progress bar
        for event in tqdm(events_sorted, unit=" event"):
            # create event and add to events
            event_nt = Event(event.end_date, event.key)
            self.events[year].append(event_nt)
            # iterate through matches in event
            for match in self.tbapy.event_matches(event.key):
                # make sure match hasn't been played
                if match.alliances["red"]["score"] != -1:
                    # set the match of event to a list to append matches to
                    self.matches[year][event.key] = []
                    # create match and add to matches
                    match_nt = Match(match.key,
                                          match.alliances["red"]["team_keys"],
                                          match.alliances["blue"]["team_keys"],
                                          match.alliances["red"]["score"],
                                          match.alliances["blue"]["score"])
                    self.matches[year][event.key].append(match_nt)

        # cache events and matches
        pickle.dump((self.events[year], self.matches[year]),
                    open("cache/" + str(year) + self.FILE_EXTENSION, "wb"))

    def load_cached(self, year):
        """Load cached years.

        Args:
            year (int): Year to be loaded.

        Returns:
            loaded_events (list): Loaded events.
            loaded_matches (dict): Loaded matches.
        """
        loaded_events, loaded_matches = pickle.load(open("cache/" + str(year) +
                                                    self.FILE_EXTENSION, "rb"))
        return loaded_events, loaded_matches

    def check_for_update(self, year):
        """Check if a cached year is up to date and update if possible.

        Args:
            year (int): Year to check for update.
        """
        # load cached year
        loaded_events, loaded_matches = self.load_cached(year)

        # if it is not the current year it won't have an update
        now = datetime.now()
        if year != now.year:
            self.matches[year] = loaded_matches
            self.events[year] = loaded_events
            return

        # for event in loaded_events:
        #     print(event)
            # event_end = datetime.strptime(event, "%Y-%m-%d")
            # print(loaded_events[event]["end"])
            # if event_end > now:
            #     pass

        self.matches[year] = loaded_matches
        self.events[year] = loaded_events
