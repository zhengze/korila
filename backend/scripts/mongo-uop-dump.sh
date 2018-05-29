#!/bin/bash

# dump mongodb data

mongodump --host 172.28.26.201:28010 -uadmin -p123456 -duop --authenticationDatabase=admin -o uopdbdata_`date +"%Y_%m_%d_%H%M%S"`
#mongodump --host 172.28.50.152:28010 -uadmin -p123456 -duop --authenticationDatabase=admin -o uopdbdata_`date +"%Y_%m_%d_%H%M%S"`
#mongodump --host 172.28.26.201:28010 -uadmin -p123456 -duop -c $1 --query='{"username":"super_admin"}' --authenticationDatabase=admin -o uopdbdata
