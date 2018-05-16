import numpy as np

class Today_bot(object):

    def __init__(self, player):
        self.player = player
        self.name = 'Today_bot'
        if self.player=="x":
            self.enemy="o"
        else:
            self.enemy="x"
    
    def home(self,grid):
        count=0
        home_part=grid[18:24]
        for i in home_part:
            if self.player in i:
                count+=len(i)
        return count
    
    
    
    def blots(self,grid):
        number_of_blots=0
        for i in grid:
            if self.player in i:
                if len(i)==1:
                    number_of_blots+=1
        return number_of_blots
    
    
    def blocks(self,grid):
        number_of_blocks=0
        for i in grid:
            if self.player in i:
                if len(i)>1:
                    number_of_blocks+=1
        return number_of_blocks
    
    
    def empty_home_slots(self,grid):
        count=0
        home_part=grid[18:24]
        for i in home_part:
            if self.player not in i:
                count+=1
        return count
    
    
    def get_action(self, actions, game):
        """
        Return best action according to self.evaluationFunction,
        with no lookahead.
        """
        v_best = 0
        a_best = None
        
        rm=False
        Race=False
        last_my=1
        last_enemy=0
        # understand if we are racing or fighting
        for i in range(len(game.grid)):
            if self.player in game.grid[i]:
                last_my=i
                break
        for i in range(len(game.grid))[::-1]:
            if game.opponent(self.player) in game.grid[i]:
                last_enemy=i
                break
        # understand if we are racing or fighting
        if last_my>last_enemy:
            rm=True
        if (game.bar_pieces.values()==[[], []])&(rm):
            Race=True
        
        
        # if race try this value function V
        if Race==True:
            for a in actions:
                ateList = game.take_action(a, self.player)
                v=500*len(game.off_pieces[self.player])+200*(self.home(game.grid))+100*(15-self.home(game.grid)-len(game.off_pieces[self.player]))
                if v > v_best:
                    v_best = v
                    a_best = a
                game.undo_action(a, self.player, ateList)
            return a_best
        
        # if not race another value function 
        else:
            for a in actions:
                ateList = game.take_action(a, self.player)
                v=700*len(game.bar_pieces[self.enemy])-400*len(game.bar_pieces[self.player])-200*self.blots(game.grid)+200*self.blocks(game.grid)+100*self.blocks(game.grid[18:24])+30*(self.home(game.grid))-100*self.empty_home_slots(game.grid)+200*len(game.off_pieces[self.player])+(15-self.home(game.grid)-len(game.off_pieces[self.player]))
                if v > v_best:
                    v_best = v
                    a_best = a
                game.undo_action(a, self.player, ateList)
            return a_best
