"""Compile the archive, split source sections and render portable PDF previews.

Requirements: Tectonic 0.17.0, pypdf 6.7.5 and Poppler pdftoppm.
The LaTeX source documents its font dependencies.
"""

import argparse
import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

from pypdf import PdfReader, PdfWriter

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tectonic", default="tectonic")
args = parser.parse_args()
archive = Path(__file__).resolve().parents[1] / "archive"
subprocess.run(
    [args.tectonic, "-o", str(archive / "pdfs"), str(archive / "latex/main.tex")],
    check=True,
)
compiled = archive / "pdfs/main.pdf"
combined = archive / "pdfs/britannica-100-pages.pdf"
compiled.replace(combined)
reader = PdfReader(combined)
if len(reader.outline) != 100:
    raise RuntimeError("Expected exactly 100 source sections")
records = []
for index, destination in enumerate(reader.outline):
    row = int(destination["/Title"].split()[-1])
    start = reader.get_destination_page_number(destination)
    end = (
        reader.get_destination_page_number(reader.outline[index + 1])
        if index + 1 < len(reader.outline)
        else len(reader.pages)
    )
    writer = PdfWriter()
    for number in range(start, end):
        writer.add_page(reader.pages[number])
    path = archive / f"pdfs/page-{row}.pdf"
    with path.open("wb") as output:
        writer.write(output)
    records.append(
        {
            "row_index": row,
            "pdf": str(path.relative_to(archive)),
            "compiled_pages": end - start,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    )

(archive / "previews").mkdir(exist_ok=True)


def preview(record):
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            "1",
            "-singlefile",
            "-scale-to",
            "1300",
            "-jpeg",
            "-jpegopt",
            "quality=85",
            str(archive / record["pdf"]),
            str(archive / f"previews/page-{record['row_index']}"),
        ],
        check=True,
    )


with ThreadPoolExecutor(max_workers=4) as executor:
    list(executor.map(preview, records))
(archive / "assets/compile-receipt.json").write_text(
    json.dumps(
        {
            "compiler": "Tectonic 0.17.0",
            "compiled_at": datetime.now(UTC).isoformat(),
            "source_pages": 100,
            "compiled_pages": len(reader.pages),
            "pages": records,
        },
        indent=2,
    )
    + "\n"
)
print(f"Compiled {len(records)} source pages into {len(reader.pages)} PDF pages")
