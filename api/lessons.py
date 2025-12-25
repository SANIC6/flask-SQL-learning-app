"""
Lesson content for SQL Learning App
Each lesson contains theory, examples, and practice exercises
"""

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
