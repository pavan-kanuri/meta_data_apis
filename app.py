from flask import Flask
import routes

app = Flask(__name__)

app.register_blueprint(routes.meta_layer.m_layer, name="metalayerbase", url_prefix=routes.meta_layer.m_layer.url_prefix)
app.register_blueprint(routes.sku_layer.s_layer, name="skulayerbase", url_prefix=routes.sku_layer.s_layer.url_prefix)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,debug=True)