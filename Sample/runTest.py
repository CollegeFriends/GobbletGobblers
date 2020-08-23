import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyGobbletGobblers import GobbletGobblers as Game
import enemy
logger.info("import OK")


if __name__ == '__main__':
    print("Start Game")    

    cnt_0 = 0
    cnt_1 = 0

    for i in range(10000):
        game = Game(enbaleRender=False)
        enemy1 = enemy.randomBot(game,side = 0)    
        enemy2 = enemy.randomBot(game,side = 1)
        # game.render('owner')
        side = 0    
        while not game.isEnd():
            state = False
            if side == 0:
                enemy1.act()
            else:
                enemy2.act()
                
            # game.render('owner')

            if side == 0:            
                side = 1
            else:
                side = 0
        
        winner = game.getWinner()
        if winner == 0:
            cnt_0 += 1
        else:
            cnt_1 += 1

    print(cnt_0,cnt_1)