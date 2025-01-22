import subprocess
import os
import time
from datetime import datetime
import pandas as pd
import numpy as np
import shutil

def run_experiment(sizes, densities, weight_ranges, instances_per_config=3):
    """
    Run experiments with different configurations and collect results.
    
    Args:
        sizes: List of (n1, n2) tuples for graph sizes
        densities: List of density values
        weight_ranges: List of (min_weight, max_weight) tuples
        instances_per_config: Number of instances to generate for each configuration
    """
    # Create temporary directories for instances and results
    temp_instance_dir = "temp_instances"
    temp_results_dir = "temp_results"
    os.makedirs(temp_instance_dir, exist_ok=True)
    os.makedirs(temp_results_dir, exist_ok=True)
    
    # Create Excel writer
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = f"hungarian_experiments_{timestamp}.xlsx"
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    
    # Run experiments for each configuration
    for weight_min, weight_max in weight_ranges:
        sheet_name = f"weights_{weight_min}_{weight_max}"
        results = []
        
        print(f"\nRunning experiments for weight range [{weight_min}, {weight_max}]")
        
        for n1, n2 in sizes:
            print(f"\nTesting size: {n1}x{n2}")
            
            for density in densities:
                print(f"  Density: {density}")
                
                for instance in range(instances_per_config):
                    # Generate instance
                    gen_cmd = [
                        "python3", "generator.py",
                        str(n1), str(n2),
                        "--min-weight", str(weight_min),
                        "--max-weight", str(weight_max),
                        "--density", str(density),
                        "--output-dir", temp_instance_dir
                    ]
                    subprocess.run(gen_cmd, stdout=subprocess.DEVNULL)
                    
                    # Get the generated file name
                    instance_file = f"bipartite_n1_{n1}_n2_{n2}_d_{int(density*100)}_1.txt"
                    instance_path = os.path.join(temp_instance_dir, instance_file)
                    
                    # Run Hungarian algorithm
                    start_time = time.time()
                    hung_cmd = [
                        "python3", "hungarian.py",
                        instance_path,
                        "--output-dir", temp_results_dir
                    ]
                    
                    subprocess.run(hung_cmd, stdout=subprocess.DEVNULL)
                    total_time = time.time() - start_time

                    # Read results
                    result_file = os.path.join(temp_results_dir, 
                                             f"{os.path.splitext(instance_file)[0]}_results.txt")
                    with open(result_file, 'r') as f:
                        lines = f.readlines()
                        execution_time = float(lines[0].split(": ")[1].split()[0])
                        total_weight = float(lines[1].split(": ")[1])
                        matching_size = len(lines) - 3  # Subtract header lines
                    
                    # Store results
                    results.append({
                        'N1': n1,
                        'N2': n2,
                        'Density': density,
                        'Instance': instance + 1,
                        'Matching Size': matching_size,
                        'Total Weight': total_weight,
                        'Algorithm Time (s)': execution_time,
                        'Total Time (s)': total_time
                    })
        
        # Create DataFrame and save to Excel sheet
        df = pd.DataFrame(results)
        
        # Add summary statistics
        summary = df.groupby(['N1', 'N2', 'Density']).agg({
            'Matching Size': ['mean', 'std'],
            'Total Weight': ['mean', 'std'],
            'Algorithm Time (s)': ['mean', 'std'],
            'Total Time (s)': ['mean', 'std']
        }).round(4)
        
        # Save both detailed results and summary to different sheets
        df.to_excel(writer, sheet_name=f"{sheet_name}_detailed", index=False)
        summary.to_excel(writer, sheet_name=f"{sheet_name}_summary")
    
    # Save and close Excel file
    writer.close()
    
    # Cleanup temporary directories
    shutil.rmtree(temp_instance_dir)
    shutil.rmtree(temp_results_dir)
    
    print(f"\nExperiments completed. Results saved to {excel_file}")

def main():
    # Configuration for experiments
    sizes = [
        (50, 50),
        (100, 100),
        (250, 250)
    ]
    
    densities = [0.2, 0.3, 0.4, 0.6, 0.7, 0.8]
    
    weight_ranges = [
        (1, 10),
        (1, 100),
        (1, 1000)
    ]
    
    # Run experiments
    print("Starting Hungarian Algorithm experiments...")
    run_experiment(sizes, densities, weight_ranges, instances_per_config=3)

if __name__ == "__main__":
    main()