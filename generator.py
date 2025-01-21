import random
import argparse
import os

def generate_bipartite_graph(n1: int, n2: int, min_weight: int, max_weight: int, density: float) -> list:
    """
    Generate a random bipartite graph with integer weights.
    
    Args:
        n1: Number of vertices in first partition
        n2: Number of vertices in second partition
        min_weight: Minimum edge weight (integer)
        max_weight: Maximum edge weight (integer)
        density: Percentage of possible edges to generate (0.0 to 1.0)
    
    Returns:
        List of tuples (v1, v2, weight) representing edges
    """
    # Calculate maximum possible edges
    max_edges = n1 * n2
    
    # Calculate number of edges to generate based on density
    num_edges = int(max_edges * density)
    
    # Generate all possible edges
    all_possible_edges = [(i, j) for i in range(n1) for j in range(n2)]
    
    # Randomly select edges
    selected_edges = random.sample(all_possible_edges, num_edges)
    
    # Generate integer weights for selected edges
    edges = []
    for v1, v2 in selected_edges:
        weight = random.randint(min_weight, max_weight)
        edges.append((v1, v2, weight))
    
    return edges

def save_graph(filename: str, n1: int, n2: int, edges: list):
    """
    Save the graph to a file.
    
    Args:
        filename: Output filename
        n1: Number of vertices in first partition
        n2: Number of vertices in second partition
        edges: List of tuples (v1, v2, weight)
    """
    with open(filename, 'w') as f:
        # Write number of vertices and edges
        f.write(f"{n1} {n2} {len(edges)}\n")
        
        # Write edges with integer weights
        for v1, v2, weight in edges:
            f.write(f"{v1} {v2} {weight}\n")

def main():
    parser = argparse.ArgumentParser(description='Generate random bipartite graph instances with integer weights')
    parser.add_argument('n1', type=int, help='Number of vertices in first partition')
    parser.add_argument('n2', type=int, help='Number of vertices in second partition')
    parser.add_argument('--min-weight', type=int, default=1, help='Minimum edge weight (integer)')
    parser.add_argument('--max-weight', type=int, default=100, help='Maximum edge weight (integer)')
    parser.add_argument('--density', type=float, default=0.7, 
                       help='Graph density (percentage of possible edges, between 0 and 1)')
    parser.add_argument('--num-instances', type=int, default=1, 
                       help='Number of instances to generate')
    parser.add_argument('--output-dir', type=str, default='instances',
                       help='Directory to save generated instances')
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.n1 <= 0 or args.n2 <= 0:
        print("Error: Number of vertices must be positive")
        return
    
    if args.min_weight >= args.max_weight:
        print("Error: Minimum weight must be less than maximum weight")
        return
    
    if args.density <= 0 or args.density > 1:
        print("Error: Density must be between 0 and 1")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate instances
    for i in range(args.num_instances):
        edges = generate_bipartite_graph(
            args.n1, args.n2, 
            args.min_weight, args.max_weight,
            args.density
        )
        
        # Generate filename
        filename = os.path.join(
            args.output_dir, 
            f'bipartite_n1_{args.n1}_n2_{args.n2}_d_{int(args.density*100)}_{i+1}.txt'
        )
        
        # Save graph
        save_graph(filename, args.n1, args.n2, edges)
        print(f"Generated instance saved to: {filename}")

if __name__ == "__main__":
    main()