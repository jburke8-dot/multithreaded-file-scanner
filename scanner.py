from __future__ import annotations

import argparse
import queue
import threading
from pathlib import Path
from typing import List


class ScanStats:
    def __init__(self) -> None:
        self.files_scanned = 0
        self.matches: List[Path] = []
        self.lock = threading.Lock()

    def record_scan(self) -> None:
        with self.lock:
            self.files_scanned += 1

    def record_match(self, path: Path) -> None:
        with self.lock:
            self.matches.append(path)


def file_contains_keyword(path: Path, keyword: str) -> bool:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                if keyword in line.lower():
                    return True
    except OSError:
        return False

    return False


def worker(
    tasks: "queue.Queue[Path]",
    keyword: str,
    stats: ScanStats,
    names_only: bool,
) -> None:
    while True:
        try:
            path = tasks.get_nowait()
        except queue.Empty:
            return

        stats.record_scan()

        filename_match = keyword in path.name.lower()
        content_match = False if names_only else file_contains_keyword(path, keyword)

        if filename_match or content_match:
            stats.record_match(path)

        tasks.task_done()


def build_task_queue(root: Path, extension: str | None) -> "queue.Queue[Path]":
    tasks: "queue.Queue[Path]" = queue.Queue()

    for path in root.rglob("*"):
        if path.is_file():
            if extension is None or path.suffix == extension:
                tasks.put(path)

    return tasks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multithreaded file scanner")
    parser.add_argument("--path", required=True, help="Directory to scan")
    parser.add_argument("--keyword", required=True, help="Keyword to search for")
    parser.add_argument("--threads", type=int, default=4, help="Number of worker threads")
    parser.add_argument("--extension", help="Optional file extension filter, such as .py")
    parser.add_argument(
        "--names-only",
        action="store_true",
        help="Only search filenames, not file contents",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    root = Path(args.path)
    if not root.exists() or not root.is_dir():
        raise SystemExit("Error: --path must be an existing directory")

    keyword = args.keyword.lower()
    tasks = build_task_queue(root, args.extension)
    stats = ScanStats()

    threads = []
    for _ in range(max(1, args.threads)):
        thread = threading.Thread(
            target=worker,
            args=(tasks, keyword, stats, args.names_only),
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Multithreaded File Scanner")
    print(f"Target path: {root}")
    print(f"Keyword: {args.keyword}")
    print(f"Threads: {max(1, args.threads)}")
    print("\nMatches:")

    if stats.matches:
        for match in sorted(stats.matches):
            print(f"- {match}")
    else:
        print("No matches found.")

    print("\nSummary:")
    print(f"Files scanned: {stats.files_scanned}")
    print(f"Matches found: {len(stats.matches)}")


if __name__ == "__main__":
    main()
