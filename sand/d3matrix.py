from . import io as io
from . import time as t
from IPython.display import IFrame, display, HTML
import json
import os
import shutil


def _vertex_to_dict(v):
    node = {'id': v.index}
    node.update(v.attributes())
    return node


def vertices_to_dicts(g):
    return list(map(lambda v: _vertex_to_dict(v), g.vs))


def _edge_to_dict(e):
    edge = {'source': e.source, 'target': e.target}
    edge.update(e.attributes())
    return edge


def edges_to_dicts(g):
    return list(map(lambda e: _edge_to_dict(e), g.es))


# Given an IGraph, produce json in the format matrix.js expects:
# {
#    "nodes":[
#              {"label":"node1","group":1},
#              {"label":"node2","group":2},
#              {"label":"node3","group":2},
#              {"label":"node4","group":3}],
#    "edges":[
#              {"source":2,"target":1,"weight":1},
#              {"source":0,"target":2,"weight":3}]
# }
def _to_json(g, title, description, scale, date):
    nodes = vertices_to_dicts(g)
    edges = edges_to_dicts(g)
    data = {'nodes': nodes,
            'edges': edges,
            'title': title,
            'description': description,
            'scale': scale,
            'date': date}
    return json.dumps(data)


def write_site(g, title, description, output_root_dir, scale=400):
    site_name = "{}_{}".format(io.legalize(title), t.seconds_since_epoch())
    output_dir = "{}/{}".format(output_root_dir, site_name)
    os.mkdir(output_dir)

    network = _to_json(g, title, description, scale, t.now())
    json_output_path = '{}/{}'.format(output_dir, 'network.json')
    io.write_file(json_output_path, network)

    vendor_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    for file in ('index.html', 'matrix.js', 'matrix.css', 'd3.v3.min.js'):
        shutil.copy2(os.path.join(vendor_path, "../templates/{}".format(file)), "{}/{}".format(output_dir, file))

    return output_dir


def matrix(g, title, description, output_root_dir='figure', scale=400):
    site_dir = write_site(g, title, description, output_root_dir, scale)
    html_output_path = "{}/{}".format(site_dir, 'index.html')
    return (site_dir, html_output_path)


def matrix_frame(html_output_path, scale=400):
    return IFrame(html_output_path, width="100%", height=scale)


def show(link):
    display(HTML("<a href='" + link + "' target='_blank'>Open in new window</a>"))
