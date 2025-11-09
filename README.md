# Tetris AI Bot

This project implements an autonomous Tetris-playing agent that evaluates game states, simulates moves, and selects actions to maximise long-term performance. The bot incorporates core Tetris mechanics, heuristic scoring, and efficient board evaluation to make near-real-time decisions during gameplay.

## Overview

The Tetris AI Bot is designed to analyse every possible placement and rotation of a tetromino, compute the resulting board state, and select the highest-scoring move based on a weighted heuristic. The objective is to minimise board height, avoid creating holes, and maximise line clears while maintaining stable board transitions.

This project includes:

* A fully simulated Tetris board
* A greedy AI player with tunable heuristics
* Support for standard tetrominoes and rotations
* Move evaluation based on board state scoring
* Optional expanded strategies such as bombs, discard chances, and advanced stacking techniques

## Features

### Core Functionality

* **Grid-based game engine**: Handles piece movement, rotation, collision detection, line clears, and game over conditions.

* **Search-based move evaluation**: The AI enumerates all legal placements for the current piece and scores resulting boards.

* **Heuristic scoring**: The bot evaluates:

  * Aggregate column height
  * Number of holes
  * Bumpiness (vertical transitions)
  * Row transitions and column transitions
  * Completed lines
  * Well depths

* **Piece simulation**: Efficient drop simulation without external libraries.

## AI Strategy

The current bot employs a **greedy single-step heuristic**, selecting the move that yields the highest immediate score. The heuristics are weighted based on known effective Tetris AI strategies.

Future improvements include:

* Multi-step lookahead
* Advanced Tetris stacking (e.g., six-three stack)
* Adaptive weights via reinforcement learning
* Evaluation caching for performance optimisation

## Project Structure

```
/project-root
│
├── board.py              # Core game logic and board simulation
├── player.py             # Heuristic evaluation and move selection
├── adversary.py   
├── arguments.py 
├── client.py
├── cmdline.py
├── constants.py 
├── exceptions.py
├── notes.docx
├── player_backup.py
├── player_try.py 
├── scores.xlsx 
├── Segment7-4Gml.otf
├── server.py
├── visual-pygame.py
├── visual.py
├── weights.py       
└── README.md              # Documentation
```

## How It Works

1. The AI iterates through all possible rotations and horizontal positions for the falling tetromino.
2. For each option, the bot simulates a drop to produce a hypothetical board.
3. The board is scored using the heuristic function.
4. The AI selects the move with the best score.
5. Gameplay continues until no further moves are possible.

## Running the Project

Ensure you have Python and the Pygame library installed.

```sh
python visual-pygame.py
```

This will launch the AI-controlled game in the pygame interface.

## Tuning Heuristics

Weights can be modified inside `player.py`:

```python
score = 1000 - 20.110954195982956 * holes - 0.46484750255165963 * len(board.cells) - 1.7338268167957067 * greatest_height - 0.9821726250852962 * bumpiness + 3.580114847254702 * lines_cleared - 100.96014008539409 * well_penalty + 0.2298762066943576 * tetris_potential
# ... add or adjust fields as needed
```

Adjust these values to experiment with different play styles or optimise performance for specific scenarios.

## Future Work

* Implement multi-step search with pruning
* Add support for hold piece and next-piece previews
* Incorporate advanced stacking techniques such as the six-three stack
* Train weights using machine learning
