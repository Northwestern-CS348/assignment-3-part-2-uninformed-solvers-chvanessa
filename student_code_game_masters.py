from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        lst1 = []
        lst2 = []
        lst3 = []
        tuplst =[]

        gs_facts = self.kb.facts
        # print('the facts!', gs_facts)
        for f in gs_facts:
            # Handling "on" facts
            pred = f.statement.predicate
            t = f.statement.terms
            if pred == 'on':
                dnum = int(str(t[0])[4]) # Had to convert the term into a string, then index
                pnum = int(str(t[1])[3])
                if pnum == 1:
                    lst1.append(dnum)
                if pnum == 2:
                    lst2.append(dnum)
                if pnum  == 3:
                    lst3.append(dnum)

        rep_lst = [lst1, lst2, lst3]

        # some sort of sorting thing here
        for l in rep_lst:
            l.sort(reverse=False)
            l = tuple(l)
        for l in rep_lst:
            tuplst.append(tuple(l))
        ans = tuple(tuplst)
        # print('DID I DO IT', ans)
        return ans

        # fact: (on disk1 peg1)
        # fact: (on disk2 peg1)
        # fact: (on disk3 peg1)

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if movable_statement.predicate != 'movable': print('sos something is wrong')
        else:
            [d,p1,p2] = movable_statement.terms

            # Remove old onTopOf statements, fact: (onTopOf disk1 disk2)
            OTOtwo = parse_input("fact: (onTopOf " + str(d) + " " + "disk2)")
            OTOthree = parse_input("fact: (onTopOf " + str(d) + " " + "disk3)")
            if OTOtwo in self.kb.facts:
                self.kb.kb_retract(OTOtwo)
            if OTOthree in self.kb.facts:
                self.kb.kb_retract(OTOthree)

            # Moved from initial peg
            oldfact = parse_input("fact: (on " + str(d) + " " + str(p1) + ")")
            self.kb.kb_retract(oldfact)

            # Moved to final peg
            newon = parse_input("fact: (on " + str(d) + " " + str(p2) + ")")
            self.kb.kb_assert(newon)

            ### DID NOT CHANGE ONTOPOF FACTS

            # Retract fact: (top d peg1)
            oldtop = parse_input("fact: (top " + str(d) + " " + str(p1) + ")")
            self.kb.kb_retract(oldtop)

            # Add fact: (top d peg2)
            newtop = parse_input("fact: (top " + str(d) + " " + str(p2) + ")")
            self.kb.kb_assert(newtop)

            # Retract from knowledge base if it was the case, fact: (empty ?peg_b)
            checkemp = parse_input("fact: (empty " + str(p2) + ")")
            if not self.kb.kb_ask(checkemp): pass
            else: self.kb.kb_retract(checkemp)

            newtuples = self.getGameState()

            for i, t in enumerate(newtuples):
                # Add empty peg statements
                if i == 0: which = "peg1"
                if i == 1: which = "peg2"
                if i == 2: which = "peg3"
                if t == ():
                    addemp = parse_input("fact: (empty " + which + ")")
                    self.kb.kb_assert(addemp)
                # Add new OTO statements
                elif len(t) == 2:
                    disk_a = "disk" + str(t[0])
                    disk_b = "disk" + str(t[1])
                    addOTO = parse_input("fact: (onTopOf " + disk_a + " " + disk_b + ")")
                    self.kb.kb_assert(addOTO)

                    # Modifying the top
                    newtop = parse_input("fact: (top " + disk_a + " " + which + ")")
                    self.kb.kb_assert(newtop)
                elif len(t) ==3:
                    disk_a = "disk" + str(t[0])
                    disk_b = "disk" + str(t[1])
                    disk_c = "disk" + str(t[2])
                    addOTO = parse_input("fact: (onTopOf " + disk_a + " " + disk_b + ")")
                    addOTO2 = parse_input("fact: (onTopOf " + disk_b + " " + disk_c + ")")
                    self.kb.kb_assert(addOTO)
                    self.kb.kb_assert(addOTO2)

                    # Modifying the top
                    newtop = parse_input("fact: (top " + disk_a + " " + which + ")")
                    self.kb.kb_assert(newtop)
                elif len(t) == 4:
                    disk_a = "disk" + str(t[0])
                    disk_b = "disk" + str(t[1])
                    disk_c = "disk" + str(t[2])
                    disk_d = "disk" + str(t[3])
                    addOTO = parse_input("fact: (onTopOf " + disk_a + " " + disk_b + ")")
                    addOTO2 = parse_input("fact: (onTopOf " + disk_b + " " + disk_c + ")")
                    addOTO3 = parse_input("fact: (onTopOf " + disk_c + " " + disk_d + ")")
                    self.kb.kb_assert(addOTO)
                    self.kb.kb_assert(addOTO2)
                    self.kb.kb_assert(addOTO3)

                    # Modifying the top
                    newtop = parse_input("fact: (top " + disk_a + " " + which + ")")
                    self.kb.kb_assert(newtop)
                elif len(t) == 5:
                    disk_a = "disk" + str(t[0])
                    disk_b = "disk" + str(t[1])
                    disk_c = "disk" + str(t[2])
                    disk_d = "disk" + str(t[3])
                    disk_d = "disk" + str(t[4])
                    addOTO = parse_input("fact: (onTopOf " + disk_a + " " + disk_b + ")")
                    addOTO2 = parse_input("fact: (onTopOf " + disk_b + " " + disk_c + ")")
                    addOTO3 = parse_input("fact: (onTopOf " + disk_c + " " + disk_d + ")")
                    addOTO4 = parse_input("fact: (onTopOf " + disk_d + " " + disk_e + ")")
                    self.kb.kb_assert(addOTO)
                    self.kb.kb_assert(addOTO2)
                    self.kb.kb_assert(addOTO3)
                    self.kb.kb_assert(addOTO4)

                    # Modifying the top
                    newtop = parse_input("fact: (top " + disk_a + " " + which + ")")
                    self.kb.kb_assert(newtop)

        return

        # fact: (movable disk1 peg1 peg2)
        # fact: (movable disk1 peg1 peg3)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        rep = [None] * 9
        tuplst = []

        tile_facts = self.kb.facts
        # print('the facts!', tile_facts)
        for f in tile_facts:
            # Handling "on" facts
            pred = f.statement.predicate
            t = f.statement.terms
            if pred == 'posn':
                xnum1 = int(str(t[1])[3])
                ynum1 = int(str(t[2])[3])
                i = (ynum1 - 1) * 3 + (xnum1 - 1)
                if str(t[0]) == 'empty':
                    rep[i] = -1
                else:
                    tilenum = int(str(t[0])[4])
                    rep[i] = tilenum

        print('what does it look like', rep)

        tuplst = [tuple(rep[0:3]), tuple(rep[3:6]), tuple(rep[6:9])]
        ans = tuple(tuplst)
        # print('this is my ans', ans)

        return ans
        # matrix format: [[? ? ?], [? ? ?], [? ? ?]]
        # jk the real matrix format: [??? ??? ???]
        # y * width + x

        # some sort of sorting thing here
        # for l in rep_lst:
        #     tuplst.append(tuple(l))
        # ans = tuple(tuplst)
        # print('DID I DO IT', ans)
        # return ans

        # elif (pred == 'movable'):
        #     for i, each in t:
        #         print('name??', each)

        # fact: (movable tile# xnum1 ynum1 xnum2 ynum2)
        # fact: (movable tile4 pos2 pos1 pos3 pos1)
        # fact: (movable tile8 pos3 pos2 pos3 pos1)

        # fact: (posn tile5 pos1 pos1)
        # fact: (posn tile4 pos2 pos1)
        # fact: (posn tile6 pos1 pos2)
        # fact: (posn tile1 pos2 pos2)
        # fact: (posn tile8 pos3 pos2)
        # fact: (posn tile7 pos1 pos1)
        # fact: (posn tile3 pos2 pos3)
        # fact: (posn tile2 pos3 pos3)

        # ans should be
        # ((5,4,-1),(6,1,8),(7,3,2)))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        if movable_statement.predicate != 'movable': print('Not an acceptable movable statement')
        else:
            t = movable_statement.terms
            tilenum = int(str(t[0])[4])  # Had to convert the term into a string, then index
            # fact: (movable tile# xnum1 ynum1 xnum2 ynum2)
            xnum1 = int(str(t[1])[3])
            ynum1 = int(str(t[2])[3])
            xnum2 = int(str(t[3])[3])
            ynum2 = int(str(t[4])[3])

            tile = str(t[0])
            x1 = str(t[1])
            y1 = str(t[2])
            x2 = str(t[3])
            y2 = str(t[4])

            # Moved to slot is no longer empty
            # oldmov = parse_input("fact: (" + str(movable_statement) + ")")
            # self.kb.kb_retract(oldmov)  # is this correct syntax
            oldposn = parse_input("fact: (posn " + tile + " " + x1 + " " + y1 + ")")
            self.kb.kb_retract(oldposn)

            # Assert the reverse movable statement
            # newmov = parse_input("fact: (movable " + tile + " " + x2 + " " + y2 +  " " + x1 + " " + y1  + ")")
            # print('new mov:', newmov)
            # self.kb.kb_assert(newmov)
            newposn = parse_input("fact: (posn " + tile + " " + x2 + " " + y2 + ")")
            # print('new position', newposn)
            self.kb.kb_assert(newposn)

            oldemp = parse_input("fact: (posn empty " + x2 + " " + y2 + ")")
            self.kb.kb_retract(oldemp)

            newemp = parse_input("fact: (posn empty " + x1 + " " + y1 + ")")
            self.kb.kb_assert(newemp)

            # i = (ynum1 - 1) * 3 + (xnum1 - 1)
            # rep[i] = tilenum

        # if empty slot
        # ind = (ynum2 - 1) * 3 + (xnum2 - 1)
        # rep[ind] = -1

        # need to add adjacency rules -- if u move it towards the center then now 3 tiles can now move into the empty slot
        # need to adjust for this
        # fact: (posn tile0 pos3 pos1)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
