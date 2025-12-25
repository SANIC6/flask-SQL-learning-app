from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import re
import os

# Get the parent directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)  # Enable CORS for frontend communication

# --- LESSON DATA ---
LESSONS = [
    {
        "id": 1,
        "title": "Introduction to SQL",
        "category": "KANTO BASICS",
        "content": {
            "description": "Understand what SQL is and why we use it.",
            "theory": """SQL (Structured Query Language) is the standard language for dealing with Relational Databases.

Think of it as a way to talk to data. You can ask questions (queries), add new data, or change existing data.

**Key Concepts:**
- **Data** is stored in **Tables**
- Tables have **Rows** (records) and **Columns** (fields)
- We use **Statements** to interact with these tables""",
            "examples": [
                {
                    "title": "Your Challenge",
                    "description": "Run a SELECT * FROM trainers query to see the data.",
                    "query": "SELECT * FROM trainers;",
                    "explanation": "This query retrieves all columns (*) from the trainers table."
                }
            ]
        }
    },
    {
        "id": 2,
        "title": "Relational Databases",
        "category": "KANTO BASICS",
        "content": {
            "description": "Learn how data is organized in tables with relationships.",
            "theory": """A Relational Database organizes data into tables that can be linked—or related—based on data common to each.

**Key Features:**
- **Tables**: Store data in rows and columns
- **Relationships**: Tables can be connected through common fields
- **Primary Keys**: Unique identifiers for each row
- **Foreign Keys**: References to primary keys in other tables

**Example:**
A `trainers` table might have a `trainer_id` as primary key.
A `pokemon` table might reference `trainer_id` as a foreign key to link Pokemon to trainers.""",
            "examples": [
                {
                    "title": "View Related Data",
                    "description": "See how trainers and pokemon tables are related.",
                    "query": "SELECT trainers.name, pokemon.name AS pokemon, pokemon.type\nFROM trainers\nJOIN pokemon ON trainers.id = pokemon.trainer_id;",
                    "explanation": "This joins two tables to show which trainer has which Pokemon."
                }
            ]
        }
    },
    {
        "id": 3,
        "title": "SQL Statements",
        "category": "KANTO BASICS",
        "content": {
            "description": "Overview of the main SQL statement types.",
            "theory": """SQL statements are commands we use to interact with databases. They fall into several categories:

**Data Manipulation Language (DML):**
- `SELECT` - Retrieve data
- `INSERT` - Add new data
- `UPDATE` - Modify existing data
- `DELETE` - Remove data

**Data Definition Language (DDL):**
- `CREATE` - Create new tables or databases
- `ALTER` - Modify table structure
- `DROP` - Delete tables or databases

**Data Control Language (DCL):**
- `GRANT` - Give permissions
- `REVOKE` - Remove permissions""",
            "examples": [
                {
                    "title": "Basic SELECT Statement",
                    "description": "The most common SQL statement - retrieving data.",
                    "query": "SELECT name, hometown FROM trainers;",
                    "explanation": "Retrieves only the name and hometown columns from the trainers table."
                }
            ]
        }
    },
    {
        "id": 4,
        "title": "CREATE TABLE",
        "category": "GYM CHALLENGES",
        "content": {
            "description": "Learn how to create new tables in your database.",
            "theory": """The CREATE TABLE statement creates a new table in the database.

**Syntax:**
```sql
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    column3 datatype
);
```

**Common Data Types:**
- `INTEGER` - Whole numbers
- `TEXT` - String/text data
- `REAL` - Decimal numbers
- `BLOB` - Binary data
- `NULL` - Empty value""",
            "examples": [
                {
                    "title": "Create a Moves Table",
                    "description": "Create a new table to store Pokemon move information.",
                    "query": "CREATE TABLE moves (\n    id INTEGER,\n    name TEXT,\n    type TEXT,\n    power INTEGER\n);",
                    "explanation": "Creates a moves table with 4 columns: id, name, type, and power."
                },
                {
                    "title": "Verify Table Creation",
                    "description": "Check that the table was created (it will be empty).",
                    "query": "SELECT * FROM moves;",
                    "explanation": "This will show the table structure but no data yet."
                }
            ]
        }
    },
    {
        "id": 5,
        "title": "INSERT INTO",
        "category": "GYM CHALLENGES",
        "content": {
            "description": "Add new data to your tables.",
            "theory": """The INSERT INTO statement adds new rows to a table.

**Syntax for single row:**
```sql
INSERT INTO table_name (column1, column2)
VALUES (value1, value2);
```

**Syntax for multiple rows:**
```sql
INSERT INTO table_name (column1, column2)
VALUES 
    (value1, value2),
    (value3, value4);
```

**Note:** If you insert values for all columns in order, you can omit the column names.""",
            "examples": [
                {
                    "title": "Insert a Single Trainer",
                    "description": "Add one new trainer to the trainers table.",
                    "query": "INSERT INTO trainers (id, name, hometown, badges)\nVALUES (5, 'Red', 'Pallet Town', 16);",
                    "explanation": "Adds a new trainer with id=5 to the trainers table."
                },
                {
                    "title": "Insert Multiple Pokemon",
                    "description": "Add multiple Pokemon at once.",
                    "query": "INSERT INTO pokemon (id, name, type, trainer_id, level, cp, sprite_url)\nVALUES \n    (150, 'Mewtwo', 'Psychic', 5, 70, 999, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png'),\n    (151, 'Mew', 'Psychic', 5, 50, 800, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/151.png');",
                    "explanation": "Adds two new Pokemon in a single statement."
                },
                {
                    "title": "View All Trainers",
                    "description": "See all trainers including the ones we just added.",
                    "query": "SELECT * FROM trainers;",
                    "explanation": "Displays all trainers in the table."
                }
            ]
        }
    },
    {
        "id": 6,
        "title": "The SELECT Statement",
        "category": "GYM CHALLENGES",
        "content": {
            "description": "Query and retrieve data from your database.",
            "theory": """SELECT is the most used SQL statement. It retrieves data from one or more tables.

**Basic Syntax:**
```sql
SELECT column1, column2 FROM table_name;
```

**Select all columns:**
```sql
SELECT * FROM table_name;
```

**Filtering with WHERE:**
```sql
SELECT * FROM table_name WHERE condition;
```

**Sorting with ORDER BY:**
```sql
SELECT * FROM table_name ORDER BY column ASC/DESC;
```

**Limiting results:**
```sql
SELECT * FROM table_name LIMIT number;
```""",
            "examples": [
                {
                    "title": "Select Specific Columns",
                    "description": "Get only name and type from pokemon.",
                    "query": "SELECT name, type FROM pokemon;",
                    "explanation": "Returns only the name and type columns."
                },
                {
                    "title": "Filter with WHERE",
                    "description": "Find Electric type Pokemon.",
                    "query": "SELECT * FROM pokemon WHERE type = 'Electric';",
                    "explanation": "Returns only Pokemon whose type is Electric."
                },
                {
                    "title": "Sort Results",
                    "description": "Get Pokemon ordered by level (highest first).",
                    "query": "SELECT name, level FROM pokemon ORDER BY level DESC;",
                    "explanation": "DESC means descending order (largest to smallest)."
                },
                {
                    "title": "Limit Results",
                    "description": "Get only the first 3 Pokemon.",
                    "query": "SELECT * FROM pokemon LIMIT 3;",
                    "explanation": "LIMIT restricts the number of rows returned."
                }
            ]
        }
    },
    {
        "id": 7,
        "title": "ALTER TABLE",
        "category": "EVOLUTION TECHNIQUES",
        "content": {
            "description": "Modify the structure of existing tables.",
            "theory": """ALTER TABLE modifies an existing table's structure.

**Add a new column:**
```sql
ALTER TABLE table_name 
ADD column_name datatype;
```

**Rename a table:**
```sql
ALTER TABLE old_name 
RENAME TO new_name;
```

**Note:** SQLite has limited ALTER TABLE support compared to other databases. You can add columns and rename tables, but dropping columns requires recreating the table.""",
            "examples": [
                {
                    "title": "Add a Column",
                    "description": "Add a 'nickname' column to the pokemon table.",
                    "query": "ALTER TABLE pokemon ADD nickname TEXT;",
                    "explanation": "Adds a new nickname column. Existing rows will have NULL for this column."
                },
                {
                    "title": "View Updated Table",
                    "description": "See the table with the new column.",
                    "query": "SELECT * FROM pokemon;",
                    "explanation": "The nickname column now exists but is empty (NULL) for all Pokemon."
                }
            ]
        }
    },
    {
        "id": 8,
        "title": "UPDATE",
        "category": "EVOLUTION TECHNIQUES",
        "content": {
            "description": "Modify existing data in your tables.",
            "theory": """UPDATE changes existing data in a table.

**Syntax:**
```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;
```

**⚠️ WARNING:** Always use a WHERE clause! Without it, ALL rows will be updated.

**Examples:**
- Update one row: `WHERE id = 1`
- Update multiple rows: `WHERE age > 30`
- Update all rows: Omit WHERE (use carefully!)""",
            "examples": [
                {
                    "title": "Update a Single Pokemon",
                    "description": "Level up Pikachu.",
                    "query": "UPDATE pokemon\nSET level = 30, cp = 450\nWHERE name = 'Pikachu';",
                    "explanation": "Updates only the row where name is 'Pikachu'."
                },
                {
                    "title": "Update Multiple Columns",
                    "description": "Update both level and CP for a Pokemon.",
                    "query": "UPDATE pokemon\nSET level = 35, cp = 600\nWHERE name = 'Gyarados';",
                    "explanation": "You can update multiple columns in one statement."
                },
                {
                    "title": "View Updated Data",
                    "description": "See the changes we made.",
                    "query": "SELECT * FROM pokemon;",
                    "explanation": "Displays all Pokemon with updated information."
                }
            ]
        }
    },
    {
        "id": 9,
        "title": "DELETE",
        "category": "EVOLUTION TECHNIQUES",
        "content": {
            "description": "Remove data from your tables.",
            "theory": """DELETE removes rows from a table.

**Syntax:**
```sql
DELETE FROM table_name
WHERE condition;
```

**⚠️ WARNING:** Always use a WHERE clause! Without it, ALL rows will be deleted.

**Examples:**
- Delete one row: `WHERE id = 1`
- Delete multiple rows: `WHERE age < 18`
- Delete all rows: `DELETE FROM table_name` (use carefully!)

**Note:** DELETE removes the data but keeps the table structure. Use DROP TABLE to remove the entire table.""",
            "examples": [
                {
                    "title": "Delete a Single Pokemon",
                    "description": "Remove the Pokemon with id = 7.",
                    "query": "DELETE FROM pokemon WHERE id = 7;",
                    "explanation": "Removes only the row where id equals 7 (Squirtle)."
                },
                {
                    "title": "Delete Multiple Pokemon",
                    "description": "Remove all Pokemon below level 15.",
                    "query": "DELETE FROM pokemon WHERE level < 15;",
                    "explanation": "Removes all rows matching the condition."
                },
                {
                    "title": "View Remaining Pokemon",
                    "description": "See what's left after deletions.",
                    "query": "SELECT * FROM pokemon;",
                    "explanation": "Shows the remaining Pokemon in the table."
                }
            ]
        }
    },
    {
        "id": 10,
        "title": "SQL Constraints",
        "category": "MASTERBALL SKILLS",
        "content": {
            "description": "Enforce rules on your data to maintain integrity.",
            "theory": """Constraints are rules enforced on data columns to ensure accuracy and reliability.

**Common Constraints:**

**PRIMARY KEY** - Uniquely identifies each row
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
);
```

**NOT NULL** - Column cannot be empty
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
```

**UNIQUE** - All values must be different
```sql
CREATE TABLE users (
    email TEXT UNIQUE
);
```

**DEFAULT** - Sets a default value
```sql
CREATE TABLE users (
    status TEXT DEFAULT 'active'
);
```

**CHECK** - Ensures values meet a condition
```sql
CREATE TABLE users (
    age INTEGER CHECK(age >= 18)
);
```

**FOREIGN KEY** - Links to another table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```""",
            "examples": [
                {
                    "title": "Create Table with Constraints",
                    "description": "Create a table with multiple constraints.",
                    "query": "CREATE TABLE caught_pokemon (\n    id INTEGER PRIMARY KEY,\n    species TEXT NOT NULL,\n    nickname TEXT UNIQUE,\n    level INTEGER CHECK(level >= 1 AND level <= 100),\n    status TEXT DEFAULT 'Active'\n);",
                    "explanation": "This table has PRIMARY KEY, NOT NULL, UNIQUE, CHECK, and DEFAULT constraints."
                },
                {
                    "title": "Insert Valid Data",
                    "description": "Add a Pokemon that meets all constraints.",
                    "query": "INSERT INTO caught_pokemon (id, species, nickname, level)\nVALUES (1, 'Pikachu', 'Sparky', 25);",
                    "explanation": "This insert succeeds because it meets all constraints."
                },
                {
                    "title": "View Caught Pokemon",
                    "description": "See the Pokemon data.",
                    "query": "SELECT * FROM caught_pokemon;",
                    "explanation": "Notice the status column has 'Active' as default value."
                }
            ]
        }
    }
]

def get_all_lessons():
    """Return metadata for all lessons"""
    return [
        {
            "id": lesson["id"],
            "title": lesson["title"],
            "category": lesson["category"]
        }
        for lesson in LESSONS
    ]

def get_lesson_by_id(lesson_id):
    """Return full lesson content by ID"""
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    return None

# --- DATABASE SETUP ---
def init_sample_database():
    """Initialize an in-memory SQLite database with Pokemon-themed data"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create trainers table
    cursor.execute('''
        CREATE TABLE trainers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            hometown TEXT,
            badges INTEGER DEFAULT 0
        )
    ''')
    
    # Insert sample trainers
    sample_trainers = [
        (1, 'Ash Ketchum', 'Pallet Town', 8),
        (2, 'Misty', 'Cerulean City', 8),
        (3, 'Brock', 'Pewter City', 8),
        (4, 'Gary Oak', 'Pallet Town', 10)
    ]
    cursor.executemany('INSERT INTO trainers VALUES (?, ?, ?, ?)', sample_trainers)
    
    # Create pokemon table
    cursor.execute('''
        CREATE TABLE pokemon (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            trainer_id INTEGER,
            level INTEGER DEFAULT 5,
            cp INTEGER,
            sprite_url TEXT,
            FOREIGN KEY (trainer_id) REFERENCES trainers(id)
        )
    ''')
    
    # Insert sample pokemon
    sample_pokemon = [
        (25, 'Pikachu', 'Electric', 1, 25, 320, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'),
        (1, 'Bulbasaur', 'Grass', 1, 15, 180, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'),
        (4, 'Charmander', 'Fire', 1, 12, 150, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png'),
        (7, 'Squirtle', 'Water', 1, 10, 140, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png'),
        (120, 'Staryu', 'Water', 2, 22, 280, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/120.png'),
        (121, 'Starmie', 'Water', 2, 28, 380, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/121.png'),
        (95, 'Onix', 'Rock', 3, 28, 450, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/95.png'),
        (74, 'Geodude', 'Rock', 3, 18, 220, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/74.png'),
        (59, 'Arcanine', 'Fire', 4, 30, 520, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/59.png'),
        (130, 'Gyarados', 'Water', 4, 32, 580, 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/130.png')
    ]
    cursor.executemany('INSERT INTO pokemon VALUES (?, ?, ?, ?, ?, ?, ?)', sample_pokemon)
    
    # Create gym_badges table
    cursor.execute('''
        CREATE TABLE gym_badges (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            type TEXT NOT NULL,
            gym_leader TEXT
        )
    ''')
    
    # Insert sample gym badges
    sample_badges = [
        (1, 'Boulder Badge', 'Pewter City', 'Rock', 'Brock'),
        (2, 'Cascade Badge', 'Cerulean City', 'Water', 'Misty'),
        (3, 'Thunder Badge', 'Vermilion City', 'Electric', 'Lt. Surge'),
        (4, 'Rainbow Badge', 'Celadon City', 'Grass', 'Erika'),
        (5, 'Soul Badge', 'Fuchsia City', 'Poison', 'Koga'),
        (6, 'Marsh Badge', 'Saffron City', 'Psychic', 'Sabrina'),
        (7, 'Volcano Badge', 'Cinnabar Island', 'Fire', 'Blaine'),
        (8, 'Earth Badge', 'Viridian City', 'Ground', 'Giovanni')
    ]
    cursor.executemany('INSERT INTO gym_badges VALUES (?, ?, ?, ?, ?)', sample_badges)
    
    # Create items table
    cursor.execute('''
        CREATE TABLE items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER,
            effect TEXT
        )
    ''')
    
    # Insert sample items
    sample_items = [
        (1, 'Potion', 'Medicine', 300, 'Restores 20 HP'),
        (2, 'Super Potion', 'Medicine', 700, 'Restores 50 HP'),
        (3, 'Pokeball', 'Pokeballs', 200, 'Standard Pokeball'),
        (4, 'Great Ball', 'Pokeballs', 600, 'Better catch rate'),
        (5, 'Ultra Ball', 'Pokeballs', 1200, 'High catch rate'),
        (6, 'Rare Candy', 'Evolution', 1000, 'Level up by 1'),
        (7, 'TM01', 'Technical Machine', 3000, 'Mega Punch'),
        (8, 'Master Ball', 'Pokeballs', 99999, '100% catch rate')
    ]
    cursor.executemany('INSERT INTO items VALUES (?, ?, ?, ?, ?)', sample_items)
    
    conn.commit()
    return conn

# --- SECURITY ---
def is_safe_query(query):
    query_upper = query.upper().strip()
    allowed_statements = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER']
    starts_with_allowed = any(query_upper.startswith(stmt) for stmt in allowed_statements)
    if not starts_with_allowed:
        return False, "Only SELECT, INSERT, UPDATE, DELETE, CREATE, and ALTER statements are allowed."
    dangerous_patterns = [
        r'\bDROP\s+DATABASE\b', r'\bDROP\s+SCHEMA\b', r'\bEXEC\b', r'\bEXECUTE\b',
        r'\bATTACH\b', r'\bDETACH\b', r'\bPRAGMA\b', r'--', r'/\*',
        r'\bLOAD_FILE\b', r'\bINTO\s+OUTFILE\b', r'\bINTO\s+DUMPFILE\b',
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, query_upper):
            return False, "Dangerous operation detected."
    return True, "Query is safe"

# --- ROUTES ---
@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(BASE_DIR, path)

@app.route('/api/execute', methods=['POST'])
def execute_query():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        raw_statements = [stmt.strip() for stmt in query.split(';')]
        statements = [stmt for stmt in raw_statements if stmt]
        if len(statements) > 15:
            return jsonify({'error': 'Too many statements. Max 15.'}), 400
        for i, stmt in enumerate(statements):
            is_safe, message = is_safe_query(stmt)
            if not is_safe:
                return jsonify({'error': f'Statement {i+1} is not safe: {message}'}), 400
        conn = init_sample_database()
        cursor = conn.cursor()
        results = []
        execution_stopped = False
        for i, stmt in enumerate(statements):
            try:
                cursor.execute(stmt)
                if stmt.upper().strip().startswith('SELECT'):
                    rows = cursor.fetchall()
                    columns = [description[0] for description in cursor.description] if cursor.description else []
                    data_results = [dict(zip(columns, row)) for row in rows]
                    results.append({
                        'statementNumber': i + 1, 'statement': stmt, 'success': True,
                        'columns': columns, 'data': data_results, 'rowCount': len(data_results)
                    })
                else:
                    conn.commit()
                    results.append({
                        'statementNumber': i + 1, 'statement': stmt, 'success': True,
                        'message': 'Success', 'rowCount': cursor.rowcount
                    })
            except sqlite3.Error as e:
                results.append({'statementNumber': i + 1, 'statement': stmt, 'success': False, 'error': str(e)})
                execution_stopped = True
                break
        conn.close()
        return jsonify({
            'success': not execution_stopped, 'multiStatement': len(statements) > 1,
            'totalStatements': len(statements), 'executedStatements': len(results),
            'stopped': execution_stopped, 'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lessons', methods=['GET'])
def get_lessons_api():
    return jsonify({'success': True, 'lessons': get_all_lessons()})

@app.route('/api/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson_api(lesson_id):
    lesson = get_lesson_by_id(lesson_id)
    if lesson:
        return jsonify({'success': True, 'lesson': lesson})
    return jsonify({'error': 'Lesson not found'}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
