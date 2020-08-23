import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyGobbletGobblers import GobbletGobblers as Game
logger.info("import OK")

if __name__ == '__main__':
    game = Game()
    print(game.getPieces(0))


