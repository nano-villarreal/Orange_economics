import flask
from flask import render_template
import io
from flask import Response, request

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from service import get_no_oil_commodities_figure, get_oil_figure, commodities_no_oil

app = flask.Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='template')

app.config["DEBUG"] = True

@app.route("/")
def home():
    return render_template("index.html", commodities=commodities_no_oil)


@app.route('/get_commodities_figure')
def plot_commodities_figure_png():
   fig = get_no_oil_commodities_figure(what_commodity=request.args.get('com'))
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)
   return Response(output.getvalue(), mimetype='image/png')


@app.route('/get_oil_figure')
def plot_oil_figure_png():
   fig = get_oil_figure()
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)
   return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)