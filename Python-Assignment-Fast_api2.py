#  Building a RESTful API for a book review system with specific endpoints and functionalities.
# Pydantic models to represent the data structures for books and reviews.
# models.py
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    book_id: int
    text: str
    rating: int

    # Built FastAPI app and define the endpoints as per the requirements

    # main.py
from fastapi import FastAPI, HTTPException
from typing import List
from models import Book, Review

app = FastAPI()

books_db = []
reviews_db = []

@app.post("/books/")
def add_book(book: Book):
    books_db.append(book)
    return {"message": "Book added successfully"}

@app.post("/reviews/")
def add_review(review: Review):
    # Check if the book exists
    if review.book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    
    reviews_db.append(review)
    return {"message": "Review added successfully"}

@app.get("/books/")
def get_books(author: str = None, publication_year: int = None):
    if author:
        return [book for book in books_db if book.author == author]
    elif publication_year:
        return [book for book in books_db if book.publication_year == publication_year]
    else:
        return books_db

@app.get("/reviews/{book_id}")
def get_reviews(book_id: int):
    return [review for review in reviews_db if review.book_id == book_id]

# Integration with database
import sqlite3
from fastapi import FastAPI

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect('book_reviews.db')
cursor = conn.cursor()

# Define database schema
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publication_year INTEGER
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY,
                    book_id INTEGER,
                    review TEXT,
                    rating INTEGER,
                    FOREIGN KEY(book_id) REFERENCES books(id)
                )''')
conn.commit()

# Define CRUD operations
def add_book(title, author, publication_year):
    cursor.execute("INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)", (title, author, publication_year))
    conn.commit()
    return cursor.lastrowid

def get_books(author=None, publication_year=None):
    query = "SELECT * FROM books"
    if author:
        query += f" WHERE author = '{author}'"
    if publication_year:
        if author:
            query += " AND"
        else:
            query += " WHERE"
        query += f" publication_year = {publication_year}"
    cursor.execute(query)
    return cursor.fetchall()

# API endpoints
@app.post("/books/")
def create_book(title: str, author: str, publication_year: int):
    book_id = add_book(title, author, publication_year)
    return {"message": "Book added successfully", "book_id": book_id}

@app.get("/books/")
def read_books(author: str = None, publication_year: int = None):
    books = get_books(author, publication_year)
    return {"books": books}

# Advanced features and Testing
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Simulated email sender function
async def send_confirmation_email(email: str, message: str):
    # Simulating email sending process
    await asyncio.sleep(3)
    print(f"Confirmation email sent to {email}: {message}")

# Background task to send confirmation email
def background_send_email(email: str, message: str):
    asyncio.create_task(send_confirmation_email(email, message))

# API models
class Review(BaseModel):
    email: str
    message: str

# API endpoint to submit review
@app.post("/submit_review/")
async def submit_review(review: Review, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_send_email, review.email, review.message)
    return {"message": "Review submitted successfully. Confirmation email will be sent shortly."}

# Test endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Employee Review System!"}

# Test client
from fastapi.testclient import TestClient

client = TestClient(app)

# Test cases for API endpoints
def test_submit_review():
    review_data = {"email": "test@example.com", "message": "This is a test review."}
    response = client.post("/submit_review/", json=review_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Review submitted successfully. Confirmation email will be sent shortly."}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Employee Review System!"}

