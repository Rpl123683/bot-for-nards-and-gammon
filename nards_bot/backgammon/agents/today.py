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
    
    def till_end(self,grid):
        total=0
        for i in range(len(grid)):
            if self.player in grid[i]:
                total+=(24-i)*len(grid[i])
        return total
    
                            
    
    
    def longest_block(self,game):
        longest=0
        game.reverse()
        for i in range(24):
            if self.player in game.grid[i]:
                counter=1
                for j in range(i+1,len(game.grid)):
                    if self.player in game.grid[j]:
                        counter+=1
                    else:
                        break
                if longest<counter:
                    try:
                        for k in range(i,-1,-1):
                            if game.opponent(player) in game.grid[k]:
                                longest=counter
                                break
                    except:
                        continue
        game.reverse()                
        return longest
    
    
    
    
    
    
    
    
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
        v_best = -1000
        a_best = None
        
        rm=False
        Race=True
        last_my=0
        last_enemy=0
        # understand if we are racing or fighting
        for i in range(len(game.grid)):
            if self.player in game.grid[i]:
                last_my=i
                break
        for j in range(last_my+1,len(game.grid)):
            if self.enemy in game.grid[j]:
                Race=False
                break
        # understand if we are racing or fighting
        
        
        # if race try this value function V
        if Race==True:
            for a in actions:
                ateList = game.take_action(a, self.player)
                v=500*len(game.off_pieces[self.player])+2*(self.home(game.grid))+(15-self.home(game.grid)-len(game.off_pieces[self.player]))
                if v > v_best:
                    v_best = v
                    a_best = a
                game.undo_action(a, self.player, ateList)
            return a_best
        
        # if not race another value function 
        else:
            for a in actions:
                ateList = game.take_action(a, self.player)
         #      v=700*len(game.bar_pieces[self.enemy])-400*len(game.bar_pieces[self.player])-200*self.blots(game.grid)+200*self.blocks(game.grid)+100*self.blocks(game.grid[18:24])+30*(self.home(game.grid))-100*self.empty_home_slots(game.grid)+200*len(game.off_pieces[self.player])+(15-self.home(game.grid)-len(game.off_pieces[self.player]))
                v=400*self.blocks(game.grid)+30*(self.home(game.grid))+10*(24*15-self.till_end(game.grid))+400*self.longest_block(game)
                if v > v_best:
                    v_best = v
                    a_best = a
                game.undo_action(a, self.player, ateList)
            return a_best
