import pytest
from lab8.src.library_manager import Book,LibraryManager

@pytest.fixture
def sample_book1():
    return Book(1,"Hobbit","J.R.R Tolkien", 1937, "Fantasy")

@pytest.fixture
def sample_book2():
    return  Book(6, "Dune", "Frank Herbert", 1965, "Science Fiction")

@pytest.fixture
def sample_book3():
    return  Book(11, "Dune part 3", "Frank Herbert", 1965, "Science Fiction")
@pytest.fixture
def empty_library_manager():
    return LibraryManager()

@pytest.fixture
def filled_library_manager(empty_library_manager,sample_book1,sample_book2):
    empty_library_manager.add_book(sample_book1)
    empty_library_manager.add_book(sample_book2)
    return empty_library_manager


def test_adding_books(empty_library_manager,sample_book1,sample_book2):

    assert len(empty_library_manager.books) == 0

    empty_library_manager.add_book(sample_book1)
    empty_library_manager.add_book(sample_book2)

    assert len(empty_library_manager.books) == 2
    assert sample_book1.book_id in empty_library_manager.books
    assert sample_book2.book_id in empty_library_manager.books

def test_adding_invalid_books(empty_library_manager):

    with pytest.raises(TypeError):
        empty_library_manager.add_book("book")

def test_adding_book_that_already_exists(filled_library_manager,sample_book1):

    result = filled_library_manager.add_book(sample_book1)

    assert result == False

def test_getting_book(filled_library_manager,sample_book1,sample_book2):

    result = filled_library_manager.get_book(sample_book1.book_id)
    assert result == sample_book1

    result = filled_library_manager.get_book(sample_book2.book_id)
    assert result == sample_book2

def test_getting_non_existent_book(filled_library_manager):

    result = filled_library_manager.get_book(99)
    assert result is None


def test_remove_book(filled_library_manager,sample_book1,sample_book2):

    assert len(filled_library_manager.books) == 2

    filled_library_manager.remove_book(sample_book1.book_id)
    assert len(filled_library_manager.books) == 1
    assert sample_book1.book_id not in filled_library_manager.books

    filled_library_manager.remove_book(sample_book2.book_id)
    assert len(filled_library_manager.books) == 0
    assert sample_book2.book_id not in filled_library_manager.books

def test_removing_non_existing_book(filled_library_manager):

    result = filled_library_manager.remove_book(99)
    assert result == False

def test_removing_borrowed_book(filled_library_manager,sample_book1):

    filled_library_manager.borrow_book(sample_book1.book_id,1)

    with pytest.raises(ValueError):
        filled_library_manager.remove_book(sample_book1.book_id)

def test_borrow_book(filled_library_manager,sample_book1,sample_book2):

    borrower_id  = 1
    filled_library_manager.borrow_book(sample_book1.book_id,borrower_id)

    assert sample_book1.is_borrowed == True
    assert sample_book2.is_borrowed == False
    assert sample_book1.borrow_count == 1
    assert sample_book2.borrow_count == 0
    assert borrower_id in filled_library_manager.borrowed_books
    assert sample_book1.book_id in filled_library_manager.borrowed_books[borrower_id]

    filled_library_manager.borrow_book(sample_book2.book_id,borrower_id)
    assert sample_book2.is_borrowed == True
    assert sample_book2.borrow_count == 1
    assert borrower_id in filled_library_manager.books
    assert len(filled_library_manager.borrowed_books[borrower_id]) == 2

    filled_library_manager.return_book(sample_book1.book_id,borrower_id)
    assert sample_book1.is_borrowed == False
    filled_library_manager.borrow_book(sample_book1.book_id,borrower_id)
    assert sample_book1.borrow_count == 2

def test_borrowing_non_existing_book(filled_library_manager):
    with pytest.raises(ValueError):
        filled_library_manager.borrow_book(99,2)

def test_borrowing_borrowed_book(filled_library_manager,sample_book1):

    filled_library_manager.borrow_book(sample_book1.book_id,1)
    result = filled_library_manager.borrow_book(sample_book1.book_id,2)

    assert result == False

def test_returning_book(filled_library_manager,sample_book1,sample_book2):

    borrower_id = 1
    filled_library_manager.borrow_book(sample_book1.book_id,borrower_id)
    filled_library_manager.borrow_book(sample_book2.book_id,borrower_id)
    assert sample_book1.is_borrowed == True
    assert sample_book2.is_borrowed == True
    assert len(filled_library_manager.borrowed_books[borrower_id]) == 2
    filled_library_manager.return_book(sample_book1.book_id,1)
    assert sample_book1.book_id not in filled_library_manager.borrowed_books[borrower_id]
    assert sample_book1.is_borrowed == False
    assert len(filled_library_manager.borrowed_books[borrower_id]) == 1
    filled_library_manager.return_book(sample_book2.book_id,borrower_id)
    assert sample_book2.is_borrowed == False
    assert borrower_id not in filled_library_manager.borrowed_books

def test_returning_non_existing_book(filled_library_manager):

    with pytest.raises(ValueError):
        filled_library_manager.return_book(99,2)

def test_returning_book_negative(filled_library_manager,sample_book1,sample_book2):
    borrower_id = 1
    borrower_id2 = 2

    filled_library_manager.borrow_book(sample_book1.book_id,borrower_id)

    with pytest.raises(ValueError):
        filled_library_manager.return_book(sample_book2.book_id,borrower_id)

    with pytest.raises(ValueError):
        filled_library_manager.return_book(sample_book1.book_id,borrower_id2)

def test_searching_books(filled_library_manager,sample_book1,sample_book2):

    criteria1  = {
        'title': sample_book1.title,
        'author': sample_book1.author,
        'year_from':1930,
        'year_to': 1970,
        'genre': sample_book1.genre,
    }

    criteria2 = {
        'year_from': 1900
    }

    result = filled_library_manager.search_books(criteria1)
    assert result[0] == sample_book1

    result = filled_library_manager.search_books({})
    assert len(result) == 2

    result = filled_library_manager.search_books(criteria2)
    assert len(result) == 2
    assert sample_book1 in result
    assert sample_book2 in result

def test_search_available_only(filled_library_manager,sample_book1,sample_book2):

    criteria1 = {
        'available_only': True,
    }

    result = filled_library_manager.search_books(criteria1)
    assert sample_book1 in result
    assert sample_book2 in result
    assert len(result) == 2

    borrower_id = 1
    filled_library_manager.borrow_book(sample_book1.book_id,borrower_id)
    result = filled_library_manager.search_books(criteria1)
    assert len(result) == 1
    assert result[0] == sample_book2
    assert sample_book1 not in result



def test_get_statistics(filled_library_manager,sample_book1,sample_book2,sample_book3):

    result = filled_library_manager.get_statistics()
    assert result['total_books'] == 2
    assert result['available_books'] == 2
    assert result['borrowed_books'] == 0
    assert result['genres'] == {"Fantasy":1,"Science Fiction":1}
    assert result['popular_books'] == [sample_book1,sample_book2]

    borrower_id = 1
    filled_library_manager.borrow_book(sample_book1.book_id,borrower_id)
    filled_library_manager.add_book(sample_book3)

    result = filled_library_manager.get_statistics()
    assert result['total_books'] == 3
    assert result['available_books'] == 2
    assert result['borrowed_books'] == 1
    assert result['genres'] == {"Fantasy":1,"Science Fiction":2}
    assert result['popular_books'] == [sample_book1,sample_book2,sample_book3]




