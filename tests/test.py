import qi
import random

# Definizione delle parole per il gioco
parole = ["cane", "gatto", "casa", "albero", "computer", "sole", "mare", "musica", "libro"]

class GuessWordGame:
    def __init__(self, session):
        self.session = session
        self.memory = self.session.service("ALMemory")
        self.dialog = self.session.service("ALDialog")
        self.word_to_guess = None

    def start_game(self):
        self.word_to_guess = random.choice(parole)
        self.memory.insertData("WordToGuess", self.word_to_guess)

        # Definizione del topic per il gioco
        topic_content = ("topic: ~guess_word_game()\n"
                         "language: english\n"
                         "concept:(WordToGuess) [{}]\n"
                         "u: (Guess) [I think it is {{WordToGuess}}]\n"
                         "u: (~stop_game) [Let's stop the game]\n"
                         "u: (Stop) OK, let's stop the game\n").format(self.word_to_guess)

        # Caricamento e attivazione del topic nel sistema di dialogo
        self.dialog.setLanguage("English")
        self.dialog.loadTopicContent(topic_content)
        self.dialog.activateTopic("~guess_word_game")

        # Avvio del gioco
        self.dialog.subscribe("guess_word_game")

    def stop_game(self):
        self.dialog.unsubscribe("guess_word_game")
        self.dialog.deactivateTopic("~guess_word_game")
        self.dialog.unloadTopic("~guess_word_game")

    def cleanup(self):
        self.stop_game()
        self.dialog.clearConcepts()

if __name__ == "__main__":
    # Connessione al robot Pepper
    connection_url = "tcp://localhost:63607"  # Modificare con l'IP di Pepper se necessario
    app = qi.Application(["GuessWordGame", "--qi-url=" + connection_url])
    app.start()
    session = app.session

    # Creazione e avvio del gioco
    game = GuessWordGame(session)
    game.start_game()

    try:
        app.run()
    except KeyboardInterrupt:
        print("Interruzione manuale")

    # Pulizia delle risorse alla fine del gioco
    game.cleanup()
    app.stop()