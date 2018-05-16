import os
import copy
import time
import random
import numpy as np

def parse_rolls(name):
    with open(name,"r") as file:  
        data = file.read()
    data=data.split("\n")
    del data[-1]
    d=[]
    for i in data:
        d.append([int(i[0]),int(i[1])])
    return d
class Game:

    LAYOUT = "0-15-o,12-15-x"
    NUMCOLS = 24
    QUAD = 6
    OFF = 'off'
    ON = 'on'
    TOKENS = ['x', 'o']

    def __init__(self, layout=LAYOUT, grid=None, off_pieces=None, bar_pieces=None, num_pieces=None, players=None):
        """
        Define a new game object
        """
        
        self.die = Game.QUAD
        self.layout = layout
        if grid:
            self.grid = copy.deepcopy(grid)
            self.off_pieces = copy.deepcopy(off_pieces)
            self.bar_pieces = copy.deepcopy(bar_pieces)
            self.num_pieces = copy.deepcopy(num_pieces)
            self.players = players
            return
        self.players = Game.TOKENS
        self.grid = [[] for _ in range(Game.NUMCOLS)]
        self.off_pieces = {}
        self.bar_pieces = {}
        self.num_pieces = {}
        self.turn_counter=0
        self.roll_history=[]
        self.possible_steps_history=[]
        #self.turn_player=[]
        self.gone_states=[]
        self.choosen_move=[]
        for t in self.players:
            self.bar_pieces[t] = []
            self.off_pieces[t] = []
            self.num_pieces[t] = 0
        
    
    
    
    
    def home(self,player):
        count=0
        home_part=self.grid[18:24]
        for i in home_part:
            if player in i:
                count+=len(i)
        return count
    
    def till_end(self,player):
        total=0
        for i in range(len(self.grid)):
            if player in self.grid[i]:
                total+=(24-i)*len(self.grid[i])
        return total
    
    
    
    def longest_block(self,player):
        longest=0
        self.reverse()
        for i in range(24):
            if player in self.grid[i]:
                counter=1
                for j in range(i+1,len(self.grid)):
                    if player in self.grid[j]:
                        counter+=1
                    else:
                        break
                if longest<counter:
                    try:
                        for k in range(i,-1,-1):
                            if self.opponent(player) in self.grid[k]:
                                longest=counter
                                break
                    except:
                        continue
        self.reverse()                
        return longest
    
    
    
    def blocks(self,player):
        number_of_blocks=0
        for i in self.grid:
            if player in i:
                number_of_blocks+=1
        return number_of_blocks
    
    
    
    def Race(self,player):
        rc=1
        last_my=23
        for i in range(len(self.grid)):
            if player in self.grid[i]:
                last_my=i
                break
        for j in range(last_my+1,len(self.grid)):
                    if self.opponent(player) in self.grid[j]:
                        rc=0
        return rc
    
    
    def longest_block_qual(self,player):
        ar=np.concatenate((np.arange(12,24),np.arange(12)))
        best=0
        self.reverse()
        for i in range(24):
            if player in self.grid[i]:
                length=1
                for j in range(i+1,len(self.grid)):
                    if player in self.grid[j]:
                        length+=1
                    else:
                        break
                try:
                    current_amount_of_blocked=0
                    current_block_place=ar[i]
                    for k in range(i,-1,-1):
                        if self.opponent(player) in grid[k]:
                            current_amount_of_blocked+=len(grid[k])
                except:
                    continue
                if length<=6:        
                    if best<(length**2)*np.sqrt(current_amount_of_blocked)*current_block_place:
                        best=(length**2)*np.sqrt(current_amount_of_blocked)*current_block_place
                else:
                    length=6
                    if best<(length**2)*np.sqrt(current_amount_of_blocked)*current_block_place:
                        best=(length**2)*np.sqrt(current_amount_of_blocked)*current_block_place 
        self.reverse()
        return best
    
        
        
        #self.turn=0
        #self.rols=parse_rolls("logs-out/_narde_neural_log_NONE_1_roll.txt")
    @staticmethod
    def new():
        game = Game()
        game.reset()
        return game

    def extract_features(self, player):
        features = []
        for p in self.players:
            for col in self.grid:
                feats = [0.] * 15
                if len(col) > 0 and col[0] == p:
                    for i in range(len(col)):
                        feats[min(i, 14)] += 1
                features += feats
            for i in range(len(self.off_pieces[p])):
                features.append(1)
            for i in range(15-len(self.off_pieces[p])):
                features.append(0)
        features.append(self.home(player))
        features.append(self.till_end(player))
        features.append(self.longest_block(player))
        features.append(self.blocks(player))
        features.append(self.Race(player))
        features.append(self.longest_block_qual(player))
            #features.append(float(len(self.bar_pieces[p])) / 2.)
            #features.append(float(len(self.off_pieces[p])) / self.num_pieces[p])
        #if player == self.players[0]:
            #features += [1., 0.]
        #else:
            #features += [0., 1.]
        return np.array(features).reshape(1, -1)

    def roll_dice(self):
        if self.turn_counter==0:
            t=(random.randint(1, self.die), random.randint(1, self.die))
            while t[0]==t[1]:
                t=(random.randint(1, self.die), random.randint(1, self.die))
            return t
        else:
            return (random.randint(1, self.die), random.randint(1, self.die))
        #try:
            #return tuple(self.rols[self.turn-1])
        #except:
            #return (random.randint(1, self.die), random.randint(1, self.die))
        
        
        
    def play(self, players, draw=False):
        player_num = random.randint(0, 1)
        
        if player_num==0:
            self.reverse()
        while not self.is_over():
            self.next_step(players[player_num], player_num, draw=draw)
            player_num = (player_num + 1) % 2
        return self.winner()

    def next_step(self, player, player_num, draw=False):
        roll = self.roll_dice()
        self.roll_history.append(roll)
        if draw:
            if player_num==0:
                self.reverse()
            self.draw()
            if player_num==0:
                self.reverse()

        self.take_turn(player, roll, draw=draw)
        self.turn_counter+=1
    def take_turn(self, player, roll, draw=False):
        if draw:
            print(self.turn_counter)
            print("Player %s rolled <%d, %d>." % (player.player, roll[0], roll[1]))
            #time.sleep(1)

        moves = self.get_actions(roll, player.player, nodups=True)
        #print(moves)
        self.possible_steps_history.append(moves)
        move = player.get_action(moves, self) if moves else None
        #print(move)
        self.choosen_move.append(move)
        self.gone_states.append(self.extract_features(player))
        #self.turn_player.append(player)
        if move:
            self.take_action(move, player.player)
        self.reverse()
    def clone(self):
        """
        Return an exact copy of the game. Changes can be made
        to the cloned version without affecting the original.
        """
        return Game(None, self.grid, self.off_pieces,
                    self.bar_pieces, self.num_pieces, self.players)

    def take_action(self, action, token):
        """
        Makes given move for player, assumes move is valid,
        will remove pieces from play
        """
        ateList = [0] * 4
        for i, (s, e) in enumerate(action):
            if s == Game.ON:
                piece = self.bar_pieces[token].pop()
            else:
                piece = self.grid[s].pop()
            if e == Game.OFF:
                self.off_pieces[token].append(piece)
                continue
            if len(self.grid[e]) > 0 and self.grid[e][0] != token:
                bar_piece = self.grid[e].pop()
                self.bar_pieces[bar_piece].append(bar_piece)
                ateList[i] = 1
            self.grid[e].append(piece)
        return ateList

    def undo_action(self, action, player, ateList):
        """
        Reverses given move for player, assumes move is valid,
        will remove pieces from play
        """
        for i, (s, e) in enumerate(reversed(action)):
            if e == Game.OFF:
                piece = self.off_pieces[player].pop()
            else:
                piece = self.grid[e].pop()
                if ateList[len(action) - 1 - i]:
                    bar_piece = self.bar_pieces[self.opponent(player)].pop()
                    self.grid[e].append(bar_piece)
            if s == Game.ON:
                self.bar_pieces[player].append(piece)
            else:
                self.grid[s].append(piece)
    def clean(self,moves,roll):
        if not (self.turn_counter<2)&(roll in [(3,3),(4,4),(6,6)]):
            dlist=[]
            for i in moves:
                zeros_counter=0
                for j in i:
                    if j[0]==0:
                        zeros_counter+=1
                    if zeros_counter>=2:
                        dlist.append(i)
            for i in dlist:
                moves.discard(i)
        else:
            dlist=[]
            for i in moves:
                zeros_counter=0
                for j in i:
                    if j[0]==0:
                        zeros_counter+=1
                    if zeros_counter>=3:
                        dlist.append(i)
            for i in dlist:
                moves.discard(i)
        return moves

    def get_actions(self, roll, player, nodups=False):
        """
        Get set of all possible move tuples
        """
        moves = set()
        if nodups:
            start = 0
        else:
            start = None

        r1, r2 = roll
        if r1 == r2: # doubles
            i = 4
            # keep trying until we find some moves
            while not self.clean(moves,roll) and i > 0:
                self.find_moves(tuple([r1]*i), player, (), moves, start)
                i -= 1
        else:
            self.find_moves(roll, player, (), moves, start)
            self.find_moves((r2, r1), player, (), moves, start)
            # has no moves, try moving only one piece
            if not self.clean(moves,roll):
                if r1>r2:
                    self.find_moves((r1, ), player, (), moves, start)
                    if not self.clean(moves,roll):
                        self.find_moves((r2, ), player, (), moves, start)
                else:
                    self.find_moves((r2, ), player, (), moves, start)
                    if not self.clean(moves,roll):
                        self.find_moves((r1, ), player, (), moves, start)
                #for r in roll:
                   # self.find_moves((r, ), player, (), moves, start)
        if self.opponent(player) not in str(self.grid[6:12]):
            mv=self.clean(moves,roll)
            for_del=[]
            for i in mv:
                atl=self.take_action(i,player)
                max_count_block=0
                self.reverse()
                for j in range(24):
                    if player in self.grid[j]:
                        count=1
                        k=j+1
                        if k<24:
                            while player in self.grid[k]:
                                count+=1
                                k+=1
                                if k==24:
                                    break
                            if count>max_count_block:
                                max_count_block=count
                self.reverse()
                self.undo_action(i,player, atl)
                if max_count_block>=6:
                    for_del.append(i)
            for i in for_del:
                mv.discard(i)
            return mv
        else:
            return  self.clean(moves,roll)
        #print moves
        
        
    def find_moves(self, rs, player, move, moves, start=None):
        if len(rs)==0:
            moves.add(move)
            return
        r, rs = rs[0], rs[1:]
        # see if we can remove a piece from the bar


        # otherwise check each grid location for valid move using r
        offboarding = self.can_offboard(player)

        for i in range(len(self.grid)):
            if start is not None:
                start = i
            if self.is_valid_move(i, i + r, player):

                piece = self.grid[i].pop()
                bar_piece = None
                if len(self.grid[i+r]) == 1 and self.grid[i+r][-1] != player:
                    bar_piece = self.grid[i + r].pop()
                self.grid[i + r].append(piece)
                self.find_moves(rs, player, move + ((i, i + r), ), moves, start)
                self.grid[i + r].pop()
                self.grid[i].append(piece)
                if bar_piece:
                    self.grid[i + r].append(bar_piece)

            # If we can't move on the board can we take the piece off?
            if offboarding and self.remove_piece(player, i, r):
                piece = self.grid[i].pop()
                self.off_pieces[player].append(piece)
                self.find_moves(rs, player, move + ((i, Game.OFF), ), moves, start)
                self.off_pieces[player].pop()
                self.grid[i].append(piece)

                
                
                
    def is_valid_block(self,start,end,player):
        before=False
        after=False
        if self.opponent(player) in str(self.grid[6:12]):
            return True
        else:
            t=copy.deepcopy(self.grid)
            t[start].pop()
            if (self.opponent(player) in str(t[end+1:end+6]))or("[]" in str(t[end+1:end+6])):
                after=True
            if (self.opponent(player) in str(t[end-5:end]))or("[]" in str(t[end-5:end])):
                before=True
            return before&after
                
    def opponent(self, token):
        """
        Retrieve opponent players token for a given players token.
        """
        for t in self.players:
            if t != token:
                return t

    def is_won(self, player):
        """
        If game is over and player won, return True, else return False
        """
        return self.is_over() and player == self.players[self.winner()]

    def is_lost(self, player):
        """
        If game is over and player lost, return True, else return False
        """
        return self.is_over() and player != self.players[self.winner()]

    def reverse(self):
        """
        Reverses a game allowing it to be seen by the opponent
        from the same perspective
        """
        #self.grid.reverse()
        self.grid=self.grid[12:]+self.grid[:12]
        #self.players.reverse()

    def reset(self):
        """
        Resets game to original layout.
        """
        for col in self.layout.split(','):
            loc, num, token = col.split('-')
            self.grid[int(loc)] = [token for _ in range(int(num))]
        for col in self.grid:
            for piece in col:
                self.num_pieces[piece] += 1

    def winner(self):
        """
        Get winner.
        """
        return 0 if len(self.off_pieces[self.players[0]]) == self.num_pieces[self.players[0]] else 1

    def is_over(self):
        """
        Checks if the game is over.
        """
        for t in self.players:
            if len(self.off_pieces[t]) == self.num_pieces[t]:
                return True
        return False

    def can_offboard(self, player):
        count = 0
        for i in range(Game.NUMCOLS - self.die, Game.NUMCOLS):
            if len(self.grid[i]) > 0 and self.grid[i][0] == player:
                count += len(self.grid[i])
        if count+len(self.off_pieces[player]) == self.num_pieces[player]:
            return True
        return False

    def can_onboard(self, player, r):
        """
        Can we take a players piece on the bar to a position
        on the grid given by roll-1?
        """
        if len(self.grid[r - 1]) <= 0 or self.grid[r - 1][0] == player:
            return True
        else:
            return False

    def remove_piece(self, player, start, r):
        """
        Can we remove a piece from location start with roll r ?
        In this function we assume we are cool to offboard,
        i.e. no pieces on the bar and all are in the home quadrant.
        """
        if start < Game.NUMCOLS - self.die:
            return False
        if len(self.grid[start]) == 0 or self.grid[start][0] != player:
            return False
        if start + r == Game.NUMCOLS:
            return True
        if start + r > Game.NUMCOLS:
            for i in range(start - 1, Game.NUMCOLS - self.die - 1, -1):
                if len(self.grid[i]) != 0 and self.grid[i][0] == player:
                    return False
            return True
        return False

    def is_valid_move(self, start, end, token):
        if len(self.grid[start]) > 0 and self.grid[start][0] == token:
            if end < 0 or end >= len(self.grid):
                return False
            if len(self.grid[end]) <= 0:
                #if self.is_valid_block(start,end, token):
                return True
            if len(self.grid[end]) >= 1 and self.grid[end][-1] == token:
                return True
        return False

    def draw_col(self,i,col):
        print "|",
        if i==-2:
            if col<10:
                print "",
            print str(col),
        elif i==-1:
            print "--",
        elif len(self.grid[col])>i:
            print " "+self.grid[col][i],
        else:
            print "  ",

    def draw(self):
        os.system('clear')
        largest = max([len(self.grid[i]) for i in range(len(self.grid)/2,len(self.grid))])
        for i in range(-2,largest):
            for col in range(len(self.grid)/2,len(self.grid)):
                self.draw_col(i,col)
            print "|"
        print
        print
        largest = max([len(self.grid[i]) for i in range(len(self.grid)/2)])
        for i in range(largest-1,-3,-1):
            for col in range(len(self.grid)/2-1,-1,-1):
                self.draw_col(i,col)
            print "|"
        for t in self.players:
            print "<Player %s>  Off Board : "%(t),
            for piece in self.off_pieces[t]:
                print t+'',
            print "   Bar : ",
            for piece in self.bar_pieces[t]:
                print t+'',
            print
