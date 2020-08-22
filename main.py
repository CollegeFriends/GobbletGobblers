from PyGobbletGobblers import GobbletGobblers as Game

if __name__ == '__main__':
    print("Start Game")
    
    game = Game()
    game.render('owner')

    side = 0
    while not game.isEnd():
        state = False
        print()
        if side == 0:
            print("-- 先手 ------------------------------")
        else:
            print("-- 後手 ------------------------------")

        while not state:
            cmd = int(input("行動を選択 [ 0 : Put / 1 : Move ] >> "))        
            if cmd == 0:
                size = int(input("置くコマのサイズ >> "))
                pos = int(input("置くコマの位置 >> "))
                state = game.putPiece(side,size,pos)

            if cmd == 1:            
                fromPos = int(input("動かすコマの位置 >> "))
                toPos = int(input("移動先 >> "))
                state = game.movePiece(side,fromPos,toPos)

        
        if side == 0:
            side = 1
        else:
            side = 0
        
        game.render('owner')

    