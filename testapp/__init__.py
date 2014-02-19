from flask import Flask, jsonify
import _mysql
app = Flask(__name__)


@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/<filename>.css")
def get_css(filename):
    return app.send_static_file(filename + '.css')


@app.route("/<filename>.js")
def get_js(filename):
    return app.send_static_file(filename + '.js')


@app.route("/constituency/<string:constituency>")
def const_info(constituency):
    db = _mysql.connect(host="localhost", user="ilwhack14", passwd="hackathon", db="ilwhack14")
    db.query("""
        SELECT
            m.name,
            m.surname,
            m.party,
            m.url,
            SUM(d.rank2004+d.rank2006*4+d.rank2009*15+d.rank2012*30)/COUNT(*)/50/6505*100 AS rank
        FROM constituencies c
        LEFT JOIN MSPs m ON c.name=m.constituency
        LEFT JOIN datazones d ON c.id = d.constituency
        WHERE c.name="Ayr"
        GROUP BY c.id
    """.format(constituency=constituency))
    r = db.use_result()
    row = r.fetch_row()
    result = []
    while row:
        msp = {
            'name': row[0][0],
            'surname': row[0][1],
            'party': row[0][2],
            'url': row[0][3],
            'rank_c': row[0][4] 
        }
        result += [msp]
        row = r.fetch_row()
    result = {'result':result}
    return jsonify(result)


if __name__ == "__main__":
    app.run()
