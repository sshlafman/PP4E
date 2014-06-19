from make_db_file import loadDbase
db = loadDbase()
for key in db:
    print(key, "=>", db[key])
print(db['sue']['name']) 
