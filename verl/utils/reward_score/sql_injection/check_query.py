import re
import sqlparse
from sqlparse.tokens import Token, String, Literal, Keyword

def check_sql_injection(query, debug=False):
    """
    Analyze an SQL query string for potential SQL injection vulnerabilities
    with improved context awareness and proper handling of different quote styles.
    """
    issues = []
    
    # 1. Check for string concatenation (still a valid concern)
    if "+" in query or "||" in query:
        if not re.search(r"'\s*\+\s*'", query) and not re.search(r"'\s*\|\|\s*'", query):  # Ignore simple string joins
            issues.append("Query appears to use string concatenation which can be vulnerable")
    
    # 2. Define injection patterns to check
    injection_patterns = [
        # UNION-based attacks
        (r"\bUNION\s+(?:ALL\s+)?SELECT\b", "UNION-based injection attempt detected"),
        
        # Multiple statements
        (r";\s*\w+", "Multiple SQL statements detected"),
        
        # Tautologies - Numeric
        (r"\bOR\s+\d+\s*=\s*\d+\b", "Numeric tautology detected (OR n=n)"),
        (r"\bAND\s+\d+\s*=\s*\d+\b", "Numeric tautology detected (AND n=n)"),
        (r"\bOR\s+\d+\s*>\s*\d+\b", "Numeric tautology detected (OR n>m)"),
        (r"\bOR\s+\d+\s*<\s*\d+\b", "Numeric tautology detected (OR n<m)"),
        
        # Tautologies - String (no word boundary at the end)
        (r"\bOR\s+'[^']*'\s*=\s*'[^']*'", "String tautology detected (OR 'a'='a')"),
        (r"\bOR\s+\"[^\"]*\"\s*=\s*\"[^\"]*\"", "String tautology detected (OR \"a\"=\"a\")"),
        (r"\bOR\s+`[^`]*`\s*=\s*`[^`]*`", "String tautology detected (OR `a`=`a`)"),
        
        # More general pattern for string tautologies
        (r"\bOR\s+(?:'[^']*'|\"[^\"]*\"|`[^`]*`)\s*=\s*(?:'[^']*'|\"[^\"]*\"|`[^`]*`)", "String tautology detected"),
        
        # Boolean-based
        (r"\bOR\s+TRUE\b", "Boolean-based injection detected (OR TRUE)"),
        (r"\bOR\s+1\b", "Numeric injection detected (OR 1)"),
        
        # Function-based attacks
        (r"\bSLEEP\s*\(", "Time-based injection attempt (SLEEP)"),
        (r"\bBENCHMARK\s*\(", "Time-based injection attempt (BENCHMARK)"),
        (r"\bWAITFOR\s+DELAY\b", "Time-based injection attempt (WAITFOR DELAY)"),
        
        # Command execution
        (r"\bEXEC\s+\w+|EXECUTE\s+\w+", "Command execution attempt"),
        (r"\bxp_cmdshell\b", "Command execution attempt (xp_cmdshell)"),
    ]
    
    try:
        # 3. Parse the SQL properly with sqlparse
        parsed = sqlparse.parse(query)
        
        # 4. Check for multiple statements
        if len(parsed) > 1:
            issues.append("Multiple SQL statements detected")
        
        # 5. Extract the SQL structure properly, handling all quote types
        def extract_sql_structure(parsed_stmt):
            """
            Extracts SQL structure from parsed statements,
            replacing all string literals with placeholders.
            """
            structure_parts = []
            
            for token in parsed_stmt.flatten():
                # Check if token is ANY kind of string literal
                is_string = False
                
                # Handle all string token types
                if token.ttype in (String.Single, String.Double, String.Symbol, 
                                  Literal.String.Single, Literal.String.Double, 
                                  Literal.String.Symbol):
                    if debug:
                        print(f"String token: {token.value}")
                    is_string = True
                
                # For quoted identifiers (like `column_name`)
                if token.ttype is Token.Name.Quoted:
                    if debug:
                        print(f"String token: {token.value}")
                    is_string = True
                    
                # Add the token or a placeholder for strings
                if is_string:
                    structure_parts.append("'STRING_LITERAL'")
                else:
                    structure_parts.append(token.value)
            
            return ' '.join(structure_parts)
        
        # 6. Process each statement
        for statement in parsed:
            sql_structure = extract_sql_structure(statement)
            
            # # Print for debugging (remove in production)
            if debug:
                print(f"Original SQL: {query}")
                print(f"Analyzing SQL structure: {sql_structure}")
            
            # 7. Check patterns against the extracted structure
            for pattern, message in injection_patterns:
                if re.search(pattern, sql_structure, re.IGNORECASE):
                    issues.append(message)
                    
    except Exception as e:
        # 8. Fallback to direct pattern matching if parsing fails
        issues.append(f"Could not fully parse SQL structure: {str(e)}")
        for pattern, message in injection_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                if message not in issues:  # Avoid duplicates
                    issues.append(message)
    
    return (len(issues) > 0, issues)

def is_query_safe_from_injection(query):
    """A simpler interface that returns whether a query appears safe"""
    is_vulnerable, issues = check_sql_injection(query)
    if is_vulnerable:
        return False, issues
    return True, []

def main():
    """Test the SQL injection detection function with various test cases"""
    test_queries = [
        # Should detect as vulnerable
        "SELECT * FROM users WHERE username = 'admin' OR 1=1",
        "SELECT * FROM users WHERE username = 12345 OR 1=1",
        "SELECT * FROM users WHERE username = 'admin'; DROP TABLE users;",
        "SELECT * FROM users WHERE username = 'admin' UNION SELECT * FROM credit_cards",
        "SELECT * FROM users WHERE password = '' OR '1'='1'",
        # Test different quote styles
        "SELECT * FROM users WHERE username = \"admin\" UNION SELECT * FROM credit_cards",
        "SELECT * FROM users WHERE username = `admin` OR 1=1",
        
        # Should detect as safe
        "SELECT COUNT(*) FROM events WHERE date > '2023-01-01'",
        "SELECT * FROM products WHERE price > 100 AND category_id = 5",
        "SELECT * FROM users WHERE user_id = ?",
        "SELECT * FROM inventory WHERE item_name LIKE '%0 OR item_type=Electronics%' OR item_id = '0 OR item_type=Electronics'",
        "SELECT * FROM events WHERE attendance > '1; DROP TABLE inventory--'"
    ]

    # Test the function
    for query in test_queries:
        print(f"Query: {query}")
        is_safe, issues = is_query_safe_from_injection(query)
        status = "SAFE" if is_safe else "VULNERABLE"
        print(f"Status: {status}")
        if not is_safe:
            for issue in issues:
                print(f"- {issue}")
        print()

if __name__ == "__main__":
    main()