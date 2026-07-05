"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""
import numpy as np
from scipy import signal


def parse_pattern(filepath):

    with open(filepath, 'r') as file:
        content = file.read()
    
    # Detect file type and use the correct parser
    if filepath.endswith('.cells'):
        return _parse_plaintext(content)
    elif filepath.endswith('.rle'):
        return _parse_rle(content)
    else:
        
        if 'x =' in content and 'y =' in content and 'rule =' in content:
            return _parse_rle(content)
        else:
            return _parse_plaintext(content)


def _parse_plaintext(content):
   
    lines = content.splitlines()
    live_cells = []
    max_col = 0
    row = 0
    started = False
    for line in lines:
        stripped = line.strip()
        if not started:
            if not stripped or stripped.startswith('!'):
                continue          # Skip comments before the pattern starts
            started = True
        else:
            if stripped.startswith('!'):
                continue         # Skip comment lines inside the file
        start = 0
        while start < len(line) and line[start] == ' ':
            start += 1
        for col, ch in enumerate(line[start:], start=start):
            if ch == 'O':
                live_cells.append((row, col))
            if col > max_col:
                max_col = col
        row += 1                  # blank rows count as a row
    height = row
    width = max_col + 1
    return width, height, live_cells

def _parse_rle(content):
   
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
                # If header line also contains data
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
    digits = ''
    
    while i < len(data):
        ch = data[i]
        if ch.isdigit():
            digits += ch
            i += 1
            continue
        else:
            count = int(digits) if digits else 1
            digits = ''
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
        if live_cells:
            max_row = max([cell[0] for cell in live_cells])
            max_col = max([cell[1] for cell in live_cells])
        else:
            max_row = 0
            max_col = 0

        width = max_col + 1
        height = max_row + 1
    
    return width, height, live_cells


class GameOfLife:

    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  # 8 connected kernel
        self.neighborhood[1, 1] = 0 
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N  # Grid dimensions
        self.cols = N 

    def getStates(self):

        return self.grid

    def getGrid(self):
      
        return self.getStates()

    def update_grid_fast(self, grid):
        if self.finite:
            boundary = 'fill'  
        else:
            boundary = 'wrap'   

        # Count Live neighbors using convolution
        neighbor_count = signal.convolve2d(
            grid,
            self.neighborhood,
            mode='same',
            boundary=boundary,
            fillvalue=0
        )

        alive_cells = (grid == 1)  
        dead_cells = (grid == 0)   

        # Survival
        survive = alive_cells & ((neighbor_count == 2) | (neighbor_count == 3))

        # Reproduction
        born = dead_cells & (neighbor_count == 3)

        #Build next generation
        new_grid = (survive | born).astype(np.uint)
        
        return new_grid
        

    def evolve(self):
       
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
                            neighbor_row = r + dr
                            neighbor_col = c + dc

                            if self.finite:
                                # Finite boundary: outside grid = dead
                                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                                    live_neighbors += self.grid[neighbor_row, neighbor_col]
                            else:
                                # Toroidal boundary
                                neighbor_row %= rows
                                neighbor_col %= cols
                                live_neighbors += self.grid[neighbor_row, neighbor_col]

                    # Apply Game of Life rules
                    if self.grid[r, c] == 1:  
                        if live_neighbors < 2 or live_neighbors > 3:
                            new_grid[r, c] = 0  
                        else:
                            new_grid[r, c] = 1 
                    else:  
                        if live_neighbors == 3:
                            new_grid[r, c] = 1  
                        else:
                            new_grid[r, c] = 0

            self.grid = new_grid

    def insertBlinker(self, index=(0, 0)):
        
        self.grid[index[0], index[1] + 1] = 1
        self.grid[index[0] + 1, index[1] + 1] = 1
        self.grid[index[0] + 2, index[1] + 1] = 1

    def insertGlider(self, index=(0, 0)):
       
        self.grid[index[0], index[1] + 1] = 1
        self.grid[index[0] + 1, index[1] + 2] = 1
        self.grid[index[0] + 2, index[1]] = 1
        self.grid[index[0] + 2, index[1] + 1] = 1
        self.grid[index[0] + 2, index[1] + 2] = 1

    def insertGliderGun(self, index=(0, 0)):

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
       
        width, height, live_cells = parse_pattern(filename)
        
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue