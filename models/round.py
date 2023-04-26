class Round:
    player_name: str
    course_name: str
    layout_name: str
    date: str
    total_strokes: int
    total_score: int
    hole_scores: list

    par: list
    cumulative_score: list
    num_holes: int

    def __init__(self, udisc_par_round):
        self.course_name = udisc_par_round[1]
        self.layout_name = udisc_par_round[2]
        self.date = udisc_par_round[3]
        self.total_strokes = int(udisc_par_round[4])
        self.par = get_hole_strokes(udisc_par_round)

    def set_player_stats(self, udisc_player_round):
        hole_strokes = get_hole_strokes(udisc_player_round)
        self.num_holes = len(hole_strokes)
        self.player_name = udisc_player_round[0]
        self.total_score = int(udisc_player_round[5])
        self.cumulative_score = []
        self.hole_scores = []
        last = 0
        for i in range(0, len(hole_strokes)):
            hole_score = hole_strokes[i] - self.par[i]
            self.hole_scores.append(hole_score)
            self.cumulative_score.append(last + hole_score)
            last = self.cumulative_score[i]

    def get_node(self, hole_index):
        return hole_index, self.cumulative_score[hole_index]


def get_hole_strokes(udisc_round):
    strokes = []
    for i in range(6, 33):  # for holes 1-27
        num_strokes = udisc_round[i]
        try:
            num_strokes = int(num_strokes)
            if num_strokes == 0:
                break  # 0 means last index was the final point
        except:
            break  # first exception means last index was the final point
        strokes.append(num_strokes)

    return strokes


def get_rounds(udisc_round, player_names):
    custom_rounds = []
    # initialize "Round" objects
    for round in udisc_round:
        if round[0] != "Par":
            continue

        custom_round = Round(round)
        custom_rounds.append(custom_round)

    # finalize "Round" objects
    for og_round in udisc_round:
        for name in player_names:
            if og_round[0] != name:
                continue
            for custom_round in custom_rounds:
                if custom_round.date == og_round[3]:
                    custom_round.set_player_stats(og_round)
                    break
    return custom_rounds
