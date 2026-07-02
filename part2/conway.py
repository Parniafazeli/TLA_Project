"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""
import numpy as np
from scipy import signal, ndimage


def parse_pattern(filepath):
    """
    [Part 1d - RLE/Plaintext Parser]
    Parse Run Length Encoded (RLE) or Plaintext (.cells) pattern files.
    
    Args:
        filepath (str): Path to the pattern file.
        
    Returns:
        tuple: (width, height, list of (r, c) offsets of live cells)
    """
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Detect format based on extension or content
    if filepath.endswith('.cells'):
        return _parse_plaintext(content)
    elif filepath.endswith('.rle'):
        return _parse_rle(content)
    else:
        # Auto-detect: if header contains RLE markers
        if 'x =' in content and 'y =' in content and 'rule =' in content:
            return _parse_rle(content)
        else:
            return _parse_plaintext(content)


def _parse_plaintext(content):
    """
    Parse Plaintext (.cells) format.
    Lines starting with '!' are comments.
    Other lines contain '.' (dead) and 'O' (live) characters.
    """
    lines = content.splitlines()
    live_cells = []
    max_col = 0
    row = 0
    started = False
    for line in lines:
        stripped = line.strip()
        if not started:
            if not stripped or stripped.startswith('!'):
                continue          # header/comments before the pattern body
            started = True
        else:
            if stripped.startswith('!'):
                continue          # (rare) trailing comment, not a row
        start = 0
        while start < len(line) and line[start] == ' ':
            start += 1
        for col, ch in enumerate(line[start:], start=start):
            if ch == 'O':
                live_cells.append((row, col))
            if col > max_col:
                max_col = col
        row += 1                  # blank rows now correctly count as a row
    height = row
    width = max_col + 1
    return width, height, live_cells

def _parse_rle(content):
    """
    Parse Run Length Encoded (.rle) format.
    Header: x = width, y = height, rule = B3/S23
    Data: numbers followed by 'b' (dead), 'o' (live), '$' (end of line), '!' (end of pattern)
    """
    lines = content.splitlines()
    header = {}
    data_lines = []
    in_data = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue  # Ignore comments
        if not in_data:
            # Parse header
            if 'x =' in line and 'y =' in line:
                parts = line.split(',')
                for part in parts:
                    part = part.strip()
                    if part.startswith('x ='):
                        header['x'] = int(part.split('=')[1].strip())
                    elif part.startswith('y ='):
                        header['y'] = int(part.split('=')[1].strip())
                    elif part.startswith('rule ='):
                        header['rule'] = part.split('=')[1].strip()
                # If header line also contains data (some RLE files have it on same line)
                if '!' in line or any(c in line for c in 'bo$'):
                    data_lines.append(line)
                    in_data = True
            else:
                # If no header, assume data has started
                data_lines.append(line)
                in_data = True
        else:
            data_lines.append(line)
    
    # Combine data (remove whitespace and newlines)
    data = ''.join(data_lines).replace(' ', '').replace('\n', '').replace('\r', '')
    
    # Parse RLE data
    width = header.get('x', 0)
    height = header.get('y', 0)
    live_cells = []
    r, c = 0, 0
    i = 0
    run_length = ''
    
    while i < len(data):
        ch = data[i]
        if ch.isdigit():
            run_length += ch
            i += 1
            continue
        else:
            count = int(run_length) if run_length else 1
            run_length = ''
            if ch == 'b':
                c += count
            elif ch == 'o':
                for _ in range(count):
                    live_cells.append((r, c))
                    c += 1
            elif ch == '$':
                r += count
                c = 0
            elif ch == '!':
                break
            i += 1
    
    # If width/height not in header, calculate from data
    if width == 0 or height == 0:
        max_r = max([cell[0] for cell in live_cells]) if live_cells else 0
        max_c = max([cell[1] for cell in live_cells]) if live_cells else 0
        width = max_c + 1
        height = max_r + 1
    
    return width, height, live_cells


class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  # 8 connected kernel
        self.neighborhood[1, 1] = 0  # do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N  # use for slow implementation of evolve
        self.cols = N  # use for slow implementation of evolve

    def getStates(self):
        """
        Returns the current states of the cells
        """
        return self.grid

    def getGrid(self):
        """
        Same as getStates()
        """
        return self.getStates()

    def update_grid_fast(self, grid):
        if self.finite:
            boundary = 'fill'  
        else:
            boundary = 'wrap'   

        # Count live neighbors for all cells using 2D convolution
        neighbor_count = signal.convolve2d(
            grid,
            self.neighborhood,
            mode='same',
            boundary=boundary,
            fillvalue=0
        )

        alive = (grid == 1)  
        dead = (grid == 0)   

        # Survival
        survive = alive & ((neighbor_count == 2) | (neighbor_count == 3))

        # Reproduction
        born = dead & (neighbor_count == 3)

        #Build next generation
        new_grid = (survive | born).astype(np.uint)
        
        return new_grid
        

    def evolve(self):
        """
        [Part 1a - Core Rules]
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        """
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            rows, cols = self.rows, self.cols
            new_grid = np.zeros((rows, cols), dtype=np.uint8)

            for r in range(rows):
                for c in range(cols):
                    # Count live neighbors (8 directions)
                    live_neighbors = 0
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            nr = r + dr
                            nc = c + dc

                            if self.finite:
                                # Finite boundary: outside grid = dead
                                if 0 <= nr < rows and 0 <= nc < cols:
                                    live_neighbors += self.grid[nr, nc]
                            else:
                                # Toroidal (wrapping) boundary
                                nr %= rows
                                nc %= cols
                                live_neighbors += self.grid[nr, nc]

                    # Apply four GoL rules
                    if self.grid[r, c] == 1:  # Live cell
                        if live_neighbors < 2 or live_neighbors > 3:
                            new_grid[r, c] = 0  # Dies
                        else:
                            new_grid[r, c] = 1  # Survives
                    else:  # Dead cell
                        if live_neighbors == 3:
                            new_grid[r, c] = 1  # Birth
                        else:
                            new_grid[r, c] = 0

            self.grid = new_grid

    def insertBlinker(self, index=(0, 0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        '''
        [Part 1b - Glider Simulation]
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        '''
        [Part 1c - Glider Gun Fix]
        FIXED: Corrected left block coordinates so the Gosper Glider Gun
        properly fires an infinite stream of gliders.
        '''
        self.grid[index[0] + 1, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 2, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 3, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 15] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 4, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 37] = self.aliveValue

        # FIXED: corrected left block coordinates (shifted back by 1 column)
        self.grid[index[0] + 5, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 3] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 23] = self.aliveValue

        self.grid[index[0] + 6, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 3] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 19] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 7, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 8, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 17] = self.aliveValue

        self.grid[index[0] + 9, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 15] = self.aliveValue

    def insertFromFile(self, filename, index=((0, 0))):
        '''
        [Part 1d - RLE/Plaintext Parser]
        Insert cells from pattern file using parse_pattern
        '''
        width, height, live_cells = parse_pattern(filename)
        print("width =", width)
        print("height =", height)
        print("live cells =", len(live_cells))
        
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue