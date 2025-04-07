class Score:
    def __init__(self):
        self.score = 0

    def increase(self):
        self.score += 1

    def get(self):
        return self.score