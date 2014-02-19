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


@app.route("/<filename>.json")
def get_js(filename):
    return app.send_static_file(filename + '.json')


@app.route("/constituency/<string:constituency>")
def const_info(constituency):
    db = _mysql.connect(host="localhost", user="ilwhack14", passwd="hackathon", db="ilwhack14")
    db.query("""
        SELECT
            m.name,
            m.surname,
            m.party,
            m.url,
            SUM(d.rank2004+d.rank2006*4+d.rank2009*15+d.rank2012*30)/COUNT(*)/50/6505*100 AS rank,
            m.total_interventions,
            m.avg_intervention_len,
            m.total_mentions_of_constituency,
            m.interventions_with_mention,
            m.mentions_percentage_of_total_text,
            m.percentage_of_interventions_with_mention
        FROM constituencies c
        LEFT JOIN MSPs m ON c.name=m.constituency
        LEFT JOIN datazones d ON c.id = d.constituency
        WHERE c.name="{constituency}"
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
            'rank_c': row[0][4],
            'total_interventions': row[0][5],
            'avg_intervention_len': row[0][6],
            'total_mentions_of_constituency': row[0][7],
            'interventions_with_mention' : row[0][8],
            'mentions_percentage_of_total_text': row[0][9],
            'percentage_of_interventions_with_mention': row[0][10]
        }
        result += [msp]
        row = r.fetch_row()
    result = {'result':result}
    return jsonify(result)


if __name__ == "__main__":
    app.run()
