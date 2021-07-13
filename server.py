import flask
import tarfile
import os
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w") as tar:  # "w:gz" instead of "w" for tar.gz compressed file
        tar.add(source_dir, arcname=os.path.sep)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>Go to %s[table_name]/[simulation_id]</h1>" % flask.request.url_root, 404

@app.route('/<table>/<int:sim_id>')
def get_dir(table, sim_id):
    output_filename = '{table}_{id}.tar'.format(table=table, id=str(sim_id))  # add .gz to file if you want .tar.gz compressed file
    source_dir = '/bags/{table}/{id}'.format(table=table, id=str(sim_id))  # in the container
    if not os.path.isdir(source_dir):
        return "<h1>The directory doesn't exist!</h1>", 404
    make_tarfile(output_filename, source_dir)
    @flask.after_this_request
    def remove_file(response):
        os.remove(output_filename)
        return response
    return flask.send_file(output_filename)


@app.route('/check/<table>/<int:sim_id>')
def check_dir(table, sim_id):
    source_dir = f'/bags/{table}/{sim_id}'
    if os.path.isdir(source_dir):
        return "1"
    else:
        return "0", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
