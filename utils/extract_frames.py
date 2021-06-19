import subprocess
import sys
import os
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Extract frames from video file. Needs ffmpeg to work.')

parser.add_argument('--in', dest='infile', type=str, help='Input video file. [REQUIRED]')
parser.add_argument('--dir', dest='outdir', default='.', type=str, help='Output directory. Defaults to cwd. [REQUIRED]')
parser.add_argument('--fps', dest='fps', type=int, help='Number of frames to extract per second of video. [REQUIRED]')
parser.add_argument('--prefix', dest='prefix', default='img', type=str, help='Prefix for extracted filenames. Defaults to "img"')

args = parser.parse_args()

OUTDIR = os.path.abspath(args.outdir)
INFILE = os.path.abspath(args.infile)

Path(OUTDIR).mkdir(parents=True, exist_ok=True)

task = subprocess.run([
						'ffmpeg',
						'-i',
						INFILE,
						'-vf',
						'fps={fps}/1'.format(fps=args.fps),
						'{outdir}/{prefix}%02d.jpg'.format(outdir=OUTDIR, prefix=args.prefix)
					], capture_output=True)

sys.stdout.buffer.write(task.stdout)
sys.stderr.buffer.write(task.stderr)
sys.exit(task.returncode)