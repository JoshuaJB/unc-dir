#!/usr/bin/python3
import requests
import sys
import urllib.parse

SEARCH_URL = "https://dir.unc.edu/api/search"
DETAIL_URL= "https://dir.unc.edu/api/lookup"
DEBUG = False
if len(sys.argv) > 1 and sys.argv[1] == "--debug":
    DEBUG = True

def createSearchResultStr(jsonRes):
    res = jsonRes["givenNameIterator"][0] + " " + jsonRes["snIterator"][0]
    if "mailIterator" in jsonRes:
        res += " <" + jsonRes["mailIterator"][0] + ">"
    if "telephoneNumberIterator" in jsonRes:
        res += " " + jsonRes["telephoneNumberIterator"][0]
    return res

def createIDDisplayStr(idObj):
    res = "Name: " + idObj["displayName"]
    if "mail" in idObj:
        res += "\n"
        res += "Email: " + idObj["mailIterator"][0]
    if "telephoneNumber" in idObj:
        res += "\n"
        res += "Work Phone: " + idObj["telephoneNumberIterator"][0]
    return res

def createAcademicDisplayStr(acObj):
    res = ""
    for i in range(0,min(len(acObj["plans"]), len(acObj["programs"]))):
        if i > 0:
            res += "\n--------\n"
        if "plans" in acObj:
            plan = acObj["plans"][i]
            res += "Major: " + plan["uncPlanIterator"][0]
        if "programs" in acObj:
            program = acObj["programs"][i]
            res += "\n"
            res += "School: " + program["uncAcademicGroupIterator"][0] + "\n"
            program["uncProgramIterator"][0] = program["uncProgramIterator"][0].replace("AS", "Arts and Sciences")
            program["uncProgramIterator"][0] = program["uncProgramIterator"][0].replace("SM", "School of Medicine")
            res += "Program: " + program["uncProgramIterator"][0]
    return res

def createStaffDisplayStr(acObj):
    res = ""
    for job in acObj["uncJobs"]:
        res += "Job: " + job["titleIterator"][0] + " - " + job["ouIterator"][0] + "\n"
    return res

def search(queryStr):
    response = requests.get(SEARCH_URL + "/" + urllib.parse.quote(queryStr))
    if response.ok:
        return response.json()
    else:
        raise Exception("Unable to get search results, response code: " + str(response.status_code))

def getDetails(dn):
    response = requests.get(DETAIL_URL + "/" + dn)
    if response.ok:
        return response.json()
    else:
        raise Exception("Unable to get search results, response code: " + str(response.status_code))

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
    details = getDetails(results[0]["dn"])
else:
    details = getDetails(results[int(input("Who do you want to get details on?: ")) - 1]["dn"])
if details:
    print("=== Details: ===")
    if DEBUG:
        print(details)
    # Find and print ID info
    for key in details.keys():
        if key == "uncPerson":
            print(createIDDisplayStr(details[key]))
            break
    # Find and print staff info
    for key in details.keys():
        if key == "uncStaff":
            print(createStaffDisplayStr(details[key]), end = '')
            break
    # Find and print academic info
    for key in details.keys():
        if key == "uncStudent":
            print(createAcademicDisplayStr(details[key]))
            break
    exit()
else:
    print("No results.")
    exit()
