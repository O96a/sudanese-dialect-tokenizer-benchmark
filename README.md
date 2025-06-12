# Sudanese Dialect Tokenizer Benchmark

This project benchmarks various tokenizers on a dataset of Sudanese dialect text. It aims to compare the tokenization efficiency (token count) of different models for this specific low-resource language variant.

## Project Structure

```
.
├── benchmark.py            # Main script to run the tokenizer benchmark.
├── dataset.json            # JSON file defining the dataset structure and pointing to sample files.
├── ensure_utf8_encoding.py # Utility script to verify and fix file encodings to UTF-8.
├── samples/                # Directory containing the Sudanese dialect text samples.
│   ├── *.txt               # Various text files with Sudanese dialect content.
├── benchmark_results.csv   # CSV output of the benchmark results.
├── benchmark_results.html  # HTML output of the benchmark results.
└── README.md               # This file.
```

## Setup

1.  **Clone the repository (or set up the project files).**
2.  **Create a Python virtual environment and activate it:**
    ```bash
    python -m venv benchmark_env
    benchmark_env\Scripts\activate 
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt 
    ```
    (You will need to create a `requirements.txt` file. See below.)

## `requirements.txt`

Create a `requirements.txt` file with the following content:

```
transformers
pandas
wcwidth
tiktoken
chardet
huggingface_hub
```

## Usage

### 1. Prepare Sample Data

-   Place your Sudanese dialect text files (UTF-8 encoded) in the `samples/` directory.
-   Update `dataset.json` to reflect your sample files. Each entry should have an `id`, `filename` (matching a file in `samples/`), `classification` (e.g., "Sudanese Dialect"), and `prompt` (the actual text content from the file).

    **Example `dataset.json` entry:**
    ```json
    [
      {
        "id": "001",
        "filename": "sudanese-phrases.txt",
        "classification": "Sudanese Dialect",
        "subclassification": "", // This field is present in the JSON but not used in the final table
        "prompt": "بعض العبارات والجمل باللهجة السودانية..."
      }
      // ... more entries
    ]
    ```

### 2. Ensure UTF-8 Encoding (Optional but Recommended)

Run the `ensure_utf8_encoding.py` script to check and convert any non-UTF-8 files in the `samples/` directory:

```bash
python ensure_utf8_encoding.py --dir samples
```

### 3. Run the Benchmark

Execute the `benchmark.py` script:

```bash
python benchmark.py --file dataset.json 
```

**Optional arguments for `benchmark.py`:**

-   `--models <model_name_or_path ...>`: Specify a list of Hugging Face model names/paths or "gpt-4" to benchmark. If not provided, a default list will be used:
    -   `gpt-4`
    -   `aubmindlab/bert-base-arabertv02`
    -   `google/gemma-7b-it`
    -   `deepseek-ai/deepseek-llm-7b-base`
-   `--ignore-numbers`: If set, numeric tokens will be ignored in the count.

**Example with specific models:**

```bash
python benchmark.py --file dataset.json --models gpt-4 aubmindlab/bert-base-arabertv02
```

### 4. View Results

-   The benchmark results will be printed to the console.
-   The results will also be saved in `benchmark_results.csv` and `benchmark_results.html`.

## Hugging Face Login

Some models (e.g., `google/gemma-7b-it`) require you to be logged into your Hugging Face account. If you encounter issues with model access:

1.  **Install Hugging Face CLI (if not already installed with `requirements.txt`):
    ```bash
    pip install huggingface_hub[cli]
    ```
2.  **Login:**
    ```bash
    huggingface-cli login
    ```
    You will be prompted for a token, which you can generate from your Hugging Face account settings: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

# Introduction


## Running the benchmark
The following command line will allow you to run the tokenizer benchmark against multiple different models

```bash
python benchmark.py --file dataset.json --models mistralai/Mistral-7B-v0.1 gpt-4 google/gemma-7b
```

## visualizer

```bash
python visualizer.py --file ./samples/Programming/BASIC/guess.bas --model google/gemma-7b
```

or

```bash
python visualizer2.py --file ./samples/Programming/BASIC/guess.bas --models mistralai/Mistral-7B-v0.1 gpt-4 google/gemma-7b
```

```bash
python visualizer2.py --file ./samples/Text/cities.txt --models mistralai/Mistral-7B-v0.1 gpt-4 google/gemma-7b --ignore-numbers
```