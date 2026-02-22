import random

def print_board(board):
    # Print board with cell numbers for empty cells
    cell_num = 0
    for row in board:
        display_row = []
        for cell in row:
            if cell == " ":
                display_row.append(str(cell_num))
            else:
                display_row.append(cell)
            cell_num += 1
        print(" | ".join(display_row))
        print("-" * 9)

def check_winner(board, player):
    # Check rows, columns and diagonals
    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def ai_move(board):
    # Medium AI: Block player win, win if possible, else random
    # 1. Win if possible
    for i, j in get_empty_cells(board):
        board[i][j] = "O"
        if check_winner(board, "O"):
            return
        board[i][j] = " "
    # 2. Block player win
    for i, j in get_empty_cells(board):
        board[i][j] = "X"
        if check_winner(board, "X"):
            board[i][j] = "O"
            return
        board[i][j] = " "
    # 3. Random move
    i, j = random.choice(get_empty_cells(board))
    board[i][j] = "O"

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe! You are X, AI is O.")
    # Randomly decide who starts
    player_turn = random.choice([True, False])
    if player_turn:
        print("You start first.")
    else:
        print("AI starts first.")

    while True:
        print_board(board)
        if player_turn:
            try:
                move = int(input("Enter your move (0-8): "))
                if move < 0 or move > 8:
                    print("Invalid cell number. Enter a number from 0 to 8.")
                    continue
                row, col = divmod(move, 3)
                if board[row][col] != " ":
                    print("Cell already taken. Try again.")
                    continue
                board[row][col] = "X"
            except Exception:
                print("Invalid input. Enter a number from 0 to 8.")
                continue
            if check_winner(board, "X"):
                print_board(board)
                print("You win!")
                break
        else:
            ai_move(board)
            if check_winner(board, "O"):
                print_board(board)
                print("AI wins!")
                break
        if not get_empty_cells(board):
            print_board(board)
            print("It's a draw!")
            break
        player_turn = not player_turn

if __name__ == "__main__":
    main()