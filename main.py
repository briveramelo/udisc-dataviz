import csv

from figures.sankey import SankeyData, RoundGraphData, get_figure
from models.round import get_rounds


def load_rounds(file_name, player_names):
    with open(file_name, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    return get_rounds(data, player_names)


def main():
    file_name = '/Users/brandonrivera-melo/Documents/Repos/udisc-dataviz/data/hector.csv'
    player_names = ["Hector", "Hector Rivera-Melo"]

    rounds = load_rounds(file_name, player_names)
    round_graph_data = [RoundGraphData(round) for round in rounds]
    graph_data = SankeyData(round_graph_data, "Hector Rivera-Melo Disc Golf Rounds 2022-2023")

    fig = get_figure(graph_data)
    fig.show()
    print("running")


if __name__ == '__main__':
    main()
