from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave." -> And(AKnight, AKnave)
knowledge0 = And(
    Not(And(AKnight, AKnave)),  # A cannot be knight and knave at the same time
    Or(AKnight, AKnave),        # A is a knight or a knave
    Implication(AKnight, And(AKnight, AKnave)),  # If A is knight, then A told the true
    Implication(AKnave, Not(And(AKnight, AKnave)))  # If A is a knave, then A told lie
)

# Puzzle 1
# A says "We are both knaves." -> And(AKnave, BKnave)
# B says nothing.
knowledge1 = And(
    Not(And(AKnight, AKnave)),  # A cannot be knight and knave at the same time
    Or(AKnight, AKnave),        # A is a knight or a knave
    Not(And(BKnight, BKnave)),  # B cannot be knight and knave at the same time
    Or(BKnight, BKnave),        # B is a knight or a knave

    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind." -> Or(And(AKnave, BKnave), And(AKnight, BKnight))
# B says "We are of different kinds." -> Or(And(AKnave, BKnight), And(AKnight, BKnave))
knowledge2 = And(
    Not(And(AKnight, AKnave)),  # A cannot be knight and knave at the same time
    Or(AKnight, AKnave),        # A is a knight or a knave
    Not(And(BKnight, BKnave)),  # B cannot be knight and knave at the same time
    Or(BKnight, BKnave),        # B is a knight or a knave

    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, Not((And(AKnave, BKnave)))),

    Implication(BKnight, And(AKnave, BKnight)),
    Implication(BKnave, Not(And(AKnight, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which. -> Or(AKnight, AKnave)
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight." 
knowledge3 = And(
    Not(And(AKnight, AKnave)),  # A cannot be knight and knave at the same time
    Or(AKnight, AKnave),        # A is a knight or a knave
    Not(And(BKnight, BKnave)),  # B cannot be knight and knave at the same time
    Or(BKnight, BKnave),        # B is a knight or a knave
    Not(And(CKnight, CKnave)),  # C cannot be knight and knave at the same time
    Or(CKnight, CKnave),        # C is a knight or a knave

    # A says either "I am a knight." or "I am a knave.", but you don't know which. -> Or(AKnight, AKnave)
    Or(
        # "I am a knight."
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),       
        # "I am a knave."
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),
    
    # B says "A said 'I am a knave'."
    Implication(BKnight, And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    )),
    Implication(BKnave, Not(And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    ))),
    
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
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
