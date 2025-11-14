#!/usr/bin/env python3
"""
Combine positive and negative warhead images into combined train/val/test folders
"""

import os
import shutil
from pathlib import Path

def combine_splits(base_dir: str):
    """Combine yes_warheads and no_warheads splits into combined folders."""
    
    base_path = Path(base_dir)
    
    splits = ['train', 'val', 'test']
    
    for split in splits:
        yes_dir = base_path / f'yes_warheads_{split}'
        no_dir = base_path / f'no_warheads_{split}'
        combined_dir = base_path / f'warheads_{split}_combined'
        
        # Create combined directory
        combined_dir.mkdir(exist_ok=True)
        
        # Count images
        yes_count = len(list(yes_dir.glob('*.png'))) if yes_dir.exists() else 0
        no_count = len(list(no_dir.glob('*.png'))) if no_dir.exists() else 0
        
        print(f"\nCombining {split} set:")
        print(f"  Positive images: {yes_count}")
        print(f"  Negative images: {no_count}")
        
        # Copy positive images
        if yes_dir.exists():
            for img_file in yes_dir.glob('*.png'):
                shutil.copy2(img_file, combined_dir)
        
        # Copy negative images
        if no_dir.exists():
            for img_file in no_dir.glob('*.png'):
                shutil.copy2(img_file, combined_dir)
        
        # Verify
        total = len(list(combined_dir.glob('*.png')))
        print(f"  Total in combined: {total}")
    
    print("\n✅ All splits combined successfully!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Combine warhead image splits")
    parser.add_argument('--base-dir', default='Russian_Warhead_Storage',
                       help='Base directory containing the split folders')
    
    args = parser.parse_args()
    
    combine_splits(args.base_dir)

