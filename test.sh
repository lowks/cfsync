#!/bin/bash
. .env
./sync.py -h
./sync.py -u $RACKSPACE_USER -k $RACKSPACE_API_KEY devopsy-uat ~/repos/DevOpsy/_deploy/

