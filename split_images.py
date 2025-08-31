#!/usr/bin/env python3

"""
Image splitting script for train/validation/test datasets
Usage: python split_images.py --source <source_dir> --output <output_dir> --train-ratio 0.8 --val-ratio 0.1 --test-ratio 0.1 --train-name train --val-name val --test-name test
"""

import os
import argparse
import shutil
import random
from pathlib import Path
from typing import List


def find_image_files(source_dir: Path) -> List[Path]:
    """Find all image files in the source directory."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(source_dir.glob(f'*{ext}'))
        image_files.extend(source_dir.glob(f'*{ext.upper()}'))
    
    return sorted(image_files)


def validate_ratios(train_ratio: float, val_ratio: float, test_ratio: float) -> bool:
    """Validate that ratios sum to approximately 1.0."""
    ratio_sum = train_ratio + val_ratio + test_ratio
    return 0.99 <= ratio_sum <= 1.01


def split_images(source_dir: str, output_dir: str, train_ratio: float = 0.8, 
                val_ratio: float = 0.1, test_ratio: float = 0.1,
                train_name: str = "train", val_name: str = "val", 
                test_name: str = "test", shuffle: bool = True) -> None:
    """Split images into training, validation, and test sets."""
    
    # Convert to Path objects
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    # Validate source directory exists
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist")
    
    # Validate ratios
    if not validate_ratios(train_ratio, val_ratio, test_ratio):
        ratio_sum = train_ratio + val_ratio + test_ratio
        raise ValueError(f"Ratios must sum to 1.0 (got {ratio_sum})")
    
    # Create output directories
    train_dir = output_path / train_name
    val_dir = output_path / val_name
    test_dir = output_path / test_name
    
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all image files
    print(f"Finding images in {source_dir}...")
    image_files = find_image_files(source_path)
    
    if not image_files:
        raise ValueError(f"No image files found in {source_dir}")
    
    total_images = len(image_files)
    print(f"Found {total_images} images")
    
    # Shuffle files if requested
    if shuffle:
        print("Shuffling images...")
        random.shuffle(image_files)
    
    # Calculate split counts
    train_count = int(total_images * train_ratio)
    val_count = int(total_images * val_ratio)
    test_count = total_images - train_count - val_count
    
    print("Split plan:")
    print(f"  Training: {train_count} images -> {train_dir}")
    print(f"  Validation: {val_count} images -> {val_dir}")
    print(f"  Test: {test_count} images -> {test_dir}")
    print()
    
    # Split and copy files
    print("Copying files...")
    
    # Training set
    print("Copying training set...")
    for i, file_path in enumerate(image_files[:train_count]):
        shutil.copy2(file_path, train_dir)
        if (i + 1) % 100 == 0:
            print(f"  Copied {i + 1}/{train_count} training images")
    
    # Validation set
    print("Copying validation set...")
    val_start = train_count
    val_end = train_count + val_count
    for i, file_path in enumerate(image_files[val_start:val_end]):
        shutil.copy2(file_path, val_dir)
        if (i + 1) % 100 == 0:
            print(f"  Copied {i + 1}/{val_count} validation images")
    
    # Test set
    print("Copying test set...")
    test_start = train_count + val_count
    for i, file_path in enumerate(image_files[test_start:]):
        shutil.copy2(file_path, test_dir)
        if (i + 1) % 100 == 0:
            print(f"  Copied {i + 1}/{test_count} test images")
    
    # Verify counts
    actual_train = len(list(train_dir.glob('*')))
    actual_val = len(list(val_dir.glob('*')))
    actual_test = len(list(test_dir.glob('*')))
    
    print()
    print("✅ Split complete!")
    print("Final counts:")
    print(f"  Training: {actual_train} images")
    print(f"  Validation: {actual_val} images")
    print(f"  Test: {actual_test} images")
    print(f"  Total: {actual_train + actual_val + actual_test} images")


def main():
    parser = argparse.ArgumentParser(
        description="Split images into training, validation, and test datasets"
    )
    
    source_dir = "./non_aaa_all"
    output_dir = "."
    train_folder = "non_aaa_train"
    val_folder = "non_aaa_val"
    test_folder = "non_aaa_test"

    # Required arguments
    parser.add_argument("--source", default=source_dir, 
                       help="Source directory containing images")
    parser.add_argument("--output", default=output_dir,
                       help="Output directory for split datasets")
    
    # Optional arguments
    parser.add_argument("--train-ratio", type=float, default=0.8,
                       help="Training set ratio (default: 0.8)")
    parser.add_argument("--val-ratio", type=float, default=0.1,
                       help="Validation set ratio (default: 0.1)")
    parser.add_argument("--test-ratio", type=float, default=0.1,
                       help="Test set ratio (default: 0.1)")
    parser.add_argument("--train-name", default=train_folder,
                       help="Training folder name (default: train)")
    parser.add_argument("--val-name", default=val_folder,
                       help="Validation folder name (default: val)")
    parser.add_argument("--test-name", default=test_folder,
                       help="Test folder name (default: test)")
    parser.add_argument("--no-shuffle", action="store_true",
                       help="Don't shuffle files before splitting")
    
    args = parser.parse_args()
    
    try:
        split_images(
            source_dir=args.source,
            output_dir=args.output,
            train_ratio=args.train_ratio,
            val_ratio=args.val_ratio,
            test_ratio=args.test_ratio,
            train_name=args.train_name,
            val_name=args.val_name,
            test_name=args.test_name,
            shuffle=not args.no_shuffle
        )
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
