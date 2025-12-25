from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import re
import os
from _lessons import get_all_lessons, get_lesson_by_id

# Get the parent directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication


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


def is_safe_query(query):
    """
    Basic SQL injection prevention and dangerous operation blocking.
    Only allows SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER statements.
    Blocks potentially dangerous operations.
    """
    # Convert to uppercase for checking
    query_upper = query.upper().strip()
    
    # List of allowed statement types
    allowed_statements = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER']
    
    # Check if query starts with an allowed statement
    starts_with_allowed = any(query_upper.startswith(stmt) for stmt in allowed_statements)
    
    if not starts_with_allowed:
        return False, "Only SELECT, INSERT, UPDATE, DELETE, CREATE, and ALTER statements are allowed."
    
    # List of dangerous keywords/patterns to block
    dangerous_patterns = [
        r'\bDROP\s+DATABASE\b',
        r'\bDROP\s+SCHEMA\b',
        r'\bEXEC\b',
        r'\bEXECUTE\b',
        r'\bATTACH\b',
        r'\bDETACH\b',
        r'\bPRAGMA\b',
        r'--',  # SQL comments can be used for injection
        r'/\*',  # Block comments
        r'\bLOAD_FILE\b',
        r'\bINTO\s+OUTFILE\b',
        r'\bINTO\s+DUMPFILE\b',
    ]
    
    # Check for dangerous patterns
    for pattern in dangerous_patterns:
        if re.search(pattern, query_upper):
            return False, f"Dangerous operation detected. This operation is not allowed for security reasons."
    
    return True, "Query is safe"


# Static files are handled by Vercel directly from the root
# The API only handles /api endpoints


@app.route('/api/execute', methods=['POST'])
def execute_query():
    """Execute SQL query/queries in a sandboxed environment (supports multiple statements)"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Parse multiple statements by splitting on semicolons
        # Split by semicolon and filter out empty statements
        raw_statements = [stmt.strip() for stmt in query.split(';')]
        statements = [stmt for stmt in raw_statements if stmt]  # Remove empty strings
        
        # Check statement limit
        if len(statements) > 15:
            return jsonify({'error': 'Too many statements. Maximum 15 statements allowed per execution.'}), 400
        
        if len(statements) == 0:
            return jsonify({'error': 'No valid SQL statements found'}), 400
        
        # Validate each statement for safety
        for i, stmt in enumerate(statements):
            is_safe, message = is_safe_query(stmt)
            if not is_safe:
                return jsonify({
                    'error': f'Statement {i+1} is not safe: {message}',
                    'statement': stmt
                }), 400
        
        # Initialize fresh database for each request (stateless)
        conn = init_sample_database()
        cursor = conn.cursor()
        
        results = []
        execution_stopped = False
        
        # Execute each statement sequentially
        for i, stmt in enumerate(statements):
            try:
                # Execute the statement
                cursor.execute(stmt)
                
                # Check if it's a SELECT query (returns data)
                if stmt.upper().strip().startswith('SELECT'):
                    rows = cursor.fetchall()
                    columns = [description[0] for description in cursor.description] if cursor.description else []
                    
                    # Convert rows to list of dictionaries
                    data_results = []
                    for row in rows:
                        data_results.append(dict(zip(columns, row)))
                    
                    results.append({
                        'statementNumber': i + 1,
                        'statement': stmt,
                        'success': True,
                        'columns': columns,
                        'data': data_results,
                        'rowCount': len(data_results)
                    })
                else:
                    # For INSERT, UPDATE, DELETE, CREATE, ALTER
                    conn.commit()
                    affected_rows = cursor.rowcount
                    
                    results.append({
                        'statementNumber': i + 1,
                        'statement': stmt,
                        'success': True,
                        'message': f'Query executed successfully. Rows affected: {affected_rows}',
                        'rowCount': affected_rows
                    })
                    
            except sqlite3.Error as e:
                # Statement failed - add error result and stop execution
                results.append({
                    'statementNumber': i + 1,
                    'statement': stmt,
                    'success': False,
                    'error': f'SQL Error: {str(e)}'
                })
                execution_stopped = True
                break  # Stop executing remaining statements
        
        conn.close()
        
        # Return results for all executed statements
        return jsonify({
            'success': not execution_stopped,  # Overall success if no errors
            'multiStatement': len(statements) > 1,
            'totalStatements': len(statements),
            'executedStatements': len(results),
            'stopped': execution_stopped,
            'results': results
        })
            
    except Exception as e:
        return jsonify({'error': f'Server Error: {str(e)}'}), 500


@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    """Get all lesson metadata"""
    try:
        lessons = get_all_lessons()
        return jsonify({'success': True, 'lessons': lessons})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get specific lesson content"""
    try:
        lesson = get_lesson_by_id(lesson_id)
        if lesson:
            return jsonify({'success': True, 'lesson': lesson})
        else:
            return jsonify({'error': 'Lesson not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'SQL Learning API is running'})


# For Vercel serverless deployment
# Vercel looks for 'app' in api/index.py by default
# No special handler needed for Flask app


# For local development
if __name__ == '__main__':
    print("🚀 SQL Learning API is running on http://localhost:5000")
    print("📚 Available endpoints:")
    print("   - POST /api/execute - Execute SQL queries")
    print("   - GET  /api/lessons - Get all lessons")
    print("   - GET  /api/lessons/<id> - Get specific lesson")
    print("   - GET  /api/health - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)
