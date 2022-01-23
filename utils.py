import csv

kerberos_data = {}

def reload():
    global kerberos_data
    kerberos_data = {}
    with open('kerberos.csv', newline='') as f:
        sheet = csv.reader(f, delimiter=',')
        for s in sheet:
            kerberos_data[s[0]] = s[1]

reload()