"""
run_pipeline.py
---------------
Master Orchestration Script for AI-Powered Fraud Network Analysis Data Pipeline.

Executes all pipeline stages sequentially:
1. Synthetic Generation (data_pipeline/generate/generate_data.py)
2. Data Cleaning & Hygiene (data_pipeline/cleaning/clean_data.py)
3. Schema Normalization (data_pipeline/normalization/normalize_data.py)
4. Quality & Referential Validation (data_pipeline/validation/validate_data.py)
5. Graph Processing & Sample Export (data_pipeline/processing/process_data.py)
"""

import os
import sys
import subprocess
import argparse


def run_command(cmd, step_name):
    print(f"\n==================================================")
    print(f"[*] Running Stage: {step_name}")
    print(f"[*] Command: {' '.join(cmd)}")
    print(f"==================================================")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"[ERROR] Stage '{step_name}' failed with return code {result.returncode}!")
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Master Data Pipeline Runner")
    parser.add_argument("--persons", type=int, help="Override number of persons")
    parser.add_argument("--events", type=int, help="Override total events")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--skip_generate", action="store_true", help="Skip synthetic data generation")
    args = parser.parse_args()

    py_exe = sys.executable

    # 1. Generation
    if not args.skip_generate:
        gen_cmd = [py_exe, "data_pipeline/generate/generate_data.py", "--seed", str(args.seed)]
        if args.persons:
            gen_cmd.extend(["--persons", str(args.persons)])
        if args.events:
            gen_cmd.extend(["--events", str(args.events)])
        run_command(gen_cmd, "1. Synthetic Data Generation")

    # 2. Cleaning
    clean_cmd = [py_exe, "data_pipeline/cleaning/clean_data.py"]
    run_command(clean_cmd, "2. Data Cleaning")

    # 3. Normalization
    norm_cmd = [py_exe, "data_pipeline/normalization/normalize_data.py"]
    run_command(norm_cmd, "3. Data Normalization")

    # 4. Validation
    val_cmd = [py_exe, "data_pipeline/validation/validate_data.py"]
    run_command(val_cmd, "4. Quality & Referential Integrity Validation")

    # 5. Graph Processing & Sample Export
    proc_cmd = [py_exe, "data_pipeline/processing/process_data.py"]
    run_command(proc_cmd, "5. Graph Relationship Extraction & Sample Export")

    print("\n==================================================")
    print("[SUCCESS] Full Data Pipeline Executed Successfully!")
    print("==================================================\n")


if __name__ == "__main__":
    main()
