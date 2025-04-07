import getData

class Scoreboard:
    def __init__(self):
        pass

    def get_highscores(self):
        """Holt die Highscores aus der Datenbank."""
        return getData.get_highscore()

    def submit_highscore(self, name, score):
        """Speichert einen neuen Highscore in der Datenbank."""
        getData.set_highscore(name, score)