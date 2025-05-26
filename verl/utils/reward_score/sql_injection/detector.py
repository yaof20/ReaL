import ast
import fire

def detect_sql_injection_vulnerabilities(code_string):
    """
    Analyzes Python code to detect potential SQL injection vulnerabilities.
    
    This function performs static analysis by:
    1. Identifying user input functions (input, request parameters, etc.)
    2. Tracking variables that contain user input
    3. Identifying sanitized variables
    4. Checking if unsanitized variables are used in SQL query construction
    
    Args:
        code_string (str): The Python code to analyze
    
    Returns:
        list: A list of dictionaries containing vulnerability information with line numbers and descriptions
    """

    vulnerabilities = []
    
    # Parse the code into an AST
    try:
        parsed_ast = ast.parse(code_string)
    except SyntaxError as e:
        return [{"line": e.lineno, "description": f"Syntax error: {str(e)}"}]
    
    # Track variables that contain user input
    tainted_variables = set()
    # Track variables that have been sanitized
    sanitized_variables = set()
    # Track variables that represent SQL queries
    sql_query_variables = {}
    # We no longer track safe executions since we need to analyze all query strings
    
    # Database library methods that might be safer but still need query inspection
    parameterized_methods = {
        'execute_params', 'executemany', 'mogrify', 'execute_values'
    }
    
    # Track defined sanitization functions and their implementations
    sanitization_functions = {}
    
    # First pass: identify function definitions that perform sanitization
    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.FunctionDef):
            # Analyze function body to determine if it's a sanitization function
            is_sanitizer = _analyze_function_for_sanitization(node)
            if is_sanitizer:
                sanitization_functions[node.name] = node
    
    # Second pass: identify tainted variables from user input
    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    
                    # Check for input() function
                    if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'input':
                        tainted_variables.add(var_name)
                    
                    # Check for string concatenation with tainted variables
                    elif isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Add):
                        if _contains_tainted_var(node.value, tainted_variables):
                            tainted_variables.add(var_name)
                    
                    # Check for f-strings with tainted variables
                    elif isinstance(node.value, ast.JoinedStr):
                        if _contains_tainted_var_in_fstring(node.value, tainted_variables):
                            tainted_variables.add(var_name)
                    
                    # Check for sanitization function calls
                    elif isinstance(node.value, ast.Call):
                        # If the variable is assigned the result of a sanitization function or operation
                        if _is_sanitization_call(node.value, sanitization_functions):
                            sanitized_variables.add(var_name)
                            # If the argument to the sanitization function was tainted, it's now clean
                            if _has_tainted_args(node.value, tainted_variables):
                                tainted_variables.discard(var_name)
    
    # Third pass: check for execute() calls and parameterized queries
    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            # Check for database query execution methods
            is_execute_method = node.func.attr == 'execute'
            is_parameterized_method = node.func.attr in parameterized_methods
            
            # Analyze any query execution method
            if (is_execute_method or is_parameterized_method) and len(node.args) >= 1:
                query_arg = node.args[0]
                
                # Check if it's a parameterized query (for better error message)
                has_params = len(node.args) >= 2
                param_message = ", even with parameterization" if has_params else ""
                
                # Direct use of tainted variable that hasn't been sanitized
                if isinstance(query_arg, ast.Name) and query_arg.id in tainted_variables and query_arg.id not in sanitized_variables:
                    vulnerabilities.append({
                        "line": node.lineno,
                        "description": f"SQL Injection vulnerability: Executing query with unsanitized variable '{query_arg.id}'{param_message}"
                    })
                
                # Direct use of f-string with tainted variables
                elif isinstance(query_arg, ast.JoinedStr) and _contains_unsanitized_var_in_fstring(query_arg, tainted_variables, sanitized_variables):
                    vulnerabilities.append({
                        "line": node.lineno,
                        "description": f"SQL Injection vulnerability: Executing query containing unsanitized user input in f-string{param_message}"
                    })
                
                # Direct string concatenation with tainted variables
                elif isinstance(query_arg, ast.BinOp) and _contains_unsanitized_var(query_arg, tainted_variables, sanitized_variables):
                    vulnerabilities.append({
                        "line": node.lineno,
                        "description": f"SQL Injection vulnerability: Executing query containing unsanitized user input via string concatenation{param_message}"
                    })
    
    # We no longer need the safe_executions set since we're checking all query strings
                        
    return vulnerabilities

def _analyze_function_for_sanitization(func_def):
    """
    Analyze a function definition to determine if it performs sanitization.
    A function is considered a sanitizer if it:
    1. Performs string replacements that escape SQL special characters
    2. Uses known sanitization libraries or methods
    3. Performs validation with rejection of invalid inputs
    4. Performs type conversion
    
    Args:
        func_def: The AST node for the function definition
        
    Returns:
        bool: True if the function appears to sanitize inputs, False otherwise
    """
    # Look for string replacement operations that escape quotes or other SQL special chars
    has_string_escape = False
    has_validation = False
    has_type_conversion = False
    
    for node in ast.walk(func_def):
        # Check for string method calls that might be escaping characters
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            # String replace methods
            if node.func.attr in {'replace', 'translate'} and len(node.args) >= 2:
                # Check if it's replacing quotes or other SQL special characters
                if _is_replacing_sql_chars(node):
                    has_string_escape = True
            
            # Regex sanitization
            elif node.func.attr in {'sub', 'subn'} and isinstance(node.func.value, ast.Name) and node.func.value.id == 're':
                has_string_escape = True
        
        # Check for type conversion
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {'int', 'float', 'decimal', 'Decimal', 'bool'}:
                has_type_conversion = True
        
        # Check for validation with conditional and return/raise
        if isinstance(node, ast.If):
            for stmt in node.body + node.orelse:
                if isinstance(stmt, (ast.Raise, ast.Return)):
                    has_validation = True
    
    # A function is a sanitizer if it does any type of SQL escaping, validation with rejection,
    # or type conversion
    return has_string_escape or has_validation or has_type_conversion

def _is_replacing_sql_chars(replace_call):
    """
    Check if a string replace call is targeting SQL special characters.
    
    Args:
        replace_call: The AST node for the replace method call
        
    Returns:
        bool: True if the call appears to be replacing SQL special characters
    """
    # SQL special characters that need escaping
    sql_special_chars = {"'", '"', ';', '-', '=', '%', '_'}
    
    # Check literal string arguments
    for arg in replace_call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            # If any SQL special character is being replaced
            if any(char in arg.value for char in sql_special_chars):
                return True
    
    return False

def _is_sanitization_call(node, sanitization_functions):
    """
    Helper function to check if a call is to a recognized sanitization function
    or performs sanitization directly
    """
    # Check if it's calling a function we've identified as a sanitizer
    if isinstance(node.func, ast.Name) and node.func.id in sanitization_functions:
        return True
    
    # Check for common database driver sanitization methods
    if isinstance(node.func, ast.Attribute):
        # Known sanitization methods in common database libraries
        known_sanitization_methods = {
            # SQLite
            'escape', 'quote', 
            # psycopg2
            'adapt', 'escape_string', 'quote_ident',
            # MySQL
            'escape_string', 'real_escape_string',
            # General
            'sanitize', 'sanitize_input', 'clean', 'prepare'
        }
        
        if node.func.attr in known_sanitization_methods:
            return True
        
        # Check for string methods that escape characters
        if node.func.attr == 'replace' and len(node.args) >= 2:
            return _is_replacing_sql_chars(node)
    
    # Check for type conversion functions
    if isinstance(node.func, ast.Name) and node.func.id in {'int', 'float', 'decimal', 'Decimal', 'bool'}:
        return True
    
    # Check for built-in parameterization/prepared statement methods
    if isinstance(node.func, ast.Attribute) and node.func.attr in {'execute', 'executemany'} and len(node.args) >= 2:
        return True
    
    return False

# Type conversion is now included in _is_sanitization_call analysis

def _has_tainted_args(call_node, tainted_variables):
    """Helper function to check if any arguments to a function call are tainted"""
    for arg in call_node.args:
        if isinstance(arg, ast.Name) and arg.id in tainted_variables:
            return True
    return False

def _contains_tainted_var(node, tainted_variables):
    """Helper function to check if an expression contains tainted variables"""
    if isinstance(node, ast.Name) and node.id in tainted_variables:
        return True
    elif isinstance(node, ast.BinOp):
        return _contains_tainted_var(node.left, tainted_variables) or _contains_tainted_var(node.right, tainted_variables)
    return False

def _contains_unsanitized_var(node, tainted_variables, sanitized_variables):
    """Helper function to check if an expression contains unsanitized tainted variables"""
    if isinstance(node, ast.Name) and node.id in tainted_variables and node.id not in sanitized_variables:
        return True
    elif isinstance(node, ast.BinOp):
        return (_contains_unsanitized_var(node.left, tainted_variables, sanitized_variables) or 
                _contains_unsanitized_var(node.right, tainted_variables, sanitized_variables))
    return False

def _contains_tainted_var_in_fstring(fstring_node, tainted_variables):
    """Helper function to check if an f-string contains tainted variables"""
    for value in fstring_node.values:
        if isinstance(value, ast.Name) and value.id in tainted_variables:
            return True
        elif isinstance(value, ast.FormattedValue) and isinstance(value.value, ast.Name) and value.value.id in tainted_variables:
            return True
    return False

def _contains_unsanitized_var_in_fstring(fstring_node, tainted_variables, sanitized_variables):
    """Helper function to check if an f-string contains unsanitized tainted variables"""
    for value in fstring_node.values:
        if isinstance(value, ast.Name) and value.id in tainted_variables and value.id not in sanitized_variables:
            return True
        elif (isinstance(value, ast.FormattedValue) and 
              isinstance(value.value, ast.Name) and 
              value.value.id in tainted_variables and 
              value.value.id not in sanitized_variables):
            return True
    return False

def main(file_path):
    """
    Main function to run the SQL injection vulnerability detector.
    
    Args:
        file_path (str): Path to the Python file to analyze
    """
    with open(file_path, 'r') as file:
        code = file.read()
    
    vulnerabilities = detect_sql_injection_vulnerabilities(code)
    
    if vulnerabilities:
        print(f"SQL Injection vulnerabilities detected in {file_path}:")
        for vuln in vulnerabilities:
            print(f"Line {vuln['line']}: {vuln['description']}")
            
        print("\nRecommended fix: Use parameterized queries instead of string formatting/concatenation")
        print("Example:\n")
        print("    query = 'SELECT * FROM products WHERE price BETWEEN ? AND ? AND category = ?'")
        print("    cursor.execute(query, (min_price_after_discount, max_price_after_discount, category))")
    else:
        print(f"No SQL Injection vulnerabilities detected in {file_path}")

# Command line usage with Fire
if __name__ == "__main__":
    fire.Fire(main)