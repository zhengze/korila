#!/usr/bin/env python
#coding: utf8

from ldap3 import Server, Connection, ALL

class LdapConn(object):
    def __init__(self):
        pass
    
    def conn(self):
        pass
        

if __name__ == "__main__":
    servername = 'ldap://172.28.4.103:389'
    server = Server(servername)
    #print(server)
    user = 'crm_test1'
    password = 'syswin#'
    base_dn = 'dc=syswin,dc=com'
    userinput = '600408'
    filter_field = "(&(|(cn=*%(input)s*)(sAMAccountName=*%(input)s*))(sAMAccountName=*))" %{'input': userinput}
    attrs = ['sAMAccountName', 'mail', 'givenName', 'sn', 'department', 'telephoneNumber', 'displayName']
    conn = Connection(servername, user=user, password=password, auto_bind=True)
    conn.search(base_dn, filter_field, attributes=attrs)
    
    print(conn.entries)
    entries = conn.entries
    for entry in entries:
        print(entry.entry_to_json())
    
    
