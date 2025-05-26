import os
import sys
import json
import tempfile
import subprocess
from typing import List, Optional, Tuple


def create_query_extractor_script(code_str: str, user_inputs: List[str]) -> str:
    """
    Create a Python script that wraps the user code with query capturing logic.
    
    Args:
        code_str: The Python code to analyze
        user_inputs: List of input values to provide
        
    Returns:
        A string containing a complete Python script
    """
    # Format the user code with proper indentation
    indented_code = "\n        ".join(code_str.splitlines())
    
    # Create the wrapper script with mock objects and query capturing
    wrapper_script = """
import sqlite3
import json
import sys
from unittest.mock import patch
from io import StringIO

# Store captured queries
captured_queries = []

# Setup input mocking
input_values = {0}
input_index = 0

def mock_input(prompt=''):
    global input_index
    print(prompt, end='')
    if input_index < len(input_values):
        value = input_values[input_index]
        input_index += 1
        print(value)  # Echo the input
        return value
    return "DEFAULT_INPUT"

# Mock Connection and Cursor classes
class MockConnection:
    def cursor(self):
        return MockCursor()
    def commit(self):
        pass
    def close(self):
        pass
    def execute(self, sql, parameters=None):
        # Some libraries might call execute directly on connection
        cursor = self.cursor()
        return cursor.execute(sql, parameters)

class MockCursor:
    def execute(self, sql, parameters=None):
        if parameters:
            # Handle parameter substitution
            query = sql
            if isinstance(parameters, (list, tuple)):
                # Replace ? placeholders with values
                parts = query.split('?')
                result = parts[0]
                for i, part in enumerate(parts[1:]):
                    if i < len(parameters):
                        param = parameters[i]
                        # param_str = f"'{{param}}'" if isinstance(param, str) else str(param)
                        if param == "DEFAULT_INPUT":
                            param_str = "'UNK_PARAM'"
                        else:
                            param_str = "'SAFE_PARAM'"
                        result += param_str + part
                    else:
                        result += '?' + part
                query = result
            elif isinstance(parameters, dict):
                # Replace :name placeholders with values
                for key, value in parameters.items():
                    # param_str = f"'{{value}}'" if isinstance(value, str) else str(value)
                    if value == "DEFAULT_INPUT":
                        param_str = "'UNK_PARAM'"
                    else:
                        param_str = "'SAFE_PARAM'"
                    query = query.replace(f":{{key}}", param_str)
            
            captured_queries.append(query)
        else:
            captured_queries.append(sql)
        return self
        
    def executemany(self, sql, seq_of_parameters):
        captured_queries.append(f"EXECUTEMANY: {{sql}} with {{len(seq_of_parameters)}} parameter sets")
        return self
        
    def executescript(self, sql_script):
        captured_queries.append(f"EXECUTESCRIPT: {{sql_script}}")
        return self
        
    def fetchall(self):
        return []
        
    def fetchone(self):
        return None
        
    def fetchmany(self, size=None):
        return []
        
    def __iter__(self):
        return iter([])

# Mock sqlite3.connect
def mock_connect(*args, **kwargs):
    return MockConnection()

# Set timeout for execution (5 seconds default)
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Code execution timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)  # 5 second timeout

# Execute the user code with patched objects
try:
    with patch('builtins.input', mock_input), patch('sqlite3.connect', mock_connect):
        # The actual user code will be inserted here
        {1}
except Exception as e:
    captured_queries.append(f"ERROR: {{str(e)}}")
finally:
    # Turn off the alarm
    signal.alarm(0)

# Print results as JSON for reliable parsing
print(json.dumps(captured_queries))
""".format(json.dumps(user_inputs), indented_code)
    
    return wrapper_script


def extract_sql_queries(code_str: str, user_inputs: Optional[List[str]] = None) -> List[str]:
    """
    Extract SQL queries by running code in a subprocess with mocked SQLite functions.
    
    Args:
        code_str: Python code as a string
        user_inputs: List of input values to use
    
    Returns:
        List of executed SQL queries with parameters substituted
    """
    if user_inputs is None:
        user_inputs = []
    
    # Create a temporary file for the extraction script
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as script_file:
        script_path = script_file.name
        extraction_script = create_query_extractor_script(code_str, user_inputs)
        script_file.write(extraction_script)
    
    try:
        # Run the script in a subprocess with timeout
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=10  # 10 second timeout
        )
        
        # Process the output
        if result.returncode != 0:
            # Error occurred
            return [f"ERROR: Process exited with code {result.returncode}", f"STDERR: {result.stderr}"]
        
        # Try to parse the JSON output
        try:
            output = result.stdout.strip()
            # Find the JSON part (in case there's other output)
            json_start = output.find('[')
            if json_start >= 0:
                output = output[json_start:]
            queries = json.loads(output)
            return queries
        except json.JSONDecodeError:
            return [f"ERROR: Failed to parse output as JSON", f"OUTPUT: {result.stdout}"]
    
    except subprocess.TimeoutExpired:
        return ["ERROR: Code execution timed out"]
    
    except Exception as e:
        return [f"ERROR: {str(e)}"]
    
    finally:
        # Clean up the temporary file
        if os.path.exists(script_path):
            os.unlink(script_path)


# Example usage
if __name__ == "__main__":
#     # Example code
#     example_code = """
# import sqlite3

# # Connect to the database
# conn = sqlite3.connect('example.db')
# cursor = conn.cursor()

# # Get user inputs
# start_date = input("Enter start date (YYYY-MM-DD): ")
# end_date = input("Enter end date (YYYY-MM-DD): ")
# location = input("Enter location: ")

# # Simple computation example
# if location.lower() == "new york":
#     location = "NYC"
    
# location = "1; DROP TABLE inventory--"

# # Construct and execute query
# query = f"SELECT * FROM events WHERE date BETWEEN '{start_date}' AND '{end_date}' AND location = {location}"
# cursor.execute(query)

# # Parameterized query example
# cursor.execute(
#     "SELECT COUNT(*) FROM events WHERE date > ? AND attendance > ?", 
#     (end_date, "1; DROP TABLE inventory--")
# )

# # Close connection
# conn.close()
# """
    example_code = """
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_34_database.db')
cursor = conn.cursor()

# Prompt the user for input
search_term = input("Enter a product name to search for: ")

search_term = search_term.replace("'", "''")  # Escape single quotes

# Execute the SQL query to find products by name
cursor.execute("SELECT * FROM products WHERE name = ?", (search_term,))

# Fetch all rows from the query
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()"""

    # Sample inputs
    inputs = ["' OR 1=1 --"]
    
    # Extract queries
    queries = extract_sql_queries(example_code, inputs)
    
    # Print results
    print("\nExtracted SQL Queries:")
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")