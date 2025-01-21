from typing import Dict, List, Set, Tuple
import numpy as np
import time
import sys
import os
import argparse

class HungarianAlgorithm:
    # [Previous class implementation remains the same]
    def __init__(self, n1: int, n2: int):
        self.n1 = n1
        self.n2 = n2
        self.n = max(n1, n2)  # We need a square matrix
        self.weights = np.zeros((self.n, self.n))
        self.X = range(self.n)
        self.Y = range(self.n)
        self.matching: Dict[int, int] = {}
        
    def set_weight(self, v1: int, v2: int, weight: float):
        """Set weight for edge (v1,v2)"""
        self.weights[v1][v2] = weight
    
    def _initial_labeling(self) -> Dict[int, float]:
        """Create initial labeling where l(y)=0 for all y in Y and l(x)=max(w(x,y)) for all x in X"""
        labeling = {}
        for x in self.X:
            labeling[x] = max(self.weights[x])
        for y in self.Y:
            labeling[y + self.n] = 0
        return labeling
    
    def _equality_graph(self) -> Set[Tuple[int, int]]:
        """Return edges in the equality graph (where l(u) + l(v) = w(u,v))"""
        El = set()
        for x in self.X:
            for y in self.Y:
                if abs(self.labeling[x] + self.labeling[y + self.n] - self.weights[x][y]) < 1e-10:
                    El.add((x, y))
        return El
    
    def _find_augmenting_path(self, start: int, El: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Find augmenting path starting from vertex start using DFS"""
        S: Set[int] = set()
        T: Set[int] = set()
        path: List[Tuple[int, int]] = []
        visited = set()
        
        def dfs(u: int) -> bool:
            if u in visited:
                return False
            visited.add(u)
            
            if u < self.n:
                S.add(u)
                for v in self.Y:
                    if (u, v) in El:
                        if v not in self.matching.values():
                            path.append((u, v))
                            return True
                        if v not in T:
                            T.add(v)
                            matched_x = [k for k, val in self.matching.items() if val == v][0]
                            path.append((u, v))
                            if dfs(matched_x):
                                return True
                            path.pop()
            return False
        
        if dfs(start):
            return path
        return []
    
    def _improve_labeling(self, S: Set[int], T: Set[int]) -> None:
        """Improve the current labeling"""
        delta = float('inf')
        for x in S:
            for y in self.Y:
                if y not in T:
                    delta = min(delta, 
                              self.labeling[x] + self.labeling[y + self.n] - self.weights[x][y])
        
        for x in S:
            self.labeling[x] -= delta
        for y in T:
            self.labeling[y + self.n] += delta
    
    def solve(self) -> Tuple[Dict[int, int], float]:
        """Find maximum weight perfect matching using Hungarian algorithm"""
        self.labeling = self._initial_labeling()
        
        while len(self.matching) < min(self.n1, self.n2):
            unmatched = set(range(self.n1)) - set(self.matching.keys())
            u = next(iter(unmatched))
            
            El = self._equality_graph()
            path = self._find_augmenting_path(u, El)
            
            if path:
                for x, y in path:
                    self.matching[x] = y
            else:
                S = set()
                T = set()
                self._improve_labeling(S, T)
        
        total_weight = sum(self.weights[x][y] for x, y in self.matching.items())
        return self.matching, total_weight

def read_graph(filename: str) -> HungarianAlgorithm:
    """Read graph from file and return Hungarian Algorithm instance"""
    with open(filename, 'r') as f:
        # Read first line containing n1, n2, m
        n1, n2, m = map(int, f.readline().split())
        
        # Initialize Hungarian Algorithm
        hungarian = HungarianAlgorithm(n1, n2)
        
        # Read m edges
        for _ in range(m):
            v1, v2, p = map(float, f.readline().split())
            hungarian.set_weight(int(v1), int(v2), p)
            
    return hungarian

def save_results(filename: str, matching: Dict[int, int], total_weight: float, execution_time: float):
    """Save results to file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(f"Execution Time: {execution_time:.6f} seconds\n")
        f.write(f"Total Weight: {total_weight}\n")
        f.write("Matching:\n")
        for v1, v2 in matching.items():
            f.write(f"{v1} {v2}\n")

def main():
    parser = argparse.ArgumentParser(description='Hungarian Algorithm for Maximum Weight Matching')
    parser.add_argument('input_file', type=str, help='Input file containing the graph')
    parser.add_argument('--output-dir', type=str, default='results', 
                       help='Directory to save results (default: results)')
    parser.add_argument('--output-file', type=str, 
                       help='Output filename (default: based on input filename)')
    
    args = parser.parse_args()
    
    try:
        # Read and solve
        hungarian = read_graph(args.input_file)
        
        # Start timing
        start_time = time.time()

        matching, total_weight = hungarian.solve()
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Determine output filename
        if args.output_file:
            output_filename = os.path.join(args.output_dir, args.output_file)
        else:
            input_basename = os.path.splitext(os.path.basename(args.input_file))[0]
            output_filename = os.path.join(args.output_dir, f"{input_basename}_results.txt")
        
        # Save results
        save_results(output_filename, matching, total_weight, execution_time)
        
        print(f"Results saved to: {output_filename}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file '{args.input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()