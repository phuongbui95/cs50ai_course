from logic import *

AKnight = Symbol("A is a Knight") # A
AKnave = Symbol("A is a Knave") # NOT(A)

BKnight = Symbol("B is a Knight") # B
BKnave = Symbol("B is a Knave") # NOT(B)

CKnight = Symbol("C is a Knight") # C
CKnave = Symbol("C is a Knave") # NOT(C)

''' Knowledge Engineering '''
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Game's rule:
    Or(AKnight, AKnave), 
    Not(And(AKnight, AKnave)),

    # Implications from what A said
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # Game's rule:
    Or(AKnight, AKnave), 
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), 
    Not(And(BKnight, BKnave)),

    # Implications from what A said
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave))),

    # Implications from what B said: nothing
    Or(And(AKnave, BKnave),And(AKnave, BKnight),And(AKnight, BKnight),And(AKnight, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # Game's rule:
    Or(AKnight, AKnave), 
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), 
    Not(And(BKnight, BKnave)),

    # Implications from what A said
    Implication(AKnight, Or(And(AKnave, BKnave),And(AKnight, BKnight))),
    Implication(AKnave, Not(Or(And(AKnave, BKnave),And(AKnight, BKnight)))),

    # Implications from what B said
    Implication(BKnight, Or(And(AKnave, BKnight),And(AKnight, BKnave))),
    Implication(BKnave, Not(Or(And(AKnave, BKnight),And(AKnight, BKnave)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # Game's rule:
    Or(AKnight, AKnave), 
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), 
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave), 
    Not(And(CKnight, CKnave)),

    # Implications from what A said
    Implication(AKnight, Or(AKnight,AKnave)), 
    Implication(AKnave, Not(Or(AKnight,AKnave))), 

    # Implications from what B said about what A said
    Implication(BKnight, Implication(Or(AKnight,AKnave),AKnave)),
    Implication(BKnave, Not(Implication(Or(AKnight,AKnave),AKnave))),

    # Implications from what B said about C
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # Implications from what C said about A
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
