import random

# Will work with Python 3.12
# May work on other Python versions too, no guarantees though

# draws the board
def draw_board(quantum_board: list[list[int]], classical_board: list[int]) -> None:
	# big o is the even positions, big x is the odd ones
	big = ["  ┌─┐   ","  ╲ ╱   ", "  │ │   ","   ╳    ", "  └─┘n  ","  ╱ ╲n  "]
	row   = "╠════════╬════════╬════════╣"
	column = "║"
	blank = "        "
	height = 3 * 3 + 2
	offset = 0
	print("╔════════╦════════╦════════╗")
	for i in range(height):
		if i == 3 or i == 7:
			print(row)
			offset += 1
		else:
			row_num = i - offset
			row_part = row_num % 3
			
			print_row = column
			for j in range(3):
				if(classical_board[j + offset * 3] > 0):
					big_mark = big[row_part * 2 + (classical_board[j + offset * 3]) % 2].replace("n", str(classical_board[j + offset * 3]))
					print_row += big_mark
				elif(len(quantum_board[j + offset * 3]) > 0):
					if len(quantum_board[j + offset * 3]) <= row_part * 3:
						print_row += blank
					else:
						for k in range(row_part * 3, (row_part + 1) * 3):
							if k >= len(quantum_board[j + offset * 3]):
								print_row += "   "
							else:
								mark = "x" if (quantum_board[j + offset * 3][k] // 10) % 2 == 1 else "o"
								mark += str(quantum_board[j + offset * 3][k] // 10) + " "
								print_row += mark
						# trim off the trailing space		
						print_row = print_row[:-1]
				else:
					print_row += blank
				print_row += column
			print(print_row)
	print("╚════════╩════════╩════════╝")

def get_position(move: int) -> int:
	return move % 10

def get_other_value(value: int, position: int) -> int:
	return (value // 10) * 10 + position

# returns true if there's a cycle (that is, a chain of superpositions that makes a loop)
# only need to check to see if there's a path from one of the last move positions to the other
# ignoring the trivial route, of course
def has_cycle(quantum_board: list[list[int]], last_moves: list[int]) -> bool:
	current_pos = get_position(last_moves[0])
	target_pos = get_position(last_moves[1])
	to_visit = list(map(get_position, quantum_board[current_pos]))
	# we ignore the trivial route, since a 1-cycle can't be made
	# since calling remove only removes the first instance, if it's a 2-cycle
	# there will still be a path
	to_visit.remove(target_pos)
	visited = [current_pos]
	while len(to_visit) > 0:
		if to_visit.count(target_pos) > 0:
			return True
		current_pos = get_position(to_visit.pop())
		visited.append(current_pos)
		for destination in quantum_board[current_pos]:
			dest_pos = get_position(destination)
			if visited.count(dest_pos) == 0 and to_visit.count(target_pos) == 0:
				to_visit.append(dest_pos)
	return False

# returns the state of the boards after a collapse has completely, with `position` being `value`.
# Note that `value` is the quantum_board variant (with the pointer to the other position)
def collapse(quantum_board: list[list[int]], classical_board: list[int], position: int, value: int) -> None:
	other_pos = get_position(value)
	quantum_board[position].remove(value)
	quantum_board[other_pos].remove(get_other_value(value, position))
	
	classical_board[position] = value // 10
	# list of quantum "cells" that need to be collapsed
	to_collapse = [position]
	while len(to_collapse) > 0:
		# will always exist
		position = to_collapse[0]
		if len(quantum_board[position]) == 0:
			to_collapse.remove(position)
		else:
			collapse_val = quantum_board[position].pop()
			other_pos = get_position(collapse_val)
			quantum_board[other_pos].remove(get_other_value(collapse_val, position))
			classical_board[other_pos] = collapse_val // 10
			to_collapse.append(other_pos)
			
	

# returns with a score to see who won. 0 if no three in a row, otherwise:
# 1 point for win with the lower highest spooky mark in their winning three in a row
# 0.5 points for other player if they also won, but with a higher highest spooky mark
def is_won(classical_board: list[int]) -> dict[str, float]:
	winner = float('nan') # placeholder value
	winner_spooky_mark = 9999
	loser_spooky_mark = 9999
	# check rows
	for i in range(0,9,3):
		if classical_board[i] == 0 or classical_board[i+1] == 0 or classical_board[i+2] == 0:
			continue
		if classical_board[i] % 2 == classical_board[i+1] % 2 == classical_board[i+2] % 2:
			highest_spooky_mark = max(classical_board[i], classical_board[i+1], classical_board[i+2])
			if highest_spooky_mark < winner_spooky_mark:
				loser_spooky_mark = winner_spooky_mark
				winner_spooky_mark = highest_spooky_mark
				if winner % 2 != classical_board[i] % 2:
					winner = classical_board[i] % 2
			else:
				loser_spooky_mark = highest_spooky_mark
	# check columns
	for i in range(3):
		if classical_board[i] == 0 or classical_board[i+3] == 0 or classical_board[i+6] == 0:
			continue
		if classical_board[i] % 2 == classical_board[i+3] % 2 == classical_board[i+6] % 2:
			highest_spooky_mark = max(classical_board[i], classical_board[i+3], classical_board[i+6])
			if highest_spooky_mark < winner_spooky_mark:
				loser_spooky_mark = winner_spooky_mark
				winner_spooky_mark = highest_spooky_mark
				if winner % 2 != classical_board[i] % 2:
					winner = classical_board[i] % 2
			else:
				loser_spooky_mark = highest_spooky_mark
	# check diagonals
	if classical_board[0] == 0 or classical_board[4] == 0 or classical_board[8] == 0:
		pass
	elif classical_board[0] % 2 == classical_board[4] % 2 == classical_board[8] % 2:
		highest_spooky_mark = max(classical_board[0], classical_board[4], classical_board[8])
		if highest_spooky_mark < winner_spooky_mark:
			loser_spooky_mark = winner_spooky_mark
			winner_spooky_mark = highest_spooky_mark
			if winner % 2 != classical_board[0] % 2:
				winner = classical_board[0] % 2
		else:
			loser_spooky_mark = highest_spooky_mark
	if classical_board[2] == 0 or classical_board[4] == 0 or classical_board[6] == 0:
		pass
	elif classical_board[2] % 2 == classical_board[4] % 2 == classical_board[6] % 2:
		highest_spooky_mark = max(classical_board[2], classical_board[4], classical_board[6])
		if highest_spooky_mark < winner_spooky_mark:
			loser_spooky_mark = winner_spooky_mark
			winner_spooky_mark = highest_spooky_mark
			if winner % 2 != classical_board[2] % 2:
				winner = classical_board[2] % 2
		else:
			loser_spooky_mark = highest_spooky_mark
	if winner == winner: # NaN is not equal to itself
		if winner == 1:
			x_points = 1
			if loser_spooky_mark < 9999:
				o_points = 0.5
			else:
				o_points = 0
		else:
			o_points = 1
			if loser_spooky_mark < 9999:
				x_points = 0.5
			else:
				x_points = 0
	else:
		o_points = 0
		x_points = 0	
	score = {"O": o_points, "X": x_points}
	return score

def move_board(valid_moves: list[bool]) -> None:
	column = "│"
	row = "─┼─┼─"
	offset = 0
	height = 3 + 2
	for i in range(height):
		print_row = ""
		if i == 1 or i == 3:
			print_row = row	
			offset += 1
		else:
			for j in range(3):
				if valid_moves[(i - offset)*3 + j]:
					print_row += str((i - offset)*3 + j) + column
				else:
					print_row += " " + column
			print_row = print_row[:-1] # remove the trailing column
		print(print_row)

def player_move(valid_moves: list[bool], player: str) -> list[int]:
	print("Valid Moves:")
	move_board(valid_moves)
	while True:
		try:
			position1 = int(input(player + " first location: "))
			if valid_moves[position1]:
				break
			print("Invalid location, try again")
		except ValueError:
			print("Not a number, try again")
	while True:
		try:
			position2 = int(input(player + " second location: "))
			if valid_moves[position2] and position2 != position1:
				break
			print("Invalid location, try again")
		except ValueError:
			print("Not a number, try again")
	return [position1, position2]

def player_collapse(moves: list[int], player: str) -> int:
	print(f"{player}, choose either {moves[0]} or {moves[1]} to be measured")
	print("The result of the measurement in that square will be whatever was played last round")	
	while True:
		try:
			position = int(input(player + " pick location: "))
			if position == moves[0] or position == moves[1]:
				return position
			print("Invalid location, try again")
		except ValueError:			
			print("Not a number, try again")
			

def ai_collapse(moves: list[int]) -> int:
	position = random.choice(moves)
	print(f"The AI has chosen to collapse {position}")
	return position
	
def ai_move(valid_moves: list[bool]) -> list[int]:
	moves = []
	for i in range(len(valid_moves)):
		if valid_moves[i]:
			moves.append(i)
	choices = random.sample(moves, 2)
	print(f"The AI has chosen to play {choices[0]} and {choices[1]}")
	return choices
			

def ai_game(ai_role: str) -> dict[str,float]:
	classical_board = [0,0,0,0,0,0,0,0,0]
	quantum_board = [[],[],[],[],[],[],[],[],[]]
	valid_moves = [True,True,True,True,True,True,True,True,True]
	score = {}
	moves = [0,0]
	position = 0
	for turn in range(1,11): # extra round for final cycle check
		player = "O" if turn % 2 == 0 else "X"
		if turn > 1 and has_cycle(quantum_board, moves):
			print("Cycle detected, resolve superpositions")
			if player == ai_role:
				position = ai_collapse(moves)
			else:		
				position = player_collapse(moves, player)
			other_pos = moves[1] if position == moves[0] else moves[0]
			collapse(quantum_board, classical_board, position, (turn - 1) * 10 + other_pos)
			for i in range(9):
					if classical_board[i] != 0:
						valid_moves[i] = False
			draw_board(quantum_board, classical_board)
		score = is_won(classical_board)
		if score["O"] > 0 or score["X"] > 0 or turn == 10:
			# someone has won or the board is full
			# not the cleanest way to end the game, especially in the latter case
			break		
		if player == ai_role:
			moves = ai_move(valid_moves)
		else:
			moves = player_move(valid_moves, player)
		quantum_board[moves[0]].append(turn * 10 + moves[1])
		quantum_board[moves[1]].append(turn * 10 + moves[0])	
		draw_board(quantum_board, classical_board)
	if score["O"] > score ["X"]:
		print("O Victory!")
	elif score["X"] > score ["O"]:
		print("X Victory!")
	else:
		print("Draw")
	return score

def game() -> dict[str,float]:
	classical_board = [0,0,0,0,0,0,0,0,0]
	quantum_board = [[],[],[],[],[],[],[],[],[]]
	valid_moves = [True,True,True,True,True,True,True,True,True]
	score = {}
	moves = [0,0]
	for turn in range(1,11): # extra round for final cycle check
		player = "O" if turn % 2 == 0 else "X"
		if turn > 1 and has_cycle(quantum_board, moves):
			print("Cycle detected, resolve superpositions")
			position = player_collapse(moves, player)
			other_pos = moves[1] if position == moves[0] else moves[0]
			collapse(quantum_board, classical_board, position, (turn - 1) * 10 + other_pos)
			for i in range(9):
					if classical_board[i] != 0:
						valid_moves[i] = False
			draw_board(quantum_board, classical_board)
		score = is_won(classical_board)
		if score["O"] > 0 or score["X"] > 0 or turn == 10:
			# someone has won or the board is full
			# not the cleanest way to end the game, especially in the latter case
			break
			
		moves = player_move(valid_moves, player)
		quantum_board[moves[0]].append(turn * 10 + moves[1])
		quantum_board[moves[1]].append(turn * 10 + moves[0])	
		draw_board(quantum_board, classical_board)
	if score["O"] > score ["X"]:
		print("O Victory!")
	elif score["X"] > score ["O"]:
		print("X Victory!")
	else:
		print("Draw")
	return score

def one_player(score: dict[str, float]):
	quit = False
	while not quit:
		while True:
			player1_role = input("Player, would you like to play as X or O? ")
			if player1_role == "x" or player1_role == "X":
				player1_role = "X"
				break
			elif player1_role == "o" or player1_role == "O":
				player1_role = "O"
				break
			else:
				print("Invalid answer. Please type either 'X' or 'O'")
		ai_role = "X" if player1_role == "O" else "O"
		match_score = ai_game(ai_role)
		score["P1"] += match_score[player1_role]
		score["P2"] += match_score[ai_role]
		print(f"Total Score:\nHuman: {score["P1"]}\nAI: {score["P2"]}")
		quitting = input("Would you like to exit? (Y/n) ")
		if quitting.startswith(("Y","y")):
			quit = True

def two_player(score: dict[str, float]):
	quit = False
	while not quit:
		while True:
			player1_role = input("Player 1, would you like to play as X or O? ")
			if player1_role == "x" or player1_role == "X":
				player1_role = "X"
				break
			elif player1_role == "o" or player1_role == "O":
				player1_role = "O"
				break
			else:
				print("Invalid answer. Please type either 'X' or 'O'")
		player2_role = "X" if player1_role == "O" else "O"
		match_score = game()
		score["P1"] += match_score[player1_role]
		score["P2"] += match_score[player2_role]
		print(f"Total Score:\nPlayer 1: {score["P1"]}\nPlayer 2: {score["P2"]}")
		quitting = input("Would you like to exit? (Y/n) ")
		if quitting.startswith(("Y","y")):
			quit = True

# start with two player, then add random AI
if __name__ == "__main__":
	quit = False
	score = {"P1": 0.0, "P2": 0.0}
	print("Welcome to Quantum Tic-Tac-Toe")
	while True:
		mode = input("Would you like to play 1 player or 2 players? ")
		if mode == "1":
			one_player(score)
		elif mode == "2":
			two_player(score)
		else:
			print("Invaild input, please type '1' or '2'")
		break
