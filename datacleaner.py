#@MTG-LIRA

import sys
import re
import os

# ----- USER CONFIGURATION -----

INPUT_FILE = "/nlsasfs/home/bhasngrh/vedhe/WMT2026/Indic-LR/En-As/data/en.norm.txt" 
    
OUTPUT_FILE = "/nlsasfs/home/bhasngrh/vedhe/WMT2026/Indic-LR/En-As/data/en.clean.txt"

# Language mode: 'src' (English) or 'tgt' (Target Lang)
LANG = 'src' 
# ------------------------------


UNWANTED_BOUNDARY_CHARS = r'[●;*:#\-ः\s><]'

def remove_mixed_hindi_sentences(text):
    """
    Detects and removes segments that are predominantly Hindi (Devanagari script),
    while preserving segments that are predominantly English.
    """
    # Optimization: If no Devanagari, return immediately
    if not re.search(r'[\u0980-\u09FF]', text):
        return text

    # Split text by sentence delimiters
    parts = re.split(r'([।?!.])', text)
    cleaned_parts = []
    skip_next_delimiter = False
    
    for part in parts:
        # If delimiter
        if re.match(r'^[।?!.\s]+$', part):
            if skip_next_delimiter:
                skip_next_delimiter = False 
                continue
            else:
                cleaned_parts.append(part)
                continue
        
        # If empty/whitespace
        if not part.strip():
            cleaned_parts.append(part)
            continue

        # Density Check
        dev_count = len(re.findall(r'[\u0980-\u09FF]', part))
        lat_count = len(re.findall(r'[a-zA-Z]', part))
        
        # Remove if Devanagari dominant
        if dev_count > lat_count and dev_count > 2:
            skip_next_delimiter = True 
            continue 
        else:
            skip_next_delimiter = False
            cleaned_parts.append(part)

    return "".join(cleaned_parts)

def clean_sentence(line, lang='src'):
    """
    Cleans a single sentence string.
    """
    original_newline = '\n' # Always preserve the newline structure
    
    # 1. Initial strip (but keep track if it was empty)
    line_content = line.strip()
    
    if not line_content:
        return original_newline

    # 2. Remove mixed Hindi sentences (Only if source is English)
    if lang == 'src':
        line_content = remove_mixed_hindi_sentences(line_content)
        if not line_content.strip():
            return original_newline

    # 3. Remove Unwanted Boundary Symbols
    start_pattern = r'^' + UNWANTED_BOUNDARY_CHARS + r'+'
    end_pattern = UNWANTED_BOUNDARY_CHARS + r'+$'
    line_content = re.sub(start_pattern, '', line_content)
    line_content = re.sub(end_pattern, '', line_content)
    
    # 4. Cleanup Punctuation
    # Collapse multiple Dandas or dots
    line_content = re.sub(r'।{2,}', '।', line_content)
    line_content = re.sub(r'([.,?!;:\u0964])\1+', r'\1', line_content)
    
    # Strip quotes (Caution: In test sets, sometimes quotes are needed, but keeping your logic)
    line_content = line_content.strip('"').strip()

    # 5. Final Formatting
    if lang == 'tgt':
        # Target (Indian Lang): Ensure exactly one Danda
        line_content = line_content.rstrip('।') + '।\n'
    else:
        # Source (English): Ensure newline
        line_content = line_content + '\n'
        
    return line_content

# --- MAIN EXECUTION ---

print(f"Processing file: {INPUT_FILE}")
print(f"Mode: {LANG}")

if not os.path.exists(INPUT_FILE):
    print(f"❌ ERROR: Input file not found: {INPUT_FILE}")
    sys.exit(1)

try:
    count = 0
    with open(INPUT_FILE, 'r', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            cleaned_line = clean_sentence(line, lang=LANG)
            outfile.write(cleaned_line)
            count += 1
            
            if count % 1000 == 0:
                print(f"Processed {count} lines...", end='\r')

    print(f"\n✅ Cleaning complete! Processed {count} lines.")
    print(f"Saved at: {OUTPUT_FILE}")

except Exception as e:
    print(f"\n❌ An error occurred: {e}")