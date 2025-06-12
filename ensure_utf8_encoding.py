import os
import sys
import chardet # Make sure chardet is installed: pip install chardet
import argparse # Import argparse at the top

def verify_and_fix_encoding(directory_path):
    """
    Verifies and fixes the encoding of .txt files in a directory to UTF-8.

    Args:
        directory_path (str): The path to the directory containing .txt files.

    Returns:
        tuple: (processed_files, fixed_files, failed_files_list)
    """
    processed_files = 0
    fixed_files = 0
    failed_files_list = []

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found - {directory_path}")
        return 0, 0, []

    print(f"Starting encoding verification and fixing for files in: {directory_path}")

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            processed_files += 1
            original_encoding = None
            try:
                with open(file_path, 'rb') as f_raw:
                    raw_data = f_raw.read()

                # 1. Try decoding as UTF-8 directly
                try:
                    text_content = raw_data.decode('utf-8')
                    print(f"OK: '{filename}' is already UTF-8.")
                    continue # Already UTF-8, move to next file
                except UnicodeDecodeError:
                    # Not UTF-8, proceed to detect and convert
                    pass

                # 2. Detect encoding using chardet
                detection_result = chardet.detect(raw_data)
                original_encoding = detection_result['encoding']
                confidence = detection_result['confidence']

                if original_encoding and confidence > 0.7: # Use a confidence threshold
                    print(f"INFO: '{filename}' detected as {original_encoding} (Confidence: {confidence:.2f}). Attempting conversion to UTF-8.")
                    text_content = raw_data.decode(original_encoding)

                    # 3. Write back as UTF-8
                    with open(file_path, 'w', encoding='utf-8') as f_utf8:
                        f_utf8.write(text_content)
                    print(f"FIXED: '{filename}' converted from {original_encoding} to UTF-8.")
                    fixed_files += 1
                elif original_encoding:
                    print(f"WARNING: '{filename}' detected as {original_encoding} but confidence is low ({confidence:.2f}). Skipping conversion.")
                    failed_files_list.append(filename + f" (low confidence: {original_encoding})")
                else:
                    print(f"ERROR: Could not detect encoding for '{filename}'. Skipping.")
                    failed_files_list.append(filename + " (detection failed)")

            except Exception as e:
                print(f"ERROR: Failed to process '{filename}'. Reason: {e}")
                failed_files_list.append(filename + f" (exception: {e})")

    print(f"\n--- Encoding Fix Summary ---")
    print(f"Total files processed: {processed_files}")
    print(f"Files successfully converted/verified as UTF-8: {processed_files - len(failed_files_list)}")
    print(f"Files newly converted to UTF-8: {fixed_files}")
    print(f"Files failed or skipped: {len(failed_files_list)}")
    if failed_files_list:
        print("Failed/Skipped files:")
        for f_name in failed_files_list:
            print(f"  - {f_name}")
    print("---------------------------\n")
    return processed_files, fixed_files, failed_files_list

if __name__ == "__main__":
    # Ensure chardet is available
    try:
        import chardet
    except ImportError:
        print("Error: 'chardet' library not found. Please install it by running: pip install chardet")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Verify and fix file encodings to UTF-8.")
    parser.add_argument("--dir", type=str, default="samples", help="Directory containing the .txt files to process.")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"Error: The specified directory '{args.dir}' does not exist.")
        sys.exit(1)
        
    verify_and_fix_encoding(args.dir)
