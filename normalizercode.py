#@MTG-LIRA
import sys
import os
sys.path.insert(0, '.')

from ArabicNormalizer import ArabicNormalizer
from IndianNormalizer import DevanagariNormalizer

# --- USER CONFIG ---
# Input text file (the one you will use for inference)
INPUT_FILE = "/nlsasfs/home/bhasngrh/vedhe/Asian_TTT/ar-hi/data/nllb/hi.txt" 

# Output text file (the normalized version)
OUTPUT_FILE = "/nlsasfs/home/bhasngrh/vedhe/WMT2026/Ar-Hi/preprocessing/normalized/nllb_norm/hi.norm.txt"

# Create normalizer
#nl = EnglishNormalizer('en') 
nl = DevanagariNormalizer()

# Ensure output directory exists (if the file is in a subfolder)
output_dir = os.path.dirname(OUTPUT_FILE)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)

print(f"Processing file: {INPUT_FILE}")

try:
    count = 0
    with open(INPUT_FILE, 'r', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            line = line.strip() # Remove existing newline characters
            
            if line: # If line is not empty
                # Normalize
                normalized_line = nl.normalize(line)
                
                # Write to output file with a newline
                outfile.write(normalized_line + '\n')
            else:
                # Handle empty lines (keep them empty to maintain line alignment)
                outfile.write('\n')
            
            count += 1
            if count % 1000 == 0:
                print(f"Processed {count} lines...", end='\r')

    print(f"\n✅ Normalization complete! Processed {count} lines.")
    print(f"Saved at: {OUTPUT_FILE}")

except FileNotFoundError:
    print(f"❌ ERROR: Could not find the input file: {INPUT_FILE}")
except Exception as e:
    print(f"❌ An error occurred: {e}")