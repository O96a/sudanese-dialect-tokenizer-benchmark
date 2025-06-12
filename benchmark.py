import argparse
from transformers import AutoTokenizer
import pandas as pd
import json
from wcwidth import wcswidth
import tiktoken  # Ensure TikToken is installed and imported

# Initialize TikToken for GPT-4, assuming this is the correct way to do so
gpt4_tokenizer = tiktoken.encoding_for_model("gpt-4")

# Function to read JSON data from a file
def load_dataset_from_file(file_path):
    print(f"Loading dataset from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    print("Dataset loaded successfully.")
    return dataset

# Benchmarking function
def benchmark_tokenizers(dataset, tokenizers, ignore_numbers=False):
    print("Starting tokenizer benchmarking...")
    results = []

    for item in dataset:
        row = {
            'ID': item['id'],
            'Filename': item['filename'][:30], 
            'Class': item['classification'],
            # 'Subclass': item.get('subclassification', '')  # Removed Subclass
        }

        for model, tokenizer in tokenizers.items():
            tokens = []
            if isinstance(tokenizer, type(gpt4_tokenizer)):
                token_ids = tokenizer.encode(item['prompt'])
                for token_id in token_ids:
                    token = tokenizer.decode([token_id])
                    if ignore_numbers and token.isdigit():
                        continue  # Skip numeric tokens
                    tokens.append(token)
            else:
                temp_tokens = tokenizer.tokenize(item['prompt'])
                if ignore_numbers:
                    tokens = [token for token in temp_tokens if not token.isdigit()]
                else:
                    tokens = temp_tokens

            # Extract the part of the model name after '/'
            model_name = model.split('/')[-1]  # Split on '/' and take the last part
            row[model_name] = len(tokens)  # Token count

        results.append(row)

    print("Benchmarking completed.")
    return results

def print_dataframe(df, col_widths):
    # Print the headers with proper spacing
    header = " | ".join(f"{name:{col_widths.get(name, 10)}}" for name in df.columns)
    print(header)

    # Print a separator
    print("-" * len(header))

    # Print each row with proper spacing
    for _, row in df.iterrows():
        row_str = " | ".join(f"{adjust_width(str(value), col_widths.get(name, 10))}" for name, value in row.items())
        print(row_str)

def adjust_width(text, desired_width):
    if '\n' in text:
        text = text.split('\n', 1)[0] + '...'
    current_width = wcswidth(text)
    if current_width == desired_width:
        return text
    elif current_width < desired_width:
        return text + ' ' * (desired_width - current_width)
    else:
        truncated_text = text
        while wcswidth(truncated_text + '...') > desired_width:
            truncated_text = truncated_text[:-1]
        return truncated_text + '...'

def main():
    parser = argparse.ArgumentParser(description='Benchmark Tokenizers')
    parser.add_argument('--file', type=str, required=True, help='Path to the JSON dataset file')
    parser.add_argument('--models', nargs='*', help='List of tokenizer models to benchmark. If not provided, a default list will be used.')
    parser.add_argument('--ignore-numbers', action='store_true', help='Ignore numeric tokens in the benchmark')

    args = parser.parse_args()

    # Define default models
    default_models = [
        "gpt-4",
        "aubmindlab/bert-base-arabertv02",
        "google/gemma-7b-it",
        "deepseek-ai/deepseek-llm-7b-base"  # Added deepseek model
    ]

    # Use provided models or default if none are provided
    models_to_benchmark = args.models if args.models else default_models
    if not models_to_benchmark: # Should not happen with nargs='*' and default_models, but as a safeguard
        print("No models specified and no default models available. Exiting.")
        return

    dataset = load_dataset_from_file(args.file)

    print("Loading tokenizer models...")
    tokenizers = {}
    for model in models_to_benchmark: # Use models_to_benchmark
        if model.lower() == "gpt-4":
            tokenizers[model] = gpt4_tokenizer
        else:
            tokenizers[model] = AutoTokenizer.from_pretrained(model)
    print(f"Models loaded: {', '.join(models_to_benchmark)}") # Use models_to_benchmark

    results = benchmark_tokenizers(dataset, tokenizers, ignore_numbers=args.ignore_numbers)

    df_results = pd.DataFrame(results)

    model_names = [model.split('/')[-1] for model in models_to_benchmark] # Use models_to_benchmark
    max_model_name_length = max(len(name) for name in model_names) if model_names else 10 # Handle empty model_names

    # Adjust column widths for better fit
    col_widths = {
        'ID': 3,  # Reduced width
        'Filename': 20,  # Reduced width
        'Class': 10,  # Reduced width
        # 'Subclass': 10,  # Removed Subclass
    }
    for model_name in model_names:
        col_widths[model_name] = max(max_model_name_length, len(model_name), 8) # Ensure a minimum width for model columns

    print_dataframe(df_results, col_widths)

    # Save results to CSV and HTML
    try:
        csv_path = "benchmark_results.csv"
        html_path = "benchmark_results.html"
        df_results.to_csv(csv_path, index=False, encoding='utf-8')
        df_results.to_html(html_path, index=False, classes=['table', 'table-striped', 'table-hover'])
        print(f"\nResults saved to {csv_path} and {html_path}")
    except Exception as e:
        print(f"\nError saving results to files: {e}")

if __name__ == "__main__":
    main()
