import json

# Configuration
# whisper_timestamped "P4.mp3" --model base --language en --output_format txt > "p4ets2020.txt"
input_file = 'p1ets2020.txt'
output_file = 'p1ets2020_clean.txt'

def process_whisper_output():
    try:
        # Step 1: Load the raw JSON text from the file
        with open(input_file, 'r', encoding='utf-8') as f:
            # Converting the text-based JSON into a Python dictionary
            data = json.load(f)

        # Step 2: Open output file to save clean results
        with open(output_file, 'w', encoding='utf-8') as out_f:
            
            # Loop through 'segments' only, ignoring the heavy 'words' objects
            for segment in data.get('segments', []):
                start = segment.get('start')
                end = segment.get('end')
                text = segment.get('text', '').strip()
                
                # Format: [Start - End] Text
                log_entry = f"[{start:>7.2f}s - {end:>7.2f}s] {text}"
                
                # Write to file and print to console
                out_f.write(log_entry + "\n")
                print(log_entry)

        print(f"\n[Done] Clean transcript saved to {output_file}")

    except json.JSONDecodeError:
        print(f"Error: The file {input_file} is not a valid JSON. Check your command output.")
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")

if __name__ == "__main__":
    process_whisper_output()