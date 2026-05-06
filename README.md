# Multithreaded File Scanner

## Overview
Multithreaded File Scanner is a Python command-line tool that recursively scans directories for files matching a keyword or extension. It uses multiple worker threads to process files concurrently and produces a summary report of matches.

## Purpose
The purpose of this project is to demonstrate concurrency, filesystem traversal, and practical command-line tool design. This project is useful for searching large folders, source code directories, or document collections more efficiently than a simple single-file script.

## Technologies Used
- Python 3
- `threading`
- `queue`
- `pathlib`
- Command-line arguments with `argparse`

## Key Features
- Recursively scans a target directory
- Searches filenames and file contents
- Uses worker threads for concurrent processing
- Optional file extension filtering
- Tracks total files scanned
- Reports matched files
- Handles unreadable files safely
- Supports case-insensitive search

## Project Structure
```txt
multithreaded-file-scanner/
├── scanner.py
├── README.md
└── sample_files/
```

## How to Run
```bash
python scanner.py --path . --keyword error
```

## Optional Arguments
```bash
python scanner.py --path . --keyword main --threads 8
python scanner.py --path . --keyword TODO --extension .py
python scanner.py --path . --keyword config --names-only
```

## Example Output
```txt
Multithreaded File Scanner
Target path: .
Keyword: error
Threads: 4

Matches:
- ./src/logger.py
- ./notes/debugging.txt

Summary:
Files scanned: 42
Matches found: 2
```

## My Contribution
I designed and implemented the scanning workflow, including directory traversal, task queue creation, worker thread coordination, file content searching, and summary reporting. I also added command-line options so the tool can be reused in different contexts.

## Challenges and Lessons Learned
The biggest challenge was safely coordinating multiple threads while avoiding duplicate work. This project helped me better understand thread-safe queues, filesystem operations, and how to structure command-line tools with useful options.

## Future Improvements
- Add CSV or JSON report output
- Add regex search support
- Add file size filters
- Add progress bar for large scans
