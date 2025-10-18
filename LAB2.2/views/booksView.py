# views/booksView.py
from services.booksService import BookService
from enums.enums import (
    BookStatus, BookType,
    BookNovelType, TextBookType, ScienceType, EducationLevel
)
from auth import current_user


def books_menu(db, current_user):
    svc = BookService(db)

    while True:
        print("\n=== BOOK MANAGEMENT MENU ===")

        if not current_user["role"]:
            print("1. View All Books")
            print("2. Search Books")
            print("0. Back to Main Menu")
            choice = input("Select: ").strip()

            if choice == "1":
                view_books(db)
            elif choice == "2":
                search_books_view(svc)
            elif choice == "0":
                break
            else:
                print("Invalid choice, please try again.")
        else:
            print("1. Add Book")
            print("2. Delete Book")
            print("3. Update Book")
            print("4. Search Book")
            print("5. List All Books")
            print("0. Back")

            choice = input("Select: ").strip()

            if choice == "1":
                add_book_view(svc)
            elif choice == "2":
                delete_book_view(svc)
            elif choice == "3":
                update_book_view(svc)
            elif choice == "4":
                search_books_view(svc)
            elif choice == "5":
                list_books_view(svc)
            elif choice == "0":
                break
            else:
                print("Invalid choice, please try again.")


def add_book_view(svc: BookService):
    print("\n=== ADD NEW BOOK ===")
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    pages = input("Pages: ").strip()
    publish_year = input("Publish Year: ").strip()

    # BookType selection (numbered)
    print("\nBook Type Options:")
    book_types = list(BookType)
    for idx, b in enumerate(book_types, start=1):
        print(f"{idx}. {b.value}")
    type_choice = input("Select Book Type (number): ").strip()
    try:
        book_type = book_types[int(type_choice) - 1]
    except Exception:
        print("[ERROR] Invalid choice, defaulting to 'novel'.")
        book_type = BookType.NOVEL

    genre = None
    subject = None
    level = None
    field = None

    # Sub-enum selection based on type
    if book_type == BookType.NOVEL:
        print("\n=== NOVEL GENRES ===")
        novel_types = list(BookNovelType)
        for i, nt in enumerate(novel_types, 1):
            print(f"{i}. {nt.value}")
        choice = input("Select Novel Genre (number, Enter to skip): ").strip()
        try:
            genre = novel_types[int(choice) - 1].value
        except Exception:
            genre = None

    elif book_type == BookType.TEXTBOOK:
        print("\n=== TEXTBOOK SUBJECTS ===")
        subjects = list(TextBookType)
        for i, sb in enumerate(subjects, 1):
            print(f"{i}. {sb.value}")
        choice = input("Select Subject (number, Enter to skip): ").strip()
        try:
            subject = subjects[int(choice) - 1].value
        except Exception:
            subject = None

        print("\n=== EDUCATION LEVEL ===")
        levels = list(EducationLevel)
        for i, lv in enumerate(levels, 1):
            print(f"{i}. {lv.value}")
        choice = input("Select Level (number, Enter to skip): ").strip()
        try:
            level = levels[int(choice) - 1].value
        except Exception:
            level = None

    elif book_type == BookType.SCIENCE:
        print("\n=== SCIENCE FIELDS ===")
        fields = list(ScienceType)
        for i, f in enumerate(fields, 1):
            print(f"{i}. {f.value}")
        choice = input("Select Field (number, Enter to skip): ").strip()
        try:
            field = fields[int(choice) - 1].value
        except Exception:
            field = None

    # Status selection (numbered)
    print("\nBook Status Options:")
    statuses = list(BookStatus)
    for i, s in enumerate(statuses, 1):
        print(f"{i}. {s.name}")
    status_choice = input("Select Status (number): ").strip()
    try:
        status = statuses[int(status_choice) - 1]
    except Exception:
        print("[WARNING] Invalid status, defaulting to AVAILABLE.")
        status = BookStatus.AVAILABLE

    data = {
        "title": title,
        "author": author,
        "pages": pages,
        "publish_year": publish_year,
        "book_type": book_type,   # pass enum (BookService handles)
        "status": status,         # pass enum
        "genre": genre,
        "subject": subject,
        "level": level,
        "field": field
    }

    svc.add_book(data)


def delete_book_view(svc: BookService):
    print("\n=== DELETE BOOK ===")
    book_id = input("Enter Book ID to delete: ").strip()
    svc.delete_book(book_id)


def update_book_view(svc: BookService):
    print("\n=== UPDATE BOOK ===")
    book_id = input("Enter Book ID to update: ").strip()

    data = {}
    for field in ["title", "author", "pages", "publish_year", "genre", "subject", "level", "field", "book_type"]:
        val = input(f"New {field.capitalize()} (press Enter to skip): ").strip()
        if val:
            data[field] = val

    status_input = input("New Status (AVAILABLE/BORROWED/OTHER, press Enter to skip): ").strip().upper()
    if status_input:
        try:
            data["status"] = BookStatus[status_input]
        except KeyError:
            print("[WARNING] Invalid status, keeping old value.")

    svc.update_book(book_id, data)


def search_books_view(svc: BookService):
    print("\n=== SEARCH BOOK ===")
    filters = {}
    book_id = input("Book_id (press Enter to skip): ").strip()
    if book_id:
        filters["book_id"] = book_id

    title = input("Title (press Enter to skip): ").strip()
    if title:
        filters["title"] = title

    author = input("Author (press Enter to skip): ").strip()
    if author:
        filters["author"] = author

    book_type = input("Book_type (press Enter to skip): ").strip()
    if book_type:
        filters["book_type"] = book_type

    status = input("Status (number or press Enter to skip): ").strip()
    if status:
        # allow number -> map to enum value
        try:
            s_idx = int(status)
            statuses = list(BookStatus)
            status_enum = statuses[s_idx - 1]
            filters["status"] = status_enum.value
        except Exception:
            # maybe user typed name or int as string
            try:
                filters["status"] = int(status)
            except Exception:
                filters["status"] = status

    results = svc.search_books(filters)

    if not results:
        print("[INFO] No books found with given filters.")
        return

    # print header
    print("\n{:<5} {:<25} {:<20} {:<10} {:<12} {:<10} {:<12}".format(
        "ID", "Title", "Author", "Pages", "Year", "Type", "Status"
    ))
    print("-" * 100)

    for r in results:
        # r may be dict or tuple
        if isinstance(r, dict):
            bid = r.get("book_id")
            title = r.get("title")
            author = r.get("author")
            pages = r.get("pages")
            year = r.get("publish_year")
            btype = r.get("book_type")
            status = r.get("status")
        else:
            bid, title, author, pages, year, status, btype = r[:7]

        print("{:<5} {:<25} {:<20} {:<10} {:<12} {:<10} {:<12}".format(
            str(bid), str(title), str(author), str(pages), str(year), str(btype), str(status)
        ))


def list_books_view(svc: BookService):
    print("\n=== ALL BOOKS ===")
    rows = svc.get_all_books()
    if not rows:
        print("[INFO] No books found.")
        return

    print("\n{:<5} {:<20} {:<15} {:<8} {:<8} {:<10} {:<12} {:<15} {:<15} {:<15}".format(
        "ID", "Title", "Author", "Pages", "Year", "Type", "Genre/Subj", "Level", "Field", "Status"
    ))
    print("-" * 130)

    for r in rows:
        print("{:<5} {:<20} {:<15} {:<8} {:<8} {:<10} {:<12} {:<15} {:<15} {:<15}".format(
            str(r.get("book_id")),
            str(r.get("title")),
            str(r.get("author")),
            str(r.get("pages")),
            str(r.get("publish_year")),
            str(r.get("book_type")),
            str(r.get("genre") or r.get("subject") or "-"),
            str(r.get("level") or "-"),
            str(r.get("field") or "-"),
            str(r.get("status"))
        ))


def view_books(db):
    try:
        svc = BookService(db)
        rows = svc.get_all_books()

        if not rows:
            print("📭 No books found in the library.")
            return

        print("\n=== 📚 LIST OF BOOKS ===")
        print("{:<10} {:<30} {:<20} {:<15}".format("Book ID", "Title", "Author", "Status"))
        print("-" * 75)
        for book in rows:
            print("{:<10} {:<30} {:<20} {:<15}".format(
                book.get("book_id"), book.get("title"), book.get("author"), str(book.get("status"))
            ))
    except Exception as e:
        print(f"[VIEW ERROR] Failed to display books: {e}")
