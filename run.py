#!/usr/bin/env python3
"""
Quick Run Script - Execute the full pipeline
Built by: [Your Name]
"""

import subprocess
import sys

def run_pipeline():
    """Run the complete transformation pipeline"""
    print("="*60)
    print("[LAUNCH] RUNNING FULL PIPELINE")
    print("="*60)
    
    # Step 1: Transform story
    print("\n[BOOK] Step 1: Transforming narrative structure...")
    result = subprocess.run([sys.executable, "transformer.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"[FAIL] Error: {result.stderr}")
        return False
    
    # Step 2: Generate scenes
    print("\n[MOVIE] Step 2: Generating scenes with dialogue...")
    result = subprocess.run([sys.executable, "scene_generator.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"[FAIL] Error: {result.stderr}")
        return False
    
    print("\n" + "="*60)
    print("[DONE] PIPELINE COMPLETE!")
    print("="*60)
    print("\nGenerated files:")
    print("  [DOC] transformed_story.json - Structured data")
    print("  [DOC] reimagined_story.md - Story outline")
    print("  [DOC] complete_story.md - Full narrative with dialogue")
    print("\nView complete_story.md for the final result!")
    
    return True

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
