#!/usr/bin/env python
# coding: utf8

from ldap3 import Server, Connection, ALL

servername = 'ldap://172.28.4.103:389'
user = 'crm_test1'
password = 'syswin#'
base_dn = 'dc=syswin,dc=com'
#userinput = '600289'
userinput = '146997'
filter_field = "(&(|(cn=*%(input)s*)(sAMAccountName=*%(input)s*))(sAMAccountName=*))" % {
    'input': userinput}
attrs = ['sAMAccountName', 'mail', 'givenName', 'sn',
         'department', 'telephoneNumber', 'displayName']


class LdapConn(object):
    def __init__(self, servername, user, password):
        self.server = Server(servername)
        self.conn = Connection(servername, user=user,
                               password=password, auto_bind=True)

    def search_user(self, base_dn, filter_field, attrs):
        result = self.conn.search(base_dn, filter_field, attributes=attrs)
        if result:
            entry = self.conn.response[0]
            return entry
        return None

    def ldap_auth(self, dn, password):
        conn = Connection(self.server, user=dn, password=password,
                          check_names=True, lazy=False, raise_exceptions=False)
        conn.bind()
        return conn.result


if __name__ == "__main__":
    ldapobj = LdapConn(servername, user, password)
    entry = ldapobj.search_user(base_dn, filter_field, attrs)
    if entry:
        attr_dict = entry["attributes"]
        dn = entry["dn"]
        result = ldapobj.ldap_auth(dn, 'Wing!1234')
        if result["description"] == "success":
            print(
                (True, attr_dict["mail"], attr_dict["sAMAccountName"], attr_dict["givenName"]))
        else:
            print("auth fail")
