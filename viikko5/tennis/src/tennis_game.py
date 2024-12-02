class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0
        self.score_names = ["Love", "Fifteen", "Thirty", "Forty"]

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.m_score1 += 1
        else:
            self.m_score2 += 1

    def get_score(self):
        score = ""
        temp_score = 0

        if self.m_score1 == self.m_score2:
            score = self.equal_scores()

        elif self.m_score1 >= 4 or self.m_score2 >= 4:
            score = self.over_forty()

        else:
            score = self.game_on()
        return score

    def equal_scores(self):
        if self.m_score1 < 3:
            return f"{self.score_names[self.m_score1]}-All"
        else:
            return "Deuce"

    def over_forty(self):
        self.states = [
            "",
            "Advantage player1",
            "Win for player1",
            "Win for player2",
            "Advantage player2",
        ]
        if (self.m_score1 - self.m_score2) > 0:
            return f"{self.states[min(2,self.m_score1-self.m_score2)]}"
        else:
            return f"{self.states[max(-2,self.m_score1-self.m_score2)]}"

    def game_on(self):
        return f"{self.score_names[self.m_score1]}-{self.score_names[self.m_score2]}"
