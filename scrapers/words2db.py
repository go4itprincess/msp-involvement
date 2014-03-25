import json
import _mysql

with open('data/msps_words.json', 'r') as content_file:
    content = json.loads(content_file.read())

db = _mysql.connect(host="d33028.mysql.zone.ee", user="d33028sa73662", passwd="Hackath0n", db="d33028sd72729")

words =[]
for person in content:
    q = "INSERT INTO `MSP_words` (`MSP_id`, `word`, `weight`)  VALUES "

    values = []

    for (word, weight) in person["top_words"]:
        values.append("('{0}', '{1}', '{2}' )".format(person["person_id"], word, weight))
        words.append(word)

    q += ' , '.join(values)

    if len(values)> 0:
        db.query(q)
    print(person['name'] + " OK!")
print(str(len(words)) + ' words added. Done')