import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
import os

# Custom CSS with improved text visibility and contrast
st.markdown("""
<style>
   /* Main styling */
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white !important;
}

/* Card styling */
.book-card {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    backdrop-filter: blur(5px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.book-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
}

/* Button styling */
.stButton button {
    background: linear-gradient(45deg, #FF512F, #DD2476);
    color: white !important;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    transition: all 0.3s ease;
    font-weight: 600;
}

.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* Sidebar styling */
.css-1d391kg {
    background: rgba(0, 0, 0, 0.3);
}

/* Input field text color - more direct selectors with !important */
div.stTextInput > div > div > input, 
div.stNumberInput > div > div > input {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

/* Input field placeholder color - fixed with direct selectors */
div.stTextInput > div > div > input::placeholder, 
div.stNumberInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.8) !important;
    opacity: 1 !important;
}

/* Dropdown styling - enhanced selectors for better control */
div.stSelectbox > div > div > div {
    background-color: rgba(255, 255, 255, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

/* Dropdown text color for both selected and options */
div.stSelectbox label {
    color: #ffffff !important;
}

div.stSelectbox > div > div > div[data-baseweb="select"] > div,
div.stSelectbox > div > div > div[data-baseweb="select"] span,
div.stSelectbox > div > div > div > div,
div.stSelectbox > div > div > div[data-baseweb="select"] {
    color: #000000 !important;
    font-weight: 500 !important;
}

/* Selected option color */
[data-baseweb="select"] [data-testid="stMarkdownContainer"] p {
    color: #000000 !important;
}

/* Dropdown menu items text color */
div[data-baseweb="menu"] div,
div[data-baseweb="menu"] span,
div[data-baseweb="menu"] p,
div[data-baseweb="popover"] div,
div[data-baseweb="popover"] span,
div[data-baseweb="popover"] p,
div[data-baseweb="select-option"] div {
    color: #000000 !important;
}

/* Dropdown options hover state */
div[data-baseweb="menu"] div:hover,
div[data-baseweb="select-option"]:hover {
    background-color: rgba(0, 0, 0, 0.1) !important;
}

/* Force all selectbox text to be black */
.stSelectbox * {
    color: #000000 !important;
}

/* Exception for the label */
.stSelectbox label {
    color: #ffffff !important;
}

/* Statistics page improvements */
.stat-card {
    background: rgba(255, 255, 255, 0.25) !important;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    backdrop-filter: blur(5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.stat-title {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    margin-bottom: 12px;
    color: #ffffff !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
}

.stat-value {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    margin-bottom: 5px;
    background: linear-gradient(45deg, #FF512F, #DD2476) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.3)) !important;
}

.stat-label {
    font-size: 1rem !important;
    color: rgba(255, 255, 255, 0.9) !important;
    font-weight: 500 !important;
}

/* Progress bar styling for statistics */
.progress-container {
    width: 100%;
    background-color: rgba(255, 255, 255, 0.25) !important;
    border-radius: 10px;
    margin: 10px 0;
    height: 15px;
    overflow: hidden;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3) !important;
}

.progress-bar {
    height: 15px;
    border-radius: 10px;
    background: linear-gradient(45deg, #FF512F, #DD2476) !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
}

/* Exit button styling */
.exit-button {
    background: linear-gradient(45deg, #FF512F, #DD2476);
    color: white !important;
    border: none;
    padding: 12px 24px;
    border-radius: 5px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 20px;
    font-weight: 600;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.exit-button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 18px rgba(0,0,0,0.3);
}

/* Make all text elements white */
p, div, span, h1, h2, h3, h4, h5, h6, li, label {
    color: #ffffff !important;
}

/* Form styling */
.stForm {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    backdrop-filter: blur(5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Checkbox styling */
.stCheckbox > label > div[role="checkbox"] {
    border-color: rgba(255, 255, 255, 0.6) !important;
}

.stCheckbox > label {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Extra fixes for dropdown text color */
[data-baseweb="select"] [data-testid="stMarkdownContainer"] {
    color: #000000 !important;
}

/* Selectbox arrow color */
[data-baseweb="icon"] svg {
    fill: #000000 !important;
}

/* Specifically targeting the selectbox text */
[data-baseweb="select"] [data-testid="stMarkdownContainer"] * {
    color: #000000 !important;
}

/* Ensure dropdown options are black */
[data-baseweb="select-option"] [data-testid="stMarkdownContainer"] * {
    color: #000000 !important;
}

/* Form dropdown text color */
form .stSelectbox [data-testid="stMarkdownContainer"] * {
    color: #000000 !important;
}

/* Edit form styling */
.edit-form {
    background: rgba(255, 255, 255, 0.15);
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

/* Action buttons container */
.action-buttons {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

/* Delete button specific styling */
.delete-btn {
    background: linear-gradient(45deg, #ff0000, #cc0000) !important;
}

/* Edit button specific styling */
.edit-btn {
    background: linear-gradient(45deg, #4CAF50, #2E7D32) !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  year INTEGER,
                  genre TEXT,
                  read INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# Database operations
def add_book(title, author, year, genre, read):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, year, genre, read) VALUES (?, ?, ?, ?, ?)",
              (title, author, year, genre, 1 if read else 0))
    conn.commit()
    conn.close()

def get_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT id, title, author, year, genre, read FROM books")
    books = c.fetchall()
    conn.close()
    return books

def get_book_by_id(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = c.fetchone()
    conn.close()
    return book

def update_book(book_id, title, author, year, genre, read):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("UPDATE books SET title=?, author=?, year=?, genre=?, read=? WHERE id=?",
              (title, author, year, genre, 1 if read else 0, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def search_books(search_term):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?",
              (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    books = c.fetchall()
    conn.close()
    return books

def get_library_stats():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Total books
    c.execute("SELECT COUNT(*) FROM books")
    total_books = c.fetchone()[0]
    
    # Read books
    c.execute("SELECT COUNT(*) FROM books WHERE read=1")
    read_books = c.fetchone()[0]
    
    # Genre distribution
    c.execute("SELECT genre, COUNT(*) FROM books GROUP BY genre")
    genre_counts = dict(c.fetchall())
    
    # Year range
    c.execute("SELECT MIN(year), MAX(year) FROM books")
    year_min, year_max = c.fetchone()
    
    conn.close()
    
    return {
        'total_books': total_books,
        'read_books': read_books,
        'genre_counts': genre_counts,
        'year_min': year_min or 0,
        'year_max': year_max or 0
    }

# Initialize session state for editing
if 'editing_book_id' not in st.session_state:
    st.session_state.editing_book_id = None

# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="Library Manager",
        options=["Add Book", "View Books", "Search", "Statistics", "Exit"],
        icons=["plus-circle-fill", "book-fill", "search", "bar-chart-fill", "box-arrow-right"],
        menu_icon="journal-richtext",
        default_index=0,
    )

# Main content
st.title("📚 Personal Library Manager")

def display_book(book, show_actions=True):
    try:
        # Safely unpack the book tuple
        if len(book) == 6:  # If using SQLite with all fields
            book_id, title, author, year, genre, read = book
        elif len(book) == 5:  # If somehow missing the ID
            title, author, year, genre, read = book
            book_id = None
        else:
            st.error(f"Unexpected book format: {book}")
            return
            
        st.markdown(f"""
        <div class="book-card">
            <h3>{title}</h3>
            <p>📝 Author: {author}</p>
            <p>📅 Year: {year}</p>
            <p>🏷️ Genre: {genre}</p>
            <p>📖 Status: {"Read ✅" if read else "Unread ❌"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if show_actions and book_id is not None:
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✏️ Edit", key=f"edit_{book_id}"):
                    st.session_state.editing_book_id = book_id
            with col2:
                if st.button(f"🗑️ Delete", key=f"delete_{book_id}"):
                    delete_book(book_id)
                    st.success(f"Book '{title}' has been deleted!")
                    st.experimental_rerun()
    except Exception as e:
        st.error(f"Error displaying book: {e}")
        st.error(f"Book data: {book}")

def edit_book_form(book_id):
    book = get_book_by_id(book_id)
    if book:
        with st.form(f"edit_form_{book_id}"):
            st.markdown(f"<div class='edit-form'>", unsafe_allow_html=True)
            title = st.text_input("📚 Title", value=book[1])
            author = st.text_input("✍️ Author", value=book[2])
            year = st.number_input("📅 Publication Year", min_value=0, max_value=2025, value=book[3])
            genre = st.selectbox("🏷️ Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Mystery", "Romance", "Fantasy", "Biography", "History", "Self-Help", "Other"], 
                                index=["Fiction", "Non-Fiction", "Science Fiction", "Mystery", "Romance", "Fantasy", "Biography", "History", "Self-Help", "Other"].index(book[4]))
            read_status = st.checkbox("📖 Have you read this book?", value=bool(book[5]))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                    update_book(book_id, title, author, year, genre, read_status)
                    st.session_state.editing_book_id = None
                    st.success("Book updated successfully!")
                    st.experimental_rerun()
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.editing_book_id = None
                    st.experimental_rerun()
            st.markdown("</div>", unsafe_allow_html=True)

if selected == "Add Book":
    st.header("Add a New Book 📕")
    st.markdown("Enter the details of the book you want to add to your library:")
    
    with st.form("add_book_form"):
        title = st.text_input("📚 Title")
        author = st.text_input("✍️ Author")
        year = st.number_input("📅 Publication Year", min_value=0, max_value=2025, value=2024)
        genre = st.selectbox("🏷️ Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Mystery", "Romance", "Fantasy", "Biography", "History", "Self-Help", "Other"])
        read_status = st.checkbox("📖 Have you read this book?")
        
        if st.form_submit_button("➕ Add Book", use_container_width=True):
            if title and author:  # Basic validation
                add_book(title, author, year, genre, read_status)
                st.success("Book added successfully!")
                st.balloons()
            else:
                st.error("Please enter at least a title and author.")

elif selected == "View Books":
    st.header("Library Collection 📚")
    all_books = get_all_books()
    
    if not all_books:
        st.info("Your library is empty. Add some books!")
    else:
        # Filter options
        st.subheader("Filter Options")
        col1, col2 = st.columns(2)
        with col1:
            filter_read = st.selectbox("Filter by read status:", ["All", "Read", "Unread"])
        with col2:
            genres = list(set([book[4] for book in all_books]))
            filter_genre = st.selectbox("Filter by genre:", ["All"] + genres)
        
        # Apply filters
        filtered_books = all_books
        if filter_read != "All":
            filtered_books = [book for book in filtered_books if (filter_read == "Read" and book[5]) or (filter_read == "Unread" and not book[5])]
        if filter_genre != "All":
            filtered_books = [book for book in filtered_books if book[4] == filter_genre]
        
        # Display filtered books
        st.subheader(f"Showing {len(filtered_books)} books")
        for book in filtered_books:
            if st.session_state.editing_book_id == book[0]:
                edit_book_form(book[0])
            else:
                display_book(book)

elif selected == "Search":
    st.header("Search Books 🔍")
    search_term = st.text_input("Enter title, author, or genre to search")
    if search_term:
        results = search_books(search_term)
        if results:
            st.subheader(f"Found {len(results)} matching books")
            for book in results:
                if st.session_state.editing_book_id == book[0]:
                    edit_book_form(book[0])
                else:
                    display_book(book)
        else:
            st.info("No matching books found")

elif selected == "Statistics":
    st.header("Library Statistics 📊")
    stats = get_library_stats()
    total_books = stats['total_books']
    
    if total_books == 0:
        st.info("Add some books to see statistics!")
    else:
        read_books = stats['read_books']
        unread_books = total_books - read_books
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        
        # Main metrics with improved UI using direct HTML/CSS for better color control
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">📚 Total Books</div>
                <div class="stat-value">{total_books}</div>
                <div class="stat-label">in your collection</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">📖 Books Read</div>
                <div class="stat-value">{read_books}</div>
                <div class="stat-label">completed books</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">📊 Completion Rate</div>
                <div class="stat-value">{percentage_read:.1f}%</div>
                <div class="stat-label">of library completed</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Reading progress bar with enhanced styling
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Reading Progress</div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {percentage_read}%;"></div>
            </div>
            <div class="stat-label">{read_books} out of {total_books} books read</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Genre distribution with improved UI
        if stats['genre_counts']:
            st.markdown('<div class="stat-title">Genre Distribution 🏷️</div>', unsafe_allow_html=True)
            for genre, count in sorted(stats['genre_counts'].items(), key=lambda x: x[1], reverse=True):
                percentage = count/total_books*100
                genre_width = int(percentage)
                st.markdown(f"""
                <div class="stat-card">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div style="color: #ffffff !important; font-weight: 600;">{genre}</div>
                        <div style="color: #ffffff !important;">{count} books ({percentage:.1f}%)</div>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {genre_width}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Publication year distribution with improved UI
        st.markdown('<div class="stat-title">Publication Years 📅</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card">
            <div style="color: #ffffff !important; font-weight: 500;">Books in your library span from <b>{stats['year_min']}</b> to <b>{stats['year_max']}</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent additions with improved UI
        if total_books > 0:
            recent_books = get_all_books()[-3:]  # Get last 3 added books
            st.markdown('<div class="stat-title">Recently Added Books 🆕</div>', unsafe_allow_html=True)
            for book in recent_books[::-1]:  # Show newest first
                st.markdown(f"""
                <div class="stat-card">
                    <div style="font-weight: 600; color: #ffffff !important;">{book[1]}</div>
                    <div style="color: #ffffff !important;">by {book[2]}</div>
                </div>
                """, unsafe_allow_html=True)

elif selected == "Exit":
    st.header("Exit Application 👋")
    st.write("Thank you for using the Personal Library Manager!")
    st.write("All your books have been saved.")
    st.markdown("""
    <div class="exit-button" onclick="window.close()">
        Exit Application
    </div>
    """, unsafe_allow_html=True)
    st.info("Note: The 'Exit' button may not work in all browsers. You can safely close this tab.")
    
    if st.button("Save and Exit"):
        st.success("Library saved successfully!")
        st.balloons()
        st.stop()