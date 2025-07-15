import os
import random
import shutil
import argparse

def sample_and_move_images(source_dir, dest_dir, sample_size, extensions=('.png', '.jpg', '.jpeg')):
    # Get all image files from the source directory
    all_images = [
        f for f in os.listdir(source_dir)
        if f.lower().endswith(extensions) and os.path.isfile(os.path.join(source_dir, f))
    ]
    
    print(f"Found {len(all_images)} image(s) in '{source_dir}'.")

    if sample_size > len(all_images):
        raise ValueError(f"Sample size ({sample_size}) is greater than total images ({len(all_images)}).")

    # Take a random sample of image filenames
    sampled_images = random.sample(all_images, sample_size)

    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    # Move sampled images
    for img_name in sampled_images:
        src_path = os.path.join(source_dir, img_name)
        dst_path = os.path.join(dest_dir, img_name)
        shutil.move(src_path, dst_path)
        print(f"Moved: {img_name}")

    print(f"\nMoved {sample_size} images to '{dest_dir}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomly sample and move images.")
    parser.add_argument("--source", default="archival_images/AAA_training_images", help="Source folder with images")
    parser.add_argument("--dest", default="AAA_eval_images", help="Destination folder for sampled images")
    parser.add_argument("--n", type=int, required=True, help="Number of images to sample")

    args = parser.parse_args()

    sample_and_move_images(args.source, args.dest, args.n)