# Chess Game

Welcome to the game of Chess!

### What It Uses

- Python (3.6.4)
- PyGame (1.9.3)
- PygButton (0.9.0)
- Stockfish (1.0.4) (Python module)
- Stockfish 9

### Instructions To Run

1. Make sure Python (3.6.4) is installed correctly with Pip.
2. Install the Python modules / packages needed using "pip install {module_name}" or "pip3 install {module_name}".
3. Download "main.py", "settings.py", and "sprites.py".
4. Download all the Chess images and save it into an "Images" folder.
5. Download Stockfish 9 from the Stockfish website. You can save it anywhere but be sure to change the "STOCKFISH_EXE_PATH" constant in "settings.py" to the path to the Stockfish executable.
6. Run "main.py" with Python.

Note: You can skip steps 3 & 4 if you download / clone the GitHub repository.

### Tree Design

Your file tree should look like this:

- Chess (root directory)
    - Images
        - Black Bishop.png
        - Black King.png
        - Black Knight.png
        - Black Pawn.png
        - Black Queen.png
        - Black Rook.png
        - White Bishop.png
        - White King.png
        - White Knight.png
        - White Pawn.png
        - White Queen.png
        - White Rook.png     
    - main.py
    - settings.py
    - sprites.py

### Instructions For Playing The Game

- Click on a piece to select it, then click on one of the highlighted squares to move it there
- Use the "escape" key to exit the game at any time

### Stockfish Engine

The singleplayer mode uses the Stockfish chess engine for its move generation. It will automatically make a move but it could take a little while. The choice of difficulty only affects the search depth of the algorithm.
