class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accpets = accepts

nfaStates = []
nfaAlphabet = []
nfaTransitions = []
nfaStart = ""
nfaAccepts = [] 

nfaExample = NFA(nfaStates, nfaAlphabet, nfaTransitions, nfaStart, nfaAccepts)


