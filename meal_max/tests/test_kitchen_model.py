import pytest
import sqlite3
from meal_max.models.kitchen_model import Meal, create_meal
from meal_max.utils.sql_utils import get_db_connection


@pytest.fixture()
def meal_instance():
    """Fixture to provide a new instance of Meal for each test."""
    return Meal(id=1, meal='Pasta', cuisine='Italian', price=10.0, difficulty='MED')

@pytest.fixture
def sample_meal1():
    return Meal(id=1, meal='Pasta', cuisine='Italian', price=10.0, difficulty='MED')

@pytest.fixture
def sample_meal2():
    return Meal(id=2, meal='Sushi', cuisine='Japanese', price=15.0, difficulty='HIGH')


##################################################
# Meal Creation Test Cases
##################################################

def test_create_meal_valid():
    """Test creating a meal with valid data."""
    try:
        create_meal('Burger', 'American', 8.0, 'LOW')
    except Exception:
        pytest.fail("create_meal raised an Exception unexpectedly on valid input.")

def test_create_meal_invalid_price():
    """Test creating a meal with an invalid (negative) price."""
    with pytest.raises(ValueError, match="Price must be a positive value."):
        Meal(id=1, meal='Salad', cuisine='Mediterranean', price=-5.0, difficulty='LOW')

def test_create_meal_invalid_difficulty():
    """Test creating a meal with an invalid difficulty level."""
    with pytest.raises(ValueError, match="Difficulty must be 'LOW', 'MED', or 'HIGH'."):
        Meal(id=2, meal='Ramen', cuisine='Japanese', price=12.0, difficulty='EASY')


##################################################
# Database Insertion Test Cases
##################################################

def test_add_duplicate_meal_to_database():
    """Test adding a duplicate meal entry to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meals (meal, cuisine, price, difficulty) VALUES (?, ?, ?, ?)",
                       ('Pizza', 'Italian', 10.0, 'MED'))
        conn.commit()

    with pytest.raises(sqlite3.IntegrityError):
        create_meal('Pizza', 'Italian', 10.0, 'MED')


##################################################
# Retrieval and Utility Function Test Cases
##################################################

def test_retrieve_meal_by_id(meal_instance):
    """Test retrieving a meal by its ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meals (id, meal, cuisine, price, difficulty) VALUES (?, ?, ?, ?, ?)",
                       (meal_instance.id, meal_instance.meal, meal_instance.cuisine, meal_instance.price, meal_instance.difficulty))
        conn.commit()

        cursor.execute("SELECT * FROM meals WHERE id=?", (meal_instance.id,))
        row = cursor.fetchone()

    assert row is not None
    assert row[1] == 'Pasta'
    assert row[2] == 'Italian'
    assert row[3] == 10.0
    assert row[4] == 'MED'

def test_get_all_meals():
    """Test retrieving all meals from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meals (meal, cuisine, price, difficulty) VALUES (?, ?, ?, ?)", ('Burger', 'American', 8.0, 'LOW'))
        cursor.execute("INSERT INTO meals (meal, cuisine, price, difficulty) VALUES (?, ?, ?, ?)", ('Tacos', 'Mexican', 5.5, 'LOW'))
        conn.commit()

        cursor.execute("SELECT * FROM meals")
        rows = cursor.fetchall()

    assert len(rows) == 2
    assert rows[0][1] == 'Burger'
    assert rows[1][1] == 'Tacos'


##################################################
# Validation and Constraint Test Cases
##################################################

def test_price_constraint_negative():
    """Test that a negative price raises a ValueError."""
    with pytest.raises(ValueError, match="Price must be a positive value."):
        Meal(id=3, meal='Soup', cuisine='French', price=-3.0, difficulty='LOW')

def test_invalid_difficulty_level():
    """Test that an invalid difficulty level raises a ValueError."""
    with pytest.raises(ValueError, match="Difficulty must be 'LOW', 'MED', or 'HIGH'."):
        Meal(id=4, meal='Curry', cuisine='Indian', price=12.0, difficulty='EASY')


##################################################
# Cleanup Test Cases
##################################################

def test_delete_meal_from_database(sample_meal1):
    """Test deleting a meal entry from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meals (id, meal, cuisine, price, difficulty) VALUES (?, ?, ?, ?, ?)",
                       (sample_meal1.id, sample_meal1.meal, sample_meal1.cuisine, sample_meal1.price, sample_meal1.difficulty))
        conn.commit()

        cursor.execute("DELETE FROM meals WHERE id=?", (sample_meal1.id,))
        conn.commit()

        cursor.execute("SELECT * FROM meals WHERE id=?", (sample_meal1.id,))
        row = cursor.fetchone()

    assert row is None, "Expected meal to be deleted from the database"


##################################################
# Edge Case Test Cases
##################################################

def test_retrieve_nonexistent_meal():
    """Test retrieving a meal that does not exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meals WHERE id=?", (999,))
        row = cursor.fetchone()

    assert row is None, "Expected no meal to be found with a nonexistent ID"
