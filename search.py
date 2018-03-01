#!/usr/bin/python3
import requests

SEARCH_URL = "https://itsapps.unc.edu/dir/dirSearch/search"
DETAIL_URL= "https://itsapps.unc.edu/dir/dirSearch/details"

def createSearchResultStr(jsonRes):
    res = jsonRes["givenName"] + " " + jsonRes["sn"]
    if "mail" in jsonRes:
        res += " (" + jsonRes["mail"] + ")"
    if "telephoneNumber" in jsonRes:
        res += " " + jsonRes["telephoneNumber"]
    return res

def createIDDisplayStr(idObj):
    res = "Name: " + idObj["cn"]
    if "mail" in idObj:
        res += "\n"
        res += "Email: " + idObj["mail"]
    if "telephoneNumber" in idObj:
        res += "\n"
        res += "Telephone Number: " + idObj["telephoneNumber"]
    return res

def search(queryStr):
    query = {"searchString": queryStr}
    response = requests.post(SEARCH_URL, data=query)
    if response.ok:
        return response.json()
    else:
        raise Exception("Unable to get search results, response code: " + response.status_code)

def getDetails(spid):
    query = {"spid": spid}
    response = requests.post(DETAIL_URL, data=query)
    if response.ok:
        return response.json()
    else:
        raise Exception("Unable to get search results, response code: " + response.status_code)

# Get a list of people matching some user-specified query (e.g. name)
results = search(input("Who do you want to get info on?: "))
if results:
    print("=== Results: ===")
    idx = 0
    while idx < len(results):
        print(str(idx+1) + ": " + createSearchResultStr(results[idx]))
        idx += 1
else:
    print("No results.")
    exit()

# Get details on one of the search results
details = {}
if len(results) == 1:
    details = getDetails(results[0]["spid"])
else:
    details = getDetails(results[int(input("Who do you want to get details on?: ")) - 1]["spid"])
if details:
    print("=== Details: ===")
    print(details)
    # Find and print ID info
    for obj in details:
        if "organizationalPerson" in obj["objectClass"]:
            print(createIDDisplayStr(obj))
            break
    exit()
else:
    print("No results.")
