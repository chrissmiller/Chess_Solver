# Chess AI
##### Chris Miller '20
---

### Minimax Search
In the Minimax object, I store the color of the side (default black), the max depth to travel to, the number of nodes visited, and a visited dictionary which is used to hash visited states and avoid visiting them twice. 

My `max_val` and `min_val` functions call each other up to the depth limit, 

My `get_val` function determines what the state of the board is, and provides extremely high and low values for victory/loss, and a zero value for a draw (this makes sense as a player with a strongly negative board position will seek a draw, while one with a positive board position will not). If the game is not over on the given board, it passes the board to the `material_heuristic` function. This function calls `get_material_value` to calculate material values for the AI's side and the opponent's side, subtracting the opponent's material from the AI's material value. It also provides a small bonus for putting the opponent in check, and seeks to avoid being put in check. 

My `get_material_value` function follows typical assignments of value (1 for pawns, 3 for knights/bishops, 5 for rooks, 9 for queens) but gives a bonus to bishops, rooks, and pawns in the endgame (defined as the AI's color having less than six pieces).

### Alpha-Beta Search
My `choose_move` function loops through depths from 1 to the defined max depth, initializing alpha and beta to negative infinity and infinity respectively, and calling the `max_val` function which searches via alpha beta search. After searching, the algorithm prints the best move at each depth, as well as the number of nodes visited and the move's predicted value.

My `max_val` and `min_val` functions are similar to the Minimax functions, except that they also update alpha and beta as they search and reject extraneous searches (based on comparisons of node value and alpha and beta). This allows the algorithm to dramatically cut the number of nodes visited.

My other structure is the same as my Minimax structure.



#### Testing
Here we see an example of how the algorithm improves the move it provides over each depth. The first move is a simple capture, which provides value at depth 1 but sees black's knight captured at depth 2, causing the program to reject it with further consideration. Three moves in, black sees that it can move its knight g4e5 and threaten white's undefended pawn - clearly the best move of the three.

    r n b q k b . r  
    p p p p p p p p  
    . . . . . . . .  
    . . . . . . . .  
    . . P . . . n .  
    . . N . . . . N  
    P P . P P P P P  
    R . B Q K B . R 
    ----------------  
    a b c d e f g h  

    Black to move

    At depth 1, Minimax recommends move g4h2
    At depth 2, Minimax recommends move h8g8
    At depth 3, Minimax recommends move g4e5
    r n b q k b . r
    p p p p p p p p
    . . . . . . . .
    . . . . n . . .
    . . P . . . . .
    . . N . . . . N
    P P . P P P P P
    R . B Q K B . R
    ----------------
    a b c d e f g h
    
---
    
Here, we see the effect of the algorithm pushing a bad outcome out past the visible horizon. 

In this example, black's queen at h4 is vulnerable to white's rook at h1. 

	r . b . k b . r
	p p p p . p p .
	. . . . p . . .
	. . n . . . . .
	. . Q . B N . q
	. . . P . . . .
	P P . . P P . .
	R N B . K . . R
	----------------
	a b c d e f g h
	
	Black to move

Minimax recommends c5d3, taking a white pawn. Although the move puts white's king in check, preventing the h1h4 queen capture, it does so by sacrificing black's knight for a pawn.

	At depth 3, Minimax recommends move c5d3 with val 4
	r . b . k b . r
	p p p p . p p .
	. . . . p . . .
	. . . . . . . .
	. . Q . B N . q
	. . . n . . . .
	P P . . P P . .
	R N B . K . . R
	----------------
	a b c d e f g h
	
After the human player captures the knight and exits check via c4d3, minimax moves black's bishop f8b4 to reclaim check. 
	
	At depth 3, Minimax recommends move f8b4 with val 4
	r . b . k . . r
	p p p p . p p .
	. . . . p . . .
	. . . . . . . .
	. b . . B N . q
	. . . Q . . . .
	P P . . P P . .
	R N B . K . . R
	----------------
	a b c d e f g h
	
This time, there is no clear vulnerability, and white plays c1d2 to protect the king.

	At depth 3, Minimax recommends move b4d2 with val 2
	r . b . k . . r
	p p p p . p p .
	. . . . p . . .
	. . . . . . . .
	. . . . B N . q
	. . . Q . . . .
	P P . b P P . .
	R N . . K . . R
	----------------
	a b c d e f g h
	
But in response, black trades bishops to put white back into check and delay h1h4 further.

	At depth 3, Minimax recommends move h4h1 with val -2
	r . b . k . . r
	p p p p . p p .
	. . . . p . . .
	. . . . . . . .
	. . . . B N . .
	. . . Q . . . .
	P P . N P P . .
	R . . . K . . q
	----------------
	a b c d e f g h

Finally, the loss of the queen or rook can no longer be pushed past the horizon, and black must act proactively with h4h1, sacrificing the queen for a rook before black's final move in the scenario avenges the queen by playing h8h1.

Overall, by sacrificing a knight for a pawn, a bishop for a bishop, a queen for a rook, and finally taking a bishop with a rook, black sees an overall material value loss of 3. If black had simply acted to sacrifice the queen for a rook and a bishop from the beginning, it would have seen an overall loss of just one point of material value. 

By increasing Minimax's acceptable depth to 4, the algorithm expands its horizon and more intelligently plays h4h1 at the expense of drastically slower performance:

	At depth 1, Minimax recommends move h4h1 with val 6
	At depth 2, Minimax recommends move c5d3 with val -3
	At depth 3, Minimax recommends move c5d3 with val 4
	At depth 4, Minimax recommends move h4h1 with val -2
	r . b . k b . r
	p p p p . p p .
	. . . . p . . .
	. . n . . . . .
	. . Q . B N . .
	. . . P . . . .
	P P . . P P . .
	R N B . K . . q
	----------------
	a b c d e f g h
	
---

I also tested the endgame performance in test_endgame.py. 

	. K . . . . . .
	. . . . . . . .
	q k . . . . . .
	. . . . . . . .
	. . . . . . . .
	. . . . . . . .
	. . . . . . . .
	. . . . . . . .
	----------------
	a b c d e f g h
	
	Black to move
	
	At depth 3, Minimax recommends move a6b7 with val 1000

As expected, black takes the mate-in-one, validating its endgame performance.

In addition, I played numerous games of chess against the AI and played the AI against the random AI - both minimax and Alpha-Beta won handily.



#### Performance Comparison

Basic implementations of Alpha-Beta (even without move ordering or hashing) drastically outperform Minimax. In the example of the Queen-Rook standoff above, displaying the number of nodes visited shows 2,252,057 nodes visited for Minimax with iterative deepening played to depth 4, versus 117,961 visited for Alpha-Beta with iterative deepening and hashing (the two algorithms produced identical moves at every level of deepening). 

Without hashing, the Alpha-Beta algorithm visits 218,269 nodes, and Minimax visits 2,920,414. Even implementing Alpha-Beta to a depth of 5 searches a mere 1,388,754 nodes in comparison and produced the higher quality move of h4f2 (in which black sacrifices its queen for a rook.

These comparisons show that clearly Alpha-Beta allows for dramatically improved performance by reducing the number of nodes searched and expanding the computationally-reachable depths.

#### Extras

I also implemented move ordering in AlphaBetaMoveOrder.py, which uses a priority queue and a tuple which stores the move's expected value (via material heuristic), a counter (to prevent the uncomparable chess.Move objects from being compared), and the move. However, this ended up being computationally expensive, and actually increased runtime - thus, I decided to stick with board.legal_moves for my main Alpha-Beta program.