from re import sub
import flask
import database_models as model

app = flask.Flask(__name__)


@app.route('/')
def route_root():
    return 'hello_world!'


@app.route('/subscribe', methods=['POST'])
def route_subscribe():
    req = flask.request.json
    url = req.get('url')
    subscriber = model.Subscriber.create(url=url)
    return flask.jsonify({
        'id': subscriber.id,
        'err': None
    })


@app.route('/unsubscribe', methods=['POST'])
def route_unsubscribe():
    req = flask.request.json
    id_ = req.get('id')
    subscriber = model.Subscriber.select().where(model.Subscriber.id == id_).get()
    subscriber.delete_instance()
    return flask.jsonify({
        'id': subscriber.id,
        'err': None
    })


@app.route('/get-category', methods=['POST'])
def route_get_catogory():
    req = flask.request.json
    id_ = req.get('id')
    category = model.Category.select().where(model.Category.id == id_).get()
    return flask.jsonify({
        'name': category.name,
        'err': None
    })


app.run(debug=True)
