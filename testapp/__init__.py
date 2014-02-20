from flask import Flask, jsonify, request
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
def get_json(filename):
    return app.send_static_file(filename + '.json')
	
	
@app.route("/<filename>.ico")
def get_ico(filename):
    return app.send_static_file(filename + '.ico')


@app.route("/constituency/<string:constituency>")
def const_info(constituency):
    db = _mysql.connect(host="localhost", user="ilwhack14", passwd="hackathon", db="ilwhack14")
    db.query("""
        SELECT
            m.name,
            m.surname,
            m.party,
            m.url,
            AVG(d.rank2004+d.rank2006*4+d.rank2009*15+d.rank2012*30)/50/6505*100 AS rank,
            m.total_interventions,
            m.avg_intervention_len,
            m.total_mentions_of_constituency,
            m.interventions_with_mention,
            m.mentions_percentage_of_total_text,
            m.percentage_of_interventions_with_mention,
            m.id,
            GROUP_CONCAT(DISTINCT CONCAT("['", w.word, "',", w.weight, "]") SEPARATOR ', ')
        FROM constituencies c
        LEFT JOIN MSPs m ON c.name=m.constituency
        LEFT JOIN datazones d ON c.id = d.constituency
        LEFT JOIN MSP_words w ON w.MSP_id = m.id
        WHERE c.name="{constituency}"
        GROUP BY c.id
    """.format(constituency=constituency))
    r = db.use_result()
    row = r.fetch_row()
    result = []
    while row:
        msp = {
            'MSP_id': row[0][11],
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
            'percentage_of_interventions_with_mention': row[0][10],
            'words': "[{0}]".format(row[0][12]),
            'shit':1
        }
        result += [msp]
        row = r.fetch_row()
    result = {'result':result}
    return jsonify(result)


@app.route("/stats/", methods=['POST', 'GET'])
def get_stats():
    print(request.form.getlist('categories[]'))
    categories = request.form.getlist('categories[]')
    fields = {'c_id':'c.id', 'c_name':'c.name'}

    if ("rank" in categories) or (len(categories)==0):
        fields['rank']="AVG(d.rank2004+d.rank2006*4+d.rank2009*15+d.rank2012*30)/50/6505*100 AS rank"

    if ("total_interventions" in categories) or (len(categories)==0):
        fields['total_interventions']="AVG(m.total_interventions)"

    if ("avg_intervention_len" in categories) or (len(categories)==0):
        fields['avg_intervention_len']="AVG(m.avg_intervention_len)"

    if ("total_mentions_of_constituency" in categories) or (len(categories)==0):
        fields['total_mentions_of_constituency']="AVG(m.total_mentions_of_constituency)"

    if ("interventions_with_mention" in categories) or (len(categories)==0):
        fields['interventions_with_mention']="AVG(m.interventions_with_mention)"

    if ("mentions_percentage_of_total_text" in categories) or (len(categories)==0):
        fields['mentions_percentage_of_total_text']="AVG(m.mentions_percentage_of_total_text)"

    if ("percentage_of_interventions_with_mention" in categories) or (len(categories)==0):
        fields['percentage_of_interventions_with_mention']="AVG(m.percentage_of_interventions_with_mention)"

    db = _mysql.connect(host="localhost", user="ilwhack14", passwd="hackathon", db="ilwhack14")
    db.query("""
        SELECT
            {fields}
        FROM constituencies c
        LEFT JOIN MSPs m ON c.name=m.constituency
        LEFT JOIN datazones d ON c.id = d.constituency
        GROUP BY c.id
    """.format(fields=' , '.join(fields.values())))

    r = db.use_result()
    result = []
    row = r.fetch_row()

    while row:
        row = row[0]
        constituency = {}
        for (i, field) in enumerate(fields.keys()):
            constituency[field] = row[i]

        result += [constituency]
        row = r.fetch_row()

    result = {'result':result}
    return jsonify(result)


if __name__ == "__main__":
    app.run()
