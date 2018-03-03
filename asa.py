#!/usr/bin/env python

import sys
import os
import requests
import json

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'User-Agent': 'ASA-API'
          }

def groupcheck(asaip, user, pw, verify, group):
    r = requests.get('https://%s/api/objects/networkobjectgroups' % asaip, \
                        headers=headers, auth=(user,pw), verify=False)
    res = r.json()

    for item in res['items']:
        obj = item['objectId']
        if obj == group:
            for members in item['members']:
                mem = members['value']
                if mem == ip:
                    res = 2
                    return res
            res = 1
            return res
    res = 0
    return res

def addgroup(asaip, user, pw, verify, group, ip):
    data = {
            "kind": "object#NetworkObjGroup",
            "name": group,
              "members": [
                {
                  "kind": "IPv4Address",
                  "value": ip
                }
              ],
              "description": "BadIPList based on OpenDXL messages"
           }

    r = requests.post('https://%s/api/objects/networkobjectgroups' % asaip, \
                        headers=headers, auth=(user,pw), data=json.dumps(data), verify=False)

    if r.status_code == 201:
        print 'Group %s got succesfully added to Cisco ASA' % group

    return r

def modgroup(asaip, user, pw, verify, group, ip):
    data = {
              "members.add": [
                {
                  "kind": "IPv4Address",
                  "value": ip
                }
              ]
           }

    r = requests.patch('https://%s/api/objects/networkobjectgroups/%s' % (asaip, group), \
                        headers=headers, auth=(user,pw), data=json.dumps(data), verify=False)

    if r.status_code == 204:
        print 'IP Address got successfully added to the %s group' % group

    return r

if __name__ == "__main__":
    asaip = '1.1.1.1'
    user = 'username'
    pw = 'password'
    verify = 'False'

    ip = sys.argv[1]
    group = 'BadIPList'

    groupchk = groupcheck(asaip, user, pw, verify, group)
    if groupchk == 0:
        addgroup(asaip, user, pw, verify, group, ip)
    elif groupchk == 1:
        modgroup(asaip, user, pw, verify, group, ip)
    elif groupchk == 2:
        print "Group already in Cisco ASA and IP is in Group"
