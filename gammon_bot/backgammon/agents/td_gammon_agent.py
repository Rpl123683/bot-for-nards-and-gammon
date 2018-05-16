import numpy as np

class TDAgent(object):

    def __init__(self, player, model, p=0):
        self.player = player
        self.model = model
        self.name = 'TD-Gammon'
        self.p=p
    def get_action(self, actions, game):
        """
        Return best action according to self.evaluationFunction,
        with no lookahead.
        """
        v_best = 0
        a_best = None
        p=[]
        #print actions
        for a in actions:
            ateList = game.take_action(a, self.player)
            if self.player == game.players[0]:
                game.reverse()
                features = game.extract_features(game.opponent(self.player))
                v = 1.-self.model.get_output(features)[0][0]
                #print v
                game.reverse()
            else:
                features = game.extract_features(self.player)
                v = self.model.get_output(features)[0][0]
            #v = 1. - v if self.player == game.players[0] else v
            p.append(v)
            if v > v_best:
                v_best = v
                a_best = a
            game.undo_action(a, self.player, ateList)
        if np.random.rand()>=self.p:    
            return a_best
        else:
            p=p/sum(p)
            return list(actions)[np.random.choice(len(list(actions)),p=p)]
        