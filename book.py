import json
from pathlib import Path

class Chapter:
    """
    Represents one chapter of a book.
    """
    def __init__(self, id: str, title: str, content_file: Path):
        self.id = id
        self.title = title
        self.content_file = content_file
    
    def __repr__(self):
        return f"chapter({self.id}, {self.title})"
    
class Book:
    """
    Represents a whole book with its metadata and list of chapters.
    """
    def __init__(self, book_folder: Path):
        self.folder = book_folder
        #Load metadata.json
        meta_path = book_folder / "metadata.json"
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.title = meta["title"]
        self.author = meta.get("author", "Unknown")
        self.language = meta.get("language", "en")
        self.translator = meta.get("translator", "")

        #Build chapter objects from the list in JSON
        self.chapters = []
        for ch_data in meta.get("chapters", []):
            ch_id = ch_data["id"]
            ch_title = ch_data["title"]
            #The corresponding markdown file
            md_file = book_folder / "chapters" / f"{ch_id}.md"
            chapter = Chapter(ch_id, ch_title, md_file)
            self.chapters.append(chapter)
        
    def __repr__(self):
        return f"Book({self.title}, {len(self.chapters)} chapters)"