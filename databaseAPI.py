import flask
from flask import request, jsonify,json
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/v1/deleteBrand', methods=['DELETE'])
def delete_api():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    brand_id = cur.execute('select id from brand where id not in (select b.id from brand b,campaign c where b.id = c.brand_id);').fetchall()
   
    if not brand_id:
    	return "All Brands are having atleast one campaign."
    	
    query='delete from brand where id in (select id from brand where id not in (select b.id from brand b,campaign c where b.id = c.brand_id));'    
    
    querySelect='select * from brand where id in (select id from brand where id not in (select b.id from brand b,campaign c where b.id = c.brand_id));'
    cur.execute(query)
    conn.commit()
    results = cur.execute(querySelect).fetchall()
    if results:
    	return "Brand is not deleted."
    else:
    	return "Brand {} is deleted as this brand has no campaign.".format(brand_id)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run()
