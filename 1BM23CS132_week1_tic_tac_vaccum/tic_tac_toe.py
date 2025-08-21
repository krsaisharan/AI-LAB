import random

def print_board(board):
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("---------")

def check_win(board, player):
    # rows
    for row in board:
        if all(s == player for s in row):
            return True
    # cols
    for c in range(3):
        if all(board[r][c] == player for r in range(3)):
            return True
    # diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(board[r][c] != " " for r in range(3) for c in range(3))

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    human = input("Choose X or O: ").upper()
    while human not in ["X","O"]:
        human = input("Invalid. Choose X or O: ").upper()
    comp = "O" if human == "X" else "X"

    turn = input("Do you want to go first? (y/n): ").lower() == "y"
    print_board(board)

    while True:
        if turn:  # Human move
            try:
                r, c = map(int, input("Enter row,col (0-2): ").split(","))
                if board[r][c] != " ":
                    print("Already taken!")
                    continue
                board[r][c] = human
            except:
                print("Invalid input")
                continue
        else:  # Computer move
            r, c = random.choice([(i,j) for i in range(3) for j in range(3) if board[i][j]==" "])
            board[r][c] = comp
            print(f"Computer places {comp} at ({r},{c})")

        print_board(board)

        if check_win(board,human):
            print("🎉 You win!")
            break
        elif check_win(board,comp):
            print("💻 Computer wins!")
            break
        elif is_full(board):
            print("🤝 Draw!")
            break

        turn = not turn

tic_tac_toe()



