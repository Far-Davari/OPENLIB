from pathlib import Path
from book import Book
from generator import SiteGenerator
import shutil

# Define paths
ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content" / "books"

gen = SiteGenerator(ROOT)

books = []
for folder in sorted(CONTENT_DIR.iterdir()):
    if folder.is_dir() and (folder / "metadata.json").exists():
        book = Book(folder)
        books.append(book)
        print(f"Found: {book}")

if not books:
    print("No books found in content/books/")
    exit(1)

gen.generate_global_homepage(books)

for book in books:
    gen.generate_book_pages(book)

gen.generate_search_index(books)

static_src = ROOT / "static"
static_dest = ROOT / "docs" / "static"
if static_dest.exists():
    shutil.rmtree(static_dest)
shutil.copytree(static_src, static_dest)
print("Copied static files to docs/")

print("All books generated.")
