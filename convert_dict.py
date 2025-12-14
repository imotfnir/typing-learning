# -*- coding: utf-8 -*-
import json
import sys
from collections import defaultdict

def convert_dict_to_json(input_file, output_file):
    """
    Parses a RIME-style dictionary file and converts it to a JSON map
    where keys are characters and values are lists of codes.
    """
    char_to_codes = defaultdict(list)
    in_data_section = False

    print(f"Starting conversion of '{input_file}'...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                # The data section starts after the '...' line
                if line.strip() == '...':
                    in_data_section = True
                    continue
                
                if not in_data_section:
                    continue

                # Ignore comments and empty lines
                if line.startswith('#') or not line.strip():
                    continue

                # Split by tab, expecting character and code
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    char, code = parts[0], parts[1]
                    
                    # Ensure character and code are not empty
                    if not char or not code:
                        # print(f"Warning: Skipped empty entry at line {i}")
                        continue

                    # Add the code to the list for the character, avoiding duplicates
                    if code not in char_to_codes[char]:
                        char_to_codes[char].append(code)
                # else:
                    # print(f"Warning: Skipped malformed line {i}: '{line.strip()}'")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during file reading or parsing: {e}")
        sys.exit(1)

    print(f"Processed {len(char_to_codes)} unique characters.")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Use ensure_ascii=False to write Chinese characters directly
            # Use indent=2 for pretty-printing the JSON file
            json.dump(char_to_codes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"An error occurred during JSON writing: {e}")
        sys.exit(1)

    print(f"Successfully converted and saved to '{output_file}'.")

if __name__ == "__main__":
    # Basic command-line argument handling
    if len(sys.argv) != 3:
        print("Usage: python convert_dict.py <input_yaml_file> <output_json_file>")
        print("Example: python convert_dict.py newcj.dict.yaml newcj.json")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    convert_dict_to_json(input_path, output_path)
