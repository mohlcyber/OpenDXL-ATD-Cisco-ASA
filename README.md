# OpenDXL-ATD-CiscoASA
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This integration is focusing on the automated threat response with McAfee ATD, OpenDXL and Cisco ASA Firewalls. McAfee Advanced Threat Defense (ATD) will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will subscribe and parse IP indicators ATD produced and will automatically update Firewall rules.

## Component Description

**McAfee Advanced Threat Defense (ATD)** is a malware analytics solution combining signatures and behavioral analysis techniques to rapidly identify malicious content and provides local threat intelligence. ATD exports IOC data in STIX format and DXL.
https://www.mcafee.com/in/products/advanced-threat-defense.aspx

**Cisco ASA Firewalls** are security devices protecting corporate networks and data centers of all sizes. It provides users with highly secure access to data and network resources - anytime, anywhere, using any device.  
https://www.cisco.com/c/en/us/products/security/adaptive-security-appliance-asa-software/index.html

## Prerequisites
McAfee ATD solution (tested with ATD 4.0.4)

Cisco ASA Firewall (tested with Cisco vASA 9.9) - make sure RestAPI is enabled

Requests ([Link](http://docs.python-requests.org/en/master/user/install/#install))

OpenDXL SDK ([Link](https://github.com/opendxl/opendxl-client-python))
```sh
git clone https://github.com/opendxl/opendxl-client-python.git
cd opendxl-client-python/
python setup.py install
```

McAfee ePolicy Orchestrator, DXL Broker

## Configuration
Enter the Cisco ASA ip, username and password in the asa.py file (line 77, 78, 79).

Enter a groupname that should be used for malicious IP addresses (asa.py - line 83).

<img width="313" alt="screen shot 2018-03-03 at 18 10 34" src="https://user-images.githubusercontent.com/25227268/36937086-4dad8518-1f0e-11e8-8c26-8954c37a85b7.png">

Create Certificates for OpenDXL ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epoexternalcertissuance.html)). 

Make sure that the FULL PATH to the config file is entered in line 17 (atd_subscriber.py).

## Process Description
McAfee ATD receives files from multiple sensors like Endpoints, Web Gateways, Network IPS or via Rest API. 
ATD will perform malware analytics and produce local threat intelligence. After an analysis every IOC will be published via the Data Exchange Layer (topic: /mcafee/event/atd/file/report). 

### atd_subscriber.py
The atd_subscriber.py receives DXL messages from ATD, filters out discovered IP's and loads asa.py.

### asa.py
The asa.py receives the discovered malicious IP's and will use API's to update Network Object Groups.

The script will:

1. create a new api session 
2. check if the network group exist already and create it if it doesn't
3. if the group exist already new discovered IP will be added to the network group

Don't forget to create a new Firewall rule related to the new created group.

<img width="871" alt="screen shot 2018-03-03 at 18 13 36" src="https://user-images.githubusercontent.com/25227268/36937109-a58e38ae-1f0e-11e8-9a14-558a632c4175.png">

## Run the OpenDXL wrapper
> python atd_subscriber.py

or

> nohup python atd_subscriber.py &

## Video

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Ovhn-Y97U5c/0.jpg)](https://www.youtube.com/watch?v=Ovhn-Y97U5c)

link: https://www.youtube.com/watch?v=Ovhn-Y97U5c

## Summary
With this use case, ATD produces local intelligence that is immediatly updating policy enforcement points like the 
Cisco ASA Firewalls with malicious IP's.
