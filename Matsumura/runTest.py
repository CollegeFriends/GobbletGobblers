import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from READ_ONLY.PyGobbletGobblers import GobbletGobblers as Game
import AI
logger.info("import OK")


if __name__ == '__main__':
    print("Start Game")    

    cnt_0 = 0
    cnt_1 = 0

    for i in range(10000):
        game = Game(enbaleRender=False)
        enemy1 = AI.randomBot(game,side = 0)    
        enemy2 = AI.randomBot(game,side = 1)

        while not game.isEnd():            
            enemy1.act()
            if game.isEnd():
                break
            enemy2.act()                        
        
        winner = game.getWinner()
        if winner == 0:
            cnt_0 += 1
        else:
            cnt_1 += 1

    print(cnt_0,cnt_1)