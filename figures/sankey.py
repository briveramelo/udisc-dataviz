from collections import Counter

import plotly.graph_objects as go
from plotly.graph_objs.sankey import Node, Link

from models.round import Round
from utils.utils import get_color, normalize


class RoundGraphData:
    def __init__(self, round: Round):
        self.round = round
        self.nodes = []
        self.sources = []
        self.targets = []
        self.links = []
        for i in range(0, round.num_holes):
            source_node = (i + 1, round.cumulative_score[i])  # x, y = 1-indexed hole #, score
            self.nodes.append(source_node)
            if i + 1 < round.num_holes:
                self.sources.append(source_node)
                target_node = i + 2, round.cumulative_score[i + 1]
                self.targets.append(target_node)
                self.links.append((source_node, target_node))


class SankeyData:
    def __init__(self, rounds: list[RoundGraphData], title):
        self.rounds = rounds
        self.title = title

        # define nodes
        nodes = [node for round in rounds for node in round.nodes]
        node_counts = Counter(nodes)
        node_counts[(0, 0)] = 1

        # define x, y positions
        x, y = [node[0] for node in node_counts], [node[1] for node in node_counts]
        max_x, min_y, max_y = max(x), min(y), max(y)
        abs_max_y = max(abs(min_y), abs(max_y))
        x = [normalize(val, 0, max_x) for val in x]
        y = [normalize(-val, -abs_max_y, abs_max_y) for val in y]  # val needs to be (-) for expected outcome

        # define links
        link_counts = Counter()
        for round in rounds:
            for link in round.links:
                key = (link[0][0], link[0][1], link[1][0], link[1][1])
                link_counts[key] += 1
            hole1_score = round.round.hole_scores[0]
            link_counts[(0, 0, 1, hole1_score)] += 1  # link imaginary "hole 0" to hole 1 for opening branch effect

        link_keys = list(link_counts)
        labels = ["{},{}".format(node[0], node[1]) for node in node_counts]
        sources = [labels.index("{},{}".format(key[0], key[1])) for key in link_keys]
        targets = [labels.index("{},{}".format(key[2], key[3])) for key in link_keys]
        values = [link_counts[key] for key in link_keys]
        link_colors = [get_color(key[3] - key[1]) for key in link_keys]

        # adjust zoom outward with a hack to put two points off-screen with large height values
        zoom_val = 8 * max(values)  # consider making this slider adjustable?
        x_add, y_add, src_add, targ_add = 2, 0.5, len(x), len(x) + 1
        x.extend([x_add, x_add])
        y.extend([y_add, y_add])
        sources.extend([src_add, src_add])
        targets.extend([targ_add, targ_add])
        values.extend([zoom_val, zoom_val])

        # apply changes
        self.link = Link()
        self.link.source = sources
        self.link.target = targets
        self.link.value = values
        self.link.color = link_colors

        self.node = Node()
        self.node.label = labels
        self.node.color = 'rgba(100, 100, 100, 0.3)'
        self.node.x = x
        self.node.y = y


def get_figure(graph_data: SankeyData):
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=5,
            thickness=5,
            line=dict(color="black", width=0.5),
            label=graph_data.node.label,
            color="black",
            x=graph_data.node.x,
            y=graph_data.node.y,
        ),
        link=dict(
            source=graph_data.link.source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=graph_data.link.target,
            value=graph_data.link.value,
            color=graph_data.link.color,
        ),
        arrangement='snap',  # snap, perpendicular, freeform, fixed
    )])

    fig.update_layout(title_text=graph_data.title, font_size=10)
    return fig