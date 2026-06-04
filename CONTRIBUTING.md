# Contributing to OpenLib

Thank you for helping make knowledge more accessible.

Whether you are translating an entire book, fixing a typo, or improving existing content, your contribution is welcome.

---

# Ways to Contribute

You can help by:

- Adding a new book translation
- Improving an existing translation
- Fixing spelling or formatting issues
- Reporting bugs
- Suggesting improvements

No programming experience is required.

---

# Adding a New Book

## 1. Create a Book Folder

Inside:

```text
content/books/
```

create a new folder:

```text
content/books/my-book/
```

The folder name will become part of the URL.

---

## 2. Create metadata.json

Example:

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "language": "en",
  "translator": "Your Name",
  "lang": "fa",
  "dir": "rtl",
  "chapters": [
    {
      "id": "01",
      "title": "Chapter 1"
    },
    {
      "id": "02",
      "title": "Chapter 2"
    }
  ]
}
```

### Field Reference

| Field      | Description            |
| ---------- | ---------------------- |
| title      | Book title             |
| author     | Original author        |
| language   | Original book language |
| translator | Translator name        |
| lang       | Translation language   |
| dir        | `ltr` or `rtl`         |
| chapters   | List of chapter files  |

Example:

```json
"language": "en",
"lang": "fa"
```

means:

- Original book language: English
- Translation language: Persian

---

## 3. Create Chapter Files

Create:

```text
content/books/my-book/chapters/
```

Add one Markdown file per chapter:

```text
01.md
02.md
03.md
...
```

Each filename must match the corresponding chapter `id`.

Example:

```json
{
  "id": "01",
  "title": "Introduction"
}
```

becomes:

```text
01.md
```

---

## 4. Preview Locally

Install dependency:

```bash
pip install markdown
```

Build the site:

```bash
python build.py
```

Run local server:

```bash
python server.py
```

Open:

```text
http://localhost:8000
```

Your book should appear automatically.

---

## 5. Submit Your Changes

```bash
git add .
git commit -m "Add translation of Book Title"
git push
```

Then open a Pull Request.

---

# Improving Existing Translations

1. Locate the chapter file.
2. Edit the Markdown content.
3. Preview locally if necessary.
4. Submit a Pull Request.

Small typo fixes are also welcome.

---

# Project Structure

```text
OPENLIB/
├── content/books/
│   └── book-name/
│       ├── metadata.json
│       └── chapters/
│           ├── 01.md
│           └── 02.md
├── templates/
├── static/
├── docs/
├── build.py
├── server.py
└── CONTRIBUTING.md
```

---

# Need Help?

- Open a GitHub Issue
- Use the Feedback form on the website

Thank you for contributing to OpenLib.
