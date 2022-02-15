import csv

kerberos_data = {}
batchlist = {}

def reload():
    global kerberos_data
    kerberos_data = {}
    with open('kerberos.csv', newline='') as f:
        sheet = csv.reader(f, delimiter=',')
        for s in sheet:
            kerberos_data[s[0]] = {"Name":s[1],"Hostel":s[2]}
    
    global batchlist
    batchlist = {}
    with open('batchlist.csv', newline='') as f:
        sheet = csv.reader(f, delimiter=',')
        for s in sheet:
            batchlist[s[0]] = s[1]

reload()