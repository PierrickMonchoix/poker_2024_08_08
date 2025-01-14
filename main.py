from typing import List
import copy

print("hey\n")

# return gainA of A (gainA of B is the opposite)
def gainA(pHandA : int, pHandB : int, pBetA : int, pDoBCall : bool, pAnte : int) :
    lRet : int

    if(pDoBCall) :
        if(pHandA < pHandB) :
            lRet = -pAnte - pBetA
        elif(pHandA == pHandB) :
            lRet = 0
        else : # pHandA > pHandB
            lRet = pAnte + pBetA
    else : # B fold
        lRet = pAnte

    return lRet

assert (gainA(pHandA=2, pHandB=1, pBetA=7, pDoBCall=True, pAnte=3) == 10)
assert (gainA(pHandA=2, pHandB=1, pBetA=7, pDoBCall=False, pAnte=3) == 3)
assert (gainA(pHandA=1, pHandB=2, pBetA=7, pDoBCall=False, pAnte=3) == 3)
assert (gainA(pHandA=1, pHandB=2, pBetA=7, pDoBCall=True, pAnte=3) == -10)

# Strategy A : hand -> bet
# It is represented by a list where index is hand and list[index] is the associated bet

def decisionA(pStrategyA : List[int], pHandA : int) :
    lRet : int
    lRet = pStrategyA[pHandA]
    return lRet

assert(decisionA([2,3,5,7], pHandA=0) == 2)
assert(decisionA([2,3,5,7], pHandA=1) == 3)
assert(decisionA([2,3,5,7], pHandA=2) == 5)
assert(decisionA([2,3,5,7], pHandA=3) == 7)

# Strategy B : betA, handB -> call/fold
# It is represented by a matrix where i is bet A, j is hand B and matrix[i][j] is 0 for fold and 1 for call

def decisionB(pStrategyB : List[List[int]], pBetA : int, pHandB : int) :
    lRet : int
    lRet = pStrategyB[pBetA][pHandB]
    return lRet

assert(decisionB(pStrategyB=[[2,3,5],[7,11,13]], pBetA=0, pHandB=0) == 2)
assert(decisionB(pStrategyB=[[2,3,5],[7,11,13]], pBetA=0, pHandB=1) == 3)
assert(decisionB(pStrategyB=[[2,3,5],[7,11,13]], pBetA=0, pHandB=2) == 5)
assert(decisionB(pStrategyB=[[2,3,5],[7,11,13]], pBetA=1, pHandB=0) == 7)
assert(decisionB(pStrategyB=[[2,3,5],[7,11,13]], pBetA=1, pHandB=1) == 11)
assert(decisionB(pStrategyB=[[2,3,5],[7,11,13]], pBetA=1, pHandB=2) == 13)

# Equity A calculate from strat A and B

def equityA(pStrategyA : List[int], pStrategyB : List[List[int]], pAnte : int) :
    lRet = float
    lSumGainA : int = 0
    lMaxHand : int = len(pStrategyA) - 1
    for lHandA in range(0, lMaxHand+1):
        for lHandB in range(0, lMaxHand+1):
            lBetA : int = decisionA(pStrategyA=pStrategyA, pHandA=lHandA)
            lDoBCall : bool = decisionB(pStrategyB=pStrategyB,pBetA=lBetA,pHandB=lHandB)
            lGainA : int = gainA(pHandA=lHandA, pHandB=lHandB, pAnte=pAnte, pBetA=lBetA, pDoBCall=lDoBCall)
            lSumGainA += lGainA
    lNumberOfPossibilities : int = (lMaxHand+1)*(lMaxHand+1)
    lRet = lSumGainA/lNumberOfPossibilities
    return lRet

assert(equityA(pStrategyA=[0], pStrategyB=[[0]],pAnte=3) == 3)
assert(equityA(pStrategyA=[1], pStrategyB=[[0],[0]],pAnte=3) == 3)
assert(equityA(pStrategyA=[1], pStrategyB=[[0],[1]],pAnte=3) == 0)
assert(equityA(pStrategyA=[1,3,0], pStrategyB=[[0,1,1],[1,0,1],[1,1,1],[0,0,1]], pAnte=5) == 11.0/9.0)

# optimal stategy B from strategy A

def optimalStrategyB(pStrategyA : List[int], pAnte : int, pMaxHand : int) :
    lRet : List[List[int]] = []
    # sort and remove duplicates
    lListBetA : List[int] = sorted(set(pStrategyA))
    for lBetA in range(0, lListBetA[-1] + 1):
        if(lBetA in lListBetA) :
            lRet.append([0]*(pMaxHand+1))
        else :
            lRet.append(None)
    lEquityA = equityA(pStrategyA=pStrategyA, pStrategyB=lRet,pAnte=5)

    lDoBFoldSomeThing : bool = True
    lTestedStategyB : List[List[int]] = copy.deepcopy(lRet)
    for lK in range(0,pow(2,len(lListBetA)*(pMaxHand+1))-1) :
        lMustBreak : bool = False
        for lBetA in lListBetA :
            if(lMustBreak) :
                break
            for lHandB in range(0, pMaxHand+1) :
                if(lTestedStategyB[lBetA][lHandB] == 1) :
                    lTestedStategyB[lBetA][lHandB] = 0
                else :
                    lTestedStategyB[lBetA][lHandB] = 1
                    lMustBreak = True
                    break
        # print("lTestedStategyB : " + str(lTestedStategyB))
        lTestedEquityA = equityA(pStrategyA=pStrategyA, pStrategyB=lTestedStategyB, pAnte=pAnte)
        # print(str(lTestedEquityA) + " vs " + str(lEquityA))
        # A must lose to maximize B equity
        if(lTestedEquityA < lEquityA) :
            # print("win : " + str(lTestedStategyB))
            lEquityA = lTestedEquityA
            lRet = copy.deepcopy(lTestedStategyB)
    return lRet
        

# not claculously checked
assert(optimalStrategyB(pStrategyA=[1,1], pAnte=1, pMaxHand=1) == [None, [0, 1]])
assert(optimalStrategyB(pStrategyA=[1,1], pAnte=2, pMaxHand=1) == [None, [1, 1]])

# optimal stategy A and then B for that given A

def optimalStrategies(pMaxBet : int, pMaxHand : int, pAnte : int) :
    lStrategyA : List[int] = [0]*(pMaxHand+1)
    lSavedStrategyB : List[List[int]] = optimalStrategyB(pStrategyA=lStrategyA, pAnte=pAnte, pMaxHand=pMaxHand)
    lEquityA = equityA(pStrategyA=lStrategyA, pStrategyB=lSavedStrategyB,pAnte=pAnte)
    print(lStrategyA)
    lTestedStrategyA = copy.deepcopy(lStrategyA)
    for lK in range(0,pow(pMaxBet+1, pMaxHand+1)-1) :
        for lHandA in range(0,pMaxHand+1) :
            if(lTestedStrategyA[lHandA] == pMaxBet) :
                lTestedStrategyA[lHandA] = 0
            else :
                lTestedStrategyA[lHandA] += 1
                break
        
        lStrategyB = copy.deepcopy(optimalStrategyB(pStrategyA=lTestedStrategyA, pMaxHand=pMaxHand, pAnte=pAnte))
        lTestedEquityA = equityA(pStrategyA=lTestedStrategyA, pStrategyB=lStrategyB, pAnte=pAnte)
        print(lTestedStrategyA)
        # print(lStrategyB)
        # print(lTestedEquityA)
        if(lTestedEquityA > lEquityA) :
            lStrategyA = copy.deepcopy(lTestedStrategyA)
            lEquityA = lTestedEquityA
            lSavedStrategyB = copy.deepcopy(lStrategyB)
            print("lStrategyA : " + str(lStrategyA))
            print("lStrategyB : " + str(lSavedStrategyB))
            print("lEquityA : " + str(lEquityA))
    
    print("=== optimal strategies ===")
    print("lStrategyA : " + str(lStrategyA))
    print("lStrategyB : " + str(lSavedStrategyB))
    print("lEquityA : " + str(lEquityA))



            
            


optimalStrategies(pMaxBet=3, pMaxHand=4, pAnte=5)


    
    

