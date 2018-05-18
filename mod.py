from requests import get

base_url = "https://www.thebluealliance.com/api/v3"

r = get(base_url + "/event/2018ausp/matches/simple", headers={"X-TBA-Auth-Key": "Q2okhWSX3j4buRyOQswSNWyhsfLTKYuGowNaKLAWCQhvTIROUBnVA8uNR6gLkLmR"})
print(r)
print(r.headers['Last-Modified'])
