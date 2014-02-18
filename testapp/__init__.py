from flask import Flask, jsonify
import _mysql
app = Flask(__name__)


@app.route("/")
def hello():
    return 'asdfadf'


@app.route("/constituency/<string:constituency>")
def const_info(constituency):
    db = _mysql.connect(host="localhost", user="ilwhack14", passwd="hackathon", db="ilwhack14")
    db.query('select m.name, m.surname, m.party, m.url from constituencies c, MSPs m where c.name="{constituency}" and c.name=m.constituency'.format(constituency=constituency))
    r = db.use_result()
    row = r.fetch_row()
    result = []
    while row:
        msp = {
            'name': row[0][0],
            'surname': row[0][1],
            'party': row[0][2],
            'url': row[0][3]
        }
        result += [msp]
        row = r.fetch_row()
    result = {'result':result}
    return jsonify(result)


if __name__ == "__main__":
    app.run()
