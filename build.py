from pathlib import Path
from book import Book
from generator import SiteGenerator

# Define paths
ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"

# Load the book 
book_folder = CONTENT_DIR / "books" / "after-dark"
book = Book(book_folder)
print (book)

# Create generator and build homepage
gen = SiteGenerator(ROOT)
gen.generate_homepage(book)
gen.generate_chapter_pages(book)