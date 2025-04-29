#!/usr/bin/env python3
"""
Extract random sample of soprano melody (stem 1) from test split of CocoChorales dataset.
Copies N random soprano MIDI files to an output input_midi directory for inference,
and renames them uniquely by track ID to avoid overwrites.
"""
import os
import argparse
import random
from pathlib import Path
import shutil

def extract_soprano_melodies(test_dir: Path, output_dir: Path, num_samples: int, seed: int = 42):
    """
    Randomly sample num_samples melody MIDI files from test_dir stems_midi/1_trumpet.mid
    and copy to output_dir with unique filenames.
    """
    random.seed(seed)
    # Gather all soprano paths
    soprano_paths = []
    for track in test_dir.iterdir():
        if not track.is_dir():
            continue
        stem_dir = track / 'stems_midi'
        soprano = stem_dir / '1_trumpet.mid'
        if soprano.exists():
            soprano_paths.append(soprano)
    total = len(soprano_paths)
    if total == 0:
        raise RuntimeError(f"No soprano files found in {test_dir}")
    if num_samples > total:
        raise ValueError(f"Requested {num_samples} samples, but only {total} available")

    # Random sample
    sampled = random.sample(soprano_paths, num_samples)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Copy files with unique names
    for src in sampled:
        # derive unique track ID from parent folder name
        track_id = src.parents[1].name  # two levels up: track folder
        dst_name = f"{track_id}_soprano.mid"
        dst = output_dir / dst_name
        shutil.copy(src, dst)
    print(f"Copied {num_samples} soprano MIDI files to {output_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract random soprano MIDI samples from test split')
    parser.add_argument('--test-dir',   type=Path, default=Path('/Volumes/Kid_Rage 1/[_Database_]/CocoChorales/cocochorales_tiny_v1_midi/test'),
                        help='Path to test split directory')
    parser.add_argument('--output-dir', type=Path, default=Path('/Users/saintpeter/Desktop/Auto_Harmonizer/Inference/input_midi/1'),
                        help='Where to copy sampled soprano MIDIs')
    parser.add_argument('--num',        type=int, default=100,
                        help='Number of random samples to extract')
    parser.add_argument('--seed',       type=int, default=42,
                        help='Random seed for reproducibility')
    args = parser.parse_args()
    extract_soprano_melodies(args.test_dir, args.output_dir, args.num, args.seed)
