"""
run_pipeline.py
===============
Convenience script to:
  1. Execute the Jupyter notebook end-to-end (kernel execution)
  2. Generate the PDF report

Usage:
    python run_pipeline.py

Requirements:
    pip install -r requirements.txt
"""

import subprocess
import sys
import time
from pathlib import Path

NOTEBOOK = "loan_default_prediction.ipynb"
REPORT   = "generate_report.py"


def run(cmd, desc):
    print(f"\n{'='*60}")
    print(f"  {desc}")
    print(f"{'='*60}")
    start = time.time()
    result = subprocess.run(cmd, shell=True)
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"\n❌ Step failed (exit code {result.returncode}). Check output above.")
        sys.exit(result.returncode)
    print(f"\n✅ Done in {elapsed/60:.1f} min")


if __name__ == "__main__":
    # Step 1: Run notebook
    if Path(NOTEBOOK).exists():
        run(
            f'jupyter nbconvert --to notebook --execute --inplace '
            f'--ExecutePreprocessor.timeout=3600 "{NOTEBOOK}"',
            f"Executing notebook: {NOTEBOOK}  (may take 15–30 min on full dataset)"
        )
    else:
        print(f"❌ Notebook not found: {NOTEBOOK}")
        sys.exit(1)

    # Step 2: Generate PDF
    if Path(REPORT).exists():
        run(f'python "{REPORT}"', "Generating PDF report")
    else:
        print(f"❌ Report script not found: {REPORT}")
        sys.exit(1)

    print("\n" + "="*60)
    print("🎉 FULL PIPELINE COMPLETE")
    print("  ├── Notebook executed  : loan_default_prediction.ipynb")
    print("  ├── Predictions saved  : loan_default_predictions.csv")
    print("  ├── Metrics saved      : model_metrics.csv")
    print("  ├── Plots saved        : plots/")
    print("  └── PDF report         : Loan_Default_Report.pdf")
    print("="*60)
