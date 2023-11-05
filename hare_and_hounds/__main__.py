import logging
from hare_and_hounds.game_logic.actor_player import ActorPlayer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("__main__.py").info("Project has run")
    ActorPlayer().run()
