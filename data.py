import os

from tqdm import tqdm
import pickle
import tbapy


class Store:

    FILE_EXTENSION = "-event_matches.p"

    def __init__(self, years, key):
        self.years = years
        self.tbapy = tbapy.TBA(key)
        self.matches = {}

        if not os.path.exists("cache/"):
            os.mkdir("cache")

        self.load_cached()

        def _new_tba_get(self, url):
            resp = self.session.get(self.URL_PRE + url,
                                    headers={"X-TBA-Auth-Key": self.auth_key,
                                             "If-Modified-Since":
                                             self.last_modified})
            if resp.status_code == 200:
                self.last_modified_response = resp.headers["Last-Modified"]
                return resp.json()
            else:
                return {}

        self.tbapy.TBA._get = _new_tba_get

    def load_cached(self):
        for year in self.years:
            if not os.path.exists("cache/" + str(year) +
                                  self.CACHE_FILE_EXTENSION):
                self.cache_match(year)
            else:
                # compare last modified tag to of year to one on tba
                self.check_for_update(year)

    def cache_match(self, year):
        self.match[year] = []
        r = self.tbapy.events(year, simple=True)

        events_sorted = [ev for ev in sorted(r, key=lambda b: b["start_date"])
                         if ev.event_type < 99]

        # {2018: [{key: lkjlkj, red_alliance: [0334, 54, 121], blue_alliance: [299, 845, 4774], red_score: 99, blue_score: 9999}, etc.]}

        for event in tqdm(events_sorted, unit=" event"):
            matches = self.tbapy.event_matches(event.key, simple=True)
            for match in matches:
                self.matches[year].append({"key": match.key,
                                           "red_alliance":
                                           match.alliances["red"],
                                           "blue_alliance":
                                           match.alliances["blue"],
                                           "red_score":
                                           match.alliances["red"]["score"],
                                           "blue_score":
                                           match.alliances["blue"]["score"]})

        pickle.dump(self.matches, open("cache/" + str(year) +
                    self.FILE_EXTENSION))

    def check_for_update(self, year):
        loaded_cache = pickle.load(open("cache/" + str(year) +
                                   self.FILE_EXTENSION, "rb"))


x = Store([2017],
          "get your own key")
