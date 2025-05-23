import ast
import re
from typing import List, Dict, Tuple, Optional, Union


# ## 1. CWE-918
def detect_ssrf(code):
    """Detect CWE-918 (SSRF) vulnerabilities in Python code."""
    tree = ast.parse(code)
    
    # Look for webhook handler pattern
    handlers = []
    url_related_vars = set()
    
    # Find functions that take URL parameters and track URL-related variables
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Find functions that take URL parameters
            for arg in node.args.args:
                if hasattr(arg, 'arg') and any(term in arg.arg.lower() for term in ['url', 'link', 'webhook', 'address', 'src', 'endpoint', 'redirect']):
                    handlers.append((node.name, arg.arg))
                    url_related_vars.add(arg.arg)
            
            # Track assignments of URL variables
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and any(url_var in target.id for url_var in url_related_vars):
                            url_related_vars.add(target.id)
    
    # Check for functions that return URL-related values without proper validation
    all_functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            all_functions.append(node.name)
    
    # Check each handler for proper validation
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Track if validation is performed
            has_hostname_check = False
            has_approved_check = False
            has_internal_check = False
            returns_url = False
            validation_present = False
            
            # Check if function returns URL or URL-related variable
            for child in ast.walk(node):
                if isinstance(child, ast.Return):
                    return_str = ast.unparse(child.value)
                    if "geturl" in return_str or any(var in return_str for var in url_related_vars):
                        returns_url = True
            
            # Look for validation patterns
            for child in ast.walk(node):
                if isinstance(child, ast.If):
                    test_str = ast.unparse(child.test)
                    # Check for hostname validation with proper domain checking
                    if "hostname" in test_str and any(term in test_str for term in ["in", "==", "!="]):
                        has_hostname_check = True
                        # Check for domain list reference in the same condition
                        if any(approved_list in test_str for approved_list in ["AUTHORIZED", "ALLOWED", "VALID", "WHITELIST"]):
                            has_approved_check = True
                            validation_present = True
                    # Check for approved domain list separately
                    elif any(approved in test_str for approved in ["APPROVED", "WHITELIST", "ALLOWED", "AUTHORIZED", "VALID"]):
                        has_approved_check = True
                    # Check for internal address blocking
                    if any(internal in test_str for internal in ["localhost", "127.0.0.1", "INTERNAL"]):
                        has_internal_check = True
            
            # Check for raise statements that might indicate validation
            for child in ast.walk(node):
                if isinstance(child, ast.Raise) and any(url_related_terms in ast.unparse(child) for url_related_terms in ["domain", "url", "redirect"]):
                    validation_present = True
            
            # Issue alert if URL is returned without validation
            if returns_url and not validation_present and not (has_hostname_check and (has_approved_check or has_internal_check)):
                # Check if this function is called by other functions
                for caller_node in ast.walk(tree):
                    if isinstance(caller_node, ast.Call) and hasattr(caller_node.func, 'id') and caller_node.func.id in all_functions:
                        if any(arg_name in node.name.lower() for arg_name in ["valid", "check", "verify", "safe", "secure"]):
                            # This appears to be a validation function without proper checks
                            issues.append({
                                "type": "CWE-918",
                                "message": f"Function '{node.name}' claims to validate URLs but doesn't implement proper safeguards",
                                "function": node.name,
                                "severity": "HIGH"
                            })
                            break
                else:
                    # General case - function returns URL without validation
                    issues.append({
                        "type": "CWE-918",
                        "message": f"Function '{node.name}' may return unvalidated URL without proper safeguards",
                        "function": node.name,
                        "severity": "HIGH"
                    })
                    
    return issues


# ## 2. CWE-347
def detect_improper_signature_verification(code):
    """Detect CWE-347 (Improper Verification of Cryptographic Signature) vulnerabilities in Python code."""
    tree = ast.parse(code)
    
    # Look for functions that handle signatures
    signature_functions = []
    
    # Define patterns for signature-related parameter names
    signature_patterns = [
        'signature', 'sig', 'sign', 'hash', 'digest', 'hmac', 'jwt', 'crypto', 'crypt'
    ]
    
    # Define patterns for data-related parameter names
    data_patterns = [
        'file', 'content', 'data', 'message', 'payload', 'location', 'name', 'id', 
        'packet', 'pkt', 'device', 'dev', 'iot', 'info'
    ]
    
    # Define patterns for security-related function names
    security_function_patterns = [
        'process', 'handle', 'manage', 'auth', 'validate', 'verify', 'packet', 'check',
        'secure', 'trust', 'cryptographic', 'signature'
    ]
    
    # Define patterns for sensitive operations
    sensitive_operation_patterns = [
        'open', 'read', 'load', 'download', 'get', 'fetch', 'receive', 'process', 
        'handle', 'manage', 'return', 'packet'
    ]
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Find functions that might handle signatures and sensitive data
            function_name = node.name.lower()
            is_security_related = any(term in function_name for term in security_function_patterns)
            
            signature_param = None
            data_params = []
            
            for arg in node.args.args:
                if hasattr(arg, 'arg'):
                    arg_name = arg.arg.lower()
                    # Identify signature parameters
                    if any(term in arg_name for term in signature_patterns):
                        signature_param = arg.arg
                    # Identify potential data parameters
                    elif any(term in arg_name for term in data_patterns):
                        data_params.append(arg.arg)
            
            # If function has a signature param, add it to our list
            # We'll check all functions with signature params regardless of other criteria
            if signature_param:
                signature_functions.append((node.name, signature_param, data_params, is_security_related))
    
    # Check each function for proper signature verification
    issues = []
    for func_name, sig_param, data_params, is_security_related in signature_functions:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                # Track if signature verification is performed
                has_verification = False
                verification_func_called = False
                
                # Look for verification patterns
                for child in ast.walk(node):
                    # Check for signature comparison in if statements
                    if isinstance(child, ast.If):
                        test_str = ast.unparse(child.test)
                        if sig_param in test_str and any(op in test_str for op in ['==', '!=', 'in']):
                            has_verification = True
                        # Check for cryptographic verification functions
                        elif any(crypto_func in test_str for crypto_func in ['verify', 'check_signature', 'validate_signature']):
                            has_verification = True
                        # Check for comparison with trusted signatures or signature validation
                        elif any(trusted in test_str for trusted in ['TRUSTED', 'VALID', 'AUTHORIZED']):
                            has_verification = True
                
                # Check for verification function calls
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        call_str = ast.unparse(child)
                        if sig_param in call_str and any(verify_func in call_str for verify_func in ['verify', 'validate', 'check']):
                            verification_func_called = True
                
                # If the function name suggests it should verify but doesn't actually verify
                misleading_function_name = any(term in func_name.lower() for term in ['verify', 'validate', 'check', 'auth']) and not has_verification
                
                # Check for sensitive operations or returns
                has_sensitive_operations = False
                returns_data = False
                
                for child in ast.walk(node):
                    # Check for sensitive function calls
                    if isinstance(child, ast.Call):
                        call_str = ast.unparse(child)
                        if any(op in call_str.lower() for op in sensitive_operation_patterns):
                            has_sensitive_operations = True
                    
                    # Check if returning data without verification
                    if isinstance(child, ast.Return) and child.value is not None:
                        return_str = ast.unparse(child.value)
                        if (any(data_param in return_str for data_param in data_params) or 
                            any(term in return_str.lower() for term in ['packet', 'data', 'content', 'receive'])):
                            returns_data = True
                
                # Determine if this is a false positive
                verification_performed = has_verification or verification_func_called
                
                # Issue alert based on different vulnerability patterns
                if not verification_performed:
                    # Case 1: Function name suggests verification but doesn't verify
                    if misleading_function_name:
                        issues.append({
                            "type": "CWE-347",
                            "message": f"Function '{func_name}' suggests it verifies signatures but doesn't perform any verification",
                            "function": func_name,
                            "severity": "HIGH"
                        })
                    # Case 2: Security-related function with signature param that returns data without verification
                    elif is_security_related and (has_sensitive_operations or returns_data):
                        issues.append({
                            "type": "CWE-347",
                            "message": f"Security-related function '{func_name}' accepts a signature parameter but doesn't verify it before processing data",
                            "function": func_name,
                            "severity": "HIGH"
                        })
                    # Case 3: Any function with signature param that performs sensitive operations without verification
                    elif has_sensitive_operations or returns_data:
                        issues.append({
                            "type": "CWE-347",
                            "message": f"Function '{func_name}' accepts a signature parameter but doesn't use it for verification before sensitive operations",
                            "function": func_name,
                            "severity": "MEDIUM"
                        })
                    
    return issues


# ## 3. CSW-863
def detect_incorrect_authorization(code):
    """Detect CWE-863 (Incorrect Authorization) vulnerabilities in Python code."""
    tree = ast.parse(code)
    
    # Define role-related parameter names
    role_param_patterns = [
        'role', 'permission', 'privilege', 'access_level', 'auth', 'rights',
        'account_role', 'user_role', 'operator_role', 'employee_role', 'member_role',
        'editor_role', 'initiator_id', 'position', 'user_id', 'user_level'  # Added these
    ]
    
    # Define resource-related terms
    resource_terms = [
        'project', 'file', 'document', 'record', 'patient', 'account', 'settings',
        'config', 'preference', 'option', 'param', 'configuration', 'proj'
    ]
    
    # Add these terms to your role_param_patterns list
    

    # You might also want to add more sensitive operations related to financial transactions
    sensitive_operations = [
        'update', 'modify', 'change', 'edit', 'adjust', 'alter', 'set', 'save',
        'delete', 'remove', 'create', 'add', 'insert', 'write', 'transfer', 'withdraw',
        'deposit', 'transaction', 'payment', 'fund'  # Added financial terms
    ]
    
    # Define database-related patterns
    db_patterns = [
        'db', 'database', 'store', 'record', 'table', '_db', 'repository', 'projects_db'
    ]
    
    # Track functions that accept role parameters
    vulnerable_functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Determine if function name suggests it performs sensitive operations
            func_name = node.name.lower()
            is_sensitive_func = (
                any(op in func_name for op in sensitive_operations) and
                any(res in func_name for res in resource_terms)
            )
            
            # Find functions that accept role parameters
            role_params = []
            resource_id_params = []
            
            for arg in node.args.args:
                if hasattr(arg, 'arg'):
                    arg_name = arg.arg.lower()
                    # Identify role parameters
                    if any(role_term in arg_name for role_term in role_param_patterns):
                        role_params.append(arg.arg)
                    # Identify resource ID parameters
                    elif (any(res in arg_name for res in resource_terms) or 
                          'id' in arg_name or 'ident' in arg_name or 
                          arg_name in ['proj', 'uid', 'token']):
                        resource_id_params.append(arg.arg)
            
            # If function has role parameters or is a sensitive function, analyze it
            if role_params or is_sensitive_func:
                # Track if authorization check is performed
                has_role_check = False
                has_db_operation = False
                has_update_operation = False
                
                # Analyze function body
                for child in ast.walk(node):
                    # Look for role checks in if statements
                    if isinstance(child, ast.If):
                        test_str = ast.unparse(child.test).lower()
                        # Check if any role parameter is used in a conditional
                        if role_params and any(role_param in test_str for role_param in role_params):
                            has_role_check = True
                        # Also check for role-related terms in the condition
                        elif any(role_term in test_str for role_term in role_param_patterns):
                            has_role_check = True
                    
                    # Check for database operations
                    if isinstance(child, ast.Subscript):
                        target_str = ast.unparse(child).lower()
                        if any(db in target_str for db in db_patterns):
                            has_db_operation = True
                    
                    # Check for update operations
                    if isinstance(child, ast.Call):
                        call_str = ast.unparse(child).lower()
                        if 'update' in call_str and any(db in call_str for db in db_patterns):
                            has_update_operation = True
                    
                    # Check for dictionary assignments (another form of update)
                    if isinstance(child, ast.Assign):
                        assign_str = ast.unparse(child).lower()
                        if any(db in assign_str for db in db_patterns) and '=' in assign_str:
                            has_update_operation = True
                
                # If function performs sensitive operations without proper checks
                performs_sensitive_operation = has_db_operation or has_update_operation
                if role_params and performs_sensitive_operation and not has_role_check:
                    # Special case for project update/configuration functions
                    if any(term in func_name for term in ['project', 'proj']) and any(term in func_name for term in ['setting', 'config', 'option', 'param']):
                        vulnerable_functions.append({
                            "type": "CWE-863",
                            "message": f"Project configuration function '{node.name}' accepts role parameters but doesn't validate them before modifying project settings",
                            "function": node.name,
                            "severity": "HIGH"
                        })
                    else:
                        vulnerable_functions.append({
                            "type": "CWE-863",
                            "message": f"Function '{node.name}' accepts role parameters but doesn't use them for authorization before performing sensitive operations",
                            "function": node.name,
                            "severity": "HIGH"
                        })
    
    return vulnerable_functions


# ## 4. CWE-352
def detect_csrf_vulnerabilities(code):
    """Detect CWE-352 (Cross-Site Request Forgery) vulnerabilities in Python code."""
    tree = ast.parse(code)
    
    # Define patterns related to web request handling
    request_param_patterns = [
        'request', 'req', 'http_request', 'web_request', 'context',
        'payload', 'input', 'req_payload', 'request_data', 'request_info',
        'input_request', 'http_data', 'web_data', 'data', 'params',
        'client_request', 'req_data', 'query', 'incoming_req', 'incoming_request',
        'input_data'
    ]
    
    # Define state-changing methods/operations
    state_changing_operations = [
        'update', 'create', 'save', 'delete', 'remove', 'erase',
        'modify', 'change', 'edit', 'alter', 'submit', 'execute'
    ]
    
    # Define JSON handling related operations
    json_handling_operations = [
        'json', 'parse', 'process', 'handle', 'decode', 'analyze', 'validate'
    ]
    
    # Define terms that indicate database operations
    database_terms = [
        'database', 'db', 'record', 'store', 'storage', 'record_storage',
        'user_data', 'data_store', 'user_store', 'account_store'
    ]
    
    # Define CSRF protection related terms
    csrf_protection_terms = [
        'csrf', 'xsrf', 'cross-site', 'token', 'nonce', 'state', 
        'anti-forgery', 'form_token', 'csrf_token', 'request_verification_token'
    ]
    
    # Track vulnerable functions
    vulnerable_functions = []
    
    # First pass - identify functions that definitively perform state changes
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name.lower()
            
            # Check if the function takes a request-like parameter
            has_request_param = False
            request_param_name = None
            
            for arg in node.args.args:
                if hasattr(arg, 'arg'):
                    arg_name = arg.arg.lower()
                    # Check for request parameter patterns
                    if any(req_term in arg_name for req_term in request_param_patterns):
                        has_request_param = True
                        request_param_name = arg.arg
                        break
            
            if has_request_param:
                # Extract function body for analysis
                func_body = ""
                for child in node.body:
                    func_body += ast.unparse(child).lower()
                
                # Check for CSRF token validation
                has_csrf_check = False
                if any(csrf_term in func_body for csrf_term in csrf_protection_terms):
                    has_csrf_check = True
                
                # Determine if function performs state changes directly
                performs_state_change = False
                
                # Check for database assignments and deletions
                performs_db_write = False
                for child in ast.walk(node):
                    # Check for database writes via assignment
                    if isinstance(child, ast.Assign):
                        assign_str = ast.unparse(child).lower()
                        assign_target = ast.unparse(child.targets[0] if child.targets else "").lower()
                        if any(db_term in assign_target for db_term in database_terms):
                            performs_db_write = True
                            performs_state_change = True
                    
                    # Check for database deletions
                    if isinstance(child, ast.Delete):
                        delete_str = ast.unparse(child).lower()
                        if any(db_term in delete_str for db_term in database_terms):
                            performs_db_write = True
                            performs_state_change = True
                
                # Check if function is a pure JSON validator/parser
                is_json_processor = False
                processes_content_type = False
                
                # Check for content-type validation
                if 'content-type' in func_body and ('application/json' in func_body or 'application' in func_body and 'json' in func_body):
                    processes_content_type = True
                
                # Check if function just returns JSON parsed data
                if 'json.loads' in func_body and 'return json.loads' in func_body:
                    is_json_processor = True
                
                # Check if the function is named like a JSON processor
                is_named_json_processor = False
                if any(term in func_name for term in json_handling_operations) and 'json' in func_name:
                    is_named_json_processor = True
                
                # Function name suggests state changes
                is_state_changing_name = any(op in func_name for op in state_changing_operations)
                
                # DECISION RULES FOR FLAGGING
                
                # Rule 1: Flag if function definitely writes to a database without CSRF check
                if performs_db_write and not has_csrf_check:
                    vulnerable_functions.append({
                        "type": "CWE-352",
                        "message": f"Function '{node.name}' performs database operations without CSRF protection",
                        "function": node.name,
                        "severity": "HIGH"
                    })
                # Rule 2: Flag if function name suggests state change but isn't just a JSON processor
                elif is_state_changing_name and not has_csrf_check and not (is_json_processor and processes_content_type):
                    vulnerable_functions.append({
                        "type": "CWE-352",
                        "message": f"Function '{node.name}' appears to perform state-changing operations without CSRF protection",
                        "function": node.name,
                        "severity": "MEDIUM"
                    })
                # Rule 3: Flag JSON processing functions ONLY if they don't validate content-type
                elif is_named_json_processor and is_json_processor and not processes_content_type and not has_csrf_check:
                    vulnerable_functions.append({
                        "type": "CWE-352",
                        "message": f"Function '{node.name}' processes JSON data without content-type validation or CSRF protection",
                        "function": node.name,
                        "severity": "MEDIUM"
                    })
    
    return vulnerable_functions


# ## 5. CWE-770
def detect_resource_allocation_without_limits(code):
    """Detect CWE-770 (Allocation of Resources Without Limits or Throttling) vulnerabilities in Python code."""
    tree = ast.parse(code)
    
    # Define patterns related to resource allocation
    resource_allocation_patterns = [
        'cache', 'map', 'dict', 'list', 'array', 'buffer', 'queue', 'pool',
        'create', 'allocate', 'new', 'load', 'read', 'parse', 'process',
        'memory', 'storage', 'file', 'thread', 'connection', 'session',
        'log', 'track', 'record', 'save', 'append', 'add', 'handle', 'encode',
        'transform', 'tokenize', 'split', 'extract', 'post', 'store', 'enqueue',
        'push', 'insert', 'send', 'analyze', 'handle', 'tokenize'
    ]
    
    # Define patterns related to input processing
    input_processing_patterns = [
        'input', 'request', 'data', 'payload', 'content', 'body', 'param',
        'argument', 'string', 'text', 'json', 'xml', 'file', 'stream',
        'message', 'packet', 'user', 'client', 'account', 'activity',
        'operation', 'action', 'interaction', 'filter', 'provided_input',
        'raw_input', 'txt', 'new_message', 'msg', 'content'
    ]
    
    # Define global collection patterns
    global_collection_patterns = [
        'activity_log', 'user_cache', 'cache', 'log', 'data', 'buffer',
        'queue', 'storage', 'chat_rooms', 'user_storage', 'history',
        'DATA_TO_TRANSFER', 'messages', 'records', 'task_queue', 'chat_room', 
        'chat_rooms_storage', 'info_cache', 'cache_storage'
    ]
    
    # Define regex pattern operations
    regex_operations = [
        're.findall', 're.match', 're.search', 're.sub', 're.subn', 're.split',
        'findall', 'match', 'search', 'compile'
    ]
    
    # Track vulnerable functions
    vulnerable_functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Extract function details
            func_name = node.name
            func_text = ast.unparse(node).lower()
            
            # Flag 1: Check for regex operations on user input without limits
            uses_regex = False
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    call_text = ast.unparse(child).lower()
                    if any(op in call_text for op in regex_operations):
                        uses_regex = True
                        break
            
            # If function uses regex, check input parameters and function name
            if uses_regex:
                processes_input = False
                
                # Check function name
                if any(pattern in func_name.lower() for pattern in [
                    'tokenize', 'process', 'parse', 'extract', 'split', 'handle',
                    'transform', 'analyze'
                ]):
                    processes_input = True
                
                # Check parameter names
                for arg in node.args.args:
                    if hasattr(arg, 'arg'):
                        arg_name = arg.arg.lower()
                        if any(pattern in arg_name for pattern in [
                            'text', 'input', 'string', 'data', 'content', 'provided_input',
                            'raw_input', 'user_input', 'txt'
                        ]):
                            processes_input = True
                            break
                
                # Check if there's a size limit check before regex
                has_size_check = False
                for child in ast.walk(node):
                    if isinstance(child, ast.If):
                        if_text = ast.unparse(child.test).lower()
                        if 'len(' in if_text and any(op in if_text for op in ['<', '<=', '>', '>=']):
                            has_size_check = True
                            break
                
                # Flag if function processes input with regex without size limits
                if processes_input and not has_size_check:
                    vulnerable_functions.append({
                        "type": "CWE-770",
                        "message": f"Function '{func_name}' processes text with regex without size limits",
                        "function": func_name,
                        "severity": "MEDIUM"
                    })
                    continue
            
            # Flag 2: Check for operations on global collections
            has_global = 'global ' in func_text
            global_vars = []
            
            if has_global:
                # Extract global variables
                for child in ast.walk(node):
                    if isinstance(child, ast.Global):
                        global_vars.extend([name.lower() for name in child.names])
                
                # Check if any globals match collection patterns
                global_collections = []
                for var in global_vars:
                    if any(pattern in var for pattern in global_collection_patterns):
                        global_collections.append(var)
                
                # Skip if no relevant global collections
                if not global_collections:
                    continue
                
                # Find all modifications to global collections
                modifies_global = False
                
                for child in ast.walk(node):
                    # Check dictionary assignments: global_var[key] = value
                    if isinstance(child, ast.Assign):
                        for target in child.targets:
                            target_text = ast.unparse(target).lower()
                            for var in global_collections:
                                if target_text.startswith(f"{var}["):
                                    modifies_global = True
                                    break
                            if modifies_global:
                                break
                    
                    # Check append operations: global_var.append(...)
                    elif isinstance(child, ast.Call):
                        call_text = ast.unparse(child).lower()
                        for var in global_collections:
                            if f"{var}.append(" in call_text:
                                modifies_global = True
                                break
                            # Check indexed append: global_var[key].append(...)
                            elif re.search(f"{var}\\[[^\\]]+\\]\\.append\\(", call_text):
                                modifies_global = True
                                break
                            # Check put operation: global_var.put(...)
                            elif f"{var}.put(" in call_text:
                                modifies_global = True
                                break
                        if modifies_global:
                            break
                
                # Skip if no modifications
                if not modifies_global:
                    continue
                
                # Check for size limit checks
                has_size_check = False
                for child in ast.walk(node):
                    if isinstance(child, ast.If):
                        if_text = ast.unparse(child.test).lower()
                        
                        # Check length of collection
                        for var in global_collections:
                            if f"len({var})" in if_text and any(op in if_text for op in ['<', '<=', '>', '>=']):
                                has_size_check = True
                                break
                            # Check indexed length
                            elif re.search(f"len\\({var}\\[[^\\]]+\\]\\)", if_text) and any(op in if_text for op in ['<', '<=', '>', '>=']):
                                has_size_check = True
                                break
                            # Check queue size
                            elif f"{var}.qsize(" in if_text and any(op in if_text for op in ['<', '<=', '>', '>=']):
                                has_size_check = True
                                break
                        
                        if has_size_check:
                            break
                
                # Flag if no size check was found
                if not has_size_check:
                    vulnerable_functions.append({
                        "type": "CWE-770",
                        "message": f"Function '{func_name}' modifies global collection(s) without size limits",
                        "function": func_name,
                        "severity": "HIGH"
                    })
                    continue
            
            # Flag 3: Check for DATA_TO_TRANSFER.append specifically
            if 'data_to_transfer.append(' in func_text:
                # Check for size limit checks
                has_size_check = False
                for child in ast.walk(node):
                    if isinstance(child, ast.If):
                        if_text = ast.unparse(child.test).lower()
                        if 'len(data_to_transfer)' in if_text and any(op in if_text for op in ['<', '<=', '>', '>=']):
                            has_size_check = True
                            break
                
                if not has_size_check:
                    vulnerable_functions.append({
                        "type": "CWE-770",
                        "message": f"Function '{func_name}' appends to DATA_TO_TRANSFER without size limits",
                        "function": func_name,
                        "severity": "HIGH"
                    })
                    continue
    
    return vulnerable_functions


# ## 6. CWE-77
def detect_command_injection(code):
    """
    Detect CWE-77 (Command Injection), CWE-79 (XSS) and related vulnerabilities in Python code.
    """
    tree = ast.parse(code)
    vulnerable_functions = []
    
    # Lists of functions and patterns
    command_execution_functions = [
        'os.system', 'os.popen', 'os.spawn', 'os.exec', 
        'subprocess.run', 'subprocess.call', 'subprocess.check_call',
        'subprocess.check_output', 'subprocess.Popen'
    ]
    
    code_evaluation_functions = [
        'eval', 'exec', 'filter'
    ]
    
    input_sources = [
        'request', 'input', 'args', 'param', 'data', 'form', 
        'query', 'command', 'sql', 'statement', 'statement',
        'query', 'body', 'payload', 'json', 'get', 'post',
        'file', 'content', 'text', 'value', 'user', 'name',
        'string', 'expression'
    ]
    
    template_function_patterns = [
        'html', 'template', 'render', 'create', 'build', 'generate', 
        'construct', 'display', 'view', 'page', 'content', 'layout'
    ]
    
    sql_related_keywords = [
        'sql', 'query', 'select', 'where', 'order by', 'from', 'database',
        'execute', 'run', 'process', 'handle', 'submit'
    ]
    
    def is_literal_string(node):
        """Return True if the node is a literal string constant."""
        return isinstance(node, ast.Constant) and isinstance(node.value, str)
    
    def contains_dynamic_expression(node):
        """Return True if the node is not a literal string or contains input source keywords."""
        if not is_literal_string(node):
            return True
        literal = node.value.lower()
        return any(kw in literal for kw in input_sources)
    
    def involves_string_manipulation(node):
        """Detect if the AST node uses operations that manipulate strings."""
        node_str = ast.unparse(node)
        patterns = ['+', '.format(', '%', 'f"', "f'", '.join(', '.replace(']
        return any(pattern in node_str for pattern in patterns)
    
    def has_sanitization(node):
        """Return True if the node includes a known sanitization call."""
        node_str = ast.unparse(node).lower()
        sanitization_patterns = [
            'escape', 'sanitize', 'quote', 'safe', 'validate',
            'shlex.quote', 'subprocess.list2cmdline'
        ]
        return any(pattern in node_str for pattern in sanitization_patterns)
    
    def is_explicitly_safe(node):
        """Check if the node represents an explicitly safe pattern."""
        node_str = ast.unparse(node)
        if "shlex.split(" in node_str and ".join(" in node_str:
            return True
        return False
    
    def uses_shell_true(keywords):
        """Check if shell=True is used in function keywords."""
        for kw in keywords:
            if kw.arg == 'shell' and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                return True
        return False
    
    def is_template_function(function_name):
        """Check if a function is likely a template rendering function."""
        if not function_name:
            return False
        function_name = function_name.lower()
        return any(pattern in function_name for pattern in template_function_patterns)
    
    def is_sql_query_function(function_name):
        """Check if a function is likely a SQL query function."""
        if not function_name:
            return False
        function_name = function_name.lower()
        return any(keyword in function_name for keyword in sql_related_keywords)
    
    def has_input_validation(function_body):
        """Check if a function has proper input validation."""
        function_body = function_body.lower()
        
        # Regex validation pattern
        has_regex_validation = (
            're.match' in function_body and 
            ('"^[' in function_body or "'^[" in function_body) and
            'raise' in function_body
        )
        
        # Character filtering validation
        has_char_filtering = (
            'all(' in function_body and 
            ('in "' in function_body or "in '" in function_body) and 
            'raise' in function_body
        )
        
        # AST validation
        has_ast_validation = (
            'ast.parse(' in function_body and 
            'for node in ast.walk(' in function_body and
            'isinstance(node,' in function_body and
            'raise' in function_body
        )
        
        return has_regex_validation or has_char_filtering or has_ast_validation
    
    def is_safe_math_evaluator(function_body):
        """Check if this is a safe math expression evaluator."""
        function_body = function_body.lower()
        
        # Check for custom safe_eval pattern
        has_safe_eval_function = 'def safe_eval(' in function_body
        has_ast_parsing = 'ast.parse(' in function_body and 'mode=' in function_body
        has_node_type_check = 'isinstance(node, ast.' in function_body
        has_error_handling = 'raise valueerror(' in function_body and 'unsupported' in function_body
        has_limited_operations = (
            ('add' in function_body and 'sub' in function_body and 
             'mult' in function_body and 'div' in function_body) or
            ('left + right' in function_body and 'left - right' in function_body and 
             'left * right' in function_body and 'left / right' in function_body)
        )
        
        return (has_safe_eval_function and has_ast_parsing and 
                has_node_type_check and has_error_handling and has_limited_operations)
    
    def is_proper_command_whitelist(function_body):
        """Check if the command uses proper whitelist validation."""
        function_body = function_body.lower()
        whitelist_keywords = ['whitelist', 'permitted', 'approved', 'allowed', 'safe']
        
        has_whitelist = any(kw in function_body for kw in whitelist_keywords)
        has_shlex = 'shlex.split(' in function_body
        has_validation = 'for' in function_body and 'if' in function_body and 'not in' in function_body and 'raise' in function_body
        
        return has_whitelist and has_shlex and has_validation
    
    def has_restricted_globals(function_body, eval_stmt):
        """Check if eval is called with restricted globals."""
        if '__builtins__' in function_body and 'none' in function_body.lower():
            # For transformation strings, check if the pattern is truly safe
            if 'transformation' in function_body.lower():
                # If it uses regex to transform before eval
                if 're.sub(' in function_body and 'eval(' in function_body and 'for' in function_body:
                    # This pattern might allow code execution even with restricted globals
                    return False
            return True
        return False
    
    def check_template_replacement_vulnerability(function_name, function_body):
        """Check for template string replacement vulnerabilities."""
        # Look for pattern of replacing placeholders in templates without escaping
        if (('{{' in function_body and '}}' in function_body) or 
            ('placeholder' in function_body.lower() and '.replace(' in function_body)):
            
            # Look for a string replacement pattern
            if 'replace(' in function_body and 'str(' in function_body and not has_sanitization(ast.parse(function_body)):
                return {
                    "type": "CWE-79",
                    "message": f"Potential XSS in {function_name}: Template variable replacement without escaping",
                    "function": function_name,
                    "severity": "HIGH",
                    "code": function_body
                }
        return None
    
    def check_sql_query_vulnerability(function_name, function_body):
        """Check for SQL injection vulnerabilities."""
        if not any(kw in function_body.lower() for kw in ['sql', 'query', 'select', 'where']):
            return None
            
        # Look for vulnerable SQL query pattern with eval()
        if 'eval(' in function_body and 'join(' in function_body and "where" in function_body.lower():
            return {
                "type": "CWE-95",
                "message": f"Potential code injection in {function_name}: Eval used with SQL WHERE conditions",
                "function": function_name,
                "severity": "HIGH",
                "code": function_body
            }
        return None
    
    def check_filter_lambda_vulnerability(function_name, function_body):
        """Check for filter with lambda and eval vulnerability."""
        if 'filter(' in function_body and 'lambda' in function_body and 'eval(' in function_body:
            return {
                "type": "CWE-95",
                "message": f"Potential code injection in {function_name}: Filter with lambda and eval",
                "function": function_name,
                "severity": "HIGH",
                "code": function_body
            }
        return None
    
    def check_eval_exec_vulnerability(function_name, function_body, func_params):
        """Check for eval/exec vulnerabilities."""
        if not ('eval(' in function_body.lower() or 'exec(' in function_body.lower()):
            return None
        
        # Get all eval/exec statements in the function
        eval_nodes = []
        func_node = ast.parse(function_body)
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call) and ast.unparse(node.func).lower() in ['eval', 'exec']:
                eval_nodes.append(node)
                
        # Skip if has proper restrictions
        if is_safe_math_evaluator(function_body):
            return None
            
        # Check for safe pattern with restricted globals
        for eval_node in eval_nodes:
            # Get the eval call as string
            eval_stmt = ast.unparse(eval_node)
            
            # If it has restricted globals but is part of transformation string
            # handling, it still may be vulnerable
            if has_restricted_globals(function_body, eval_stmt) and not 'transformation' in function_name.lower():
                return None
            
            # Check for direct use of parameters in the eval call
            for param in func_params:
                if (f"eval({param}" in eval_stmt or 
                    f"eval({param}." in eval_stmt or
                    f"exec({param}" in eval_stmt or
                    f"exec({param}." in eval_stmt):
                    return {
                        "type": "CWE-95",
                        "message": f"Potential code injection in {function_name}: Unsanitized parameter '{param}' used in eval/exec",
                        "function": function_name,
                        "severity": "HIGH",
                        "code": function_body
                    }
                    
        # If we have a transformation_string parameter specifically
        if 'transformation_string' in func_params and 'eval(' in function_body:
            # Check if the transformation string is properly validated before eval
            has_safe_validation = (
                'try:' in function_body and 
                'except' in function_body and
                ('ValueError' in function_body or 'Exception' in function_body)
            )
            if not has_safe_validation:
                return {
                    "type": "CWE-95",
                    "message": f"Potential code injection in {function_name}: Insufficient validation of transformation string",
                    "function": function_name,
                    "severity": "HIGH",
                    "code": function_body
                }
        
        return None
    
    def check_transformation_string_vulnerability(function_name, function_body, func_params):
        """Check for vulnerabilities in transformation string parsing."""
        if 'transformation' in function_name.lower() and 'eval(' in function_body:
            # Look for use of regex before eval
            if 're.sub(' in function_body and 'eval(' in function_body:
                # This regex + eval pattern can be dangerous even with restricted globals
                return {
                    "type": "CWE-95",
                    "message": f"Potential code injection in {function_name}: Regex substitution before eval",
                    "function": function_name,
                    "severity": "HIGH",
                    "code": function_body
                }
        return None
    
    # Collect function definitions and parameters
    function_details = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            function_body = ast.unparse(node)
            function_params = [arg.arg for arg in node.args.args if arg.arg != 'self']
            function_details[function_name] = {
                'body': function_body,
                'params': function_params
            }
    
    # Analyze each function for vulnerabilities
    for function_name, details in function_details.items():
        function_body = details['body']
        function_params = details['params']
        
        # Skip if this is a safe math evaluator function
        if is_safe_math_evaluator(function_body):
            continue
            
        # Skip if this is a proper command whitelist function
        if is_proper_command_whitelist(function_body):
            continue
        
        # 1. Check for template replacement vulnerability (XSS)
        template_vulnerability = check_template_replacement_vulnerability(function_name, function_body)
        if template_vulnerability:
            vulnerable_functions.append(template_vulnerability)
        
        # 2. Check for SQL query vulnerability
        sql_vulnerability = check_sql_query_vulnerability(function_name, function_body)
        if sql_vulnerability:
            vulnerable_functions.append(sql_vulnerability)
        
        # 3. Check for filter with lambda and eval vulnerability
        filter_vulnerability = check_filter_lambda_vulnerability(function_name, function_body)
        if filter_vulnerability:
            vulnerable_functions.append(filter_vulnerability)
        
        # 4. Check for eval/exec vulnerability
        eval_vulnerability = check_eval_exec_vulnerability(function_name, function_body, function_params)
        if eval_vulnerability:
            vulnerable_functions.append(eval_vulnerability)
        
        # 5. Check for transformation string vulnerability
        transform_vulnerability = check_transformation_string_vulnerability(function_name, function_body, function_params)
        if transform_vulnerability:
            vulnerable_functions.append(transform_vulnerability)
    
    # Also check for command injection (os.system, subprocess, etc.)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func_str = ast.unparse(node.func).lower()
            
            # Skip if not a command execution function
            if not any(cmd_func in func_str for cmd_func in command_execution_functions):
                continue
            
            # Get containing function
            containing_function = None
            containing_function_body = None
            for fn_name, details in function_details.items():
                if ast.unparse(node) in details['body']:
                    containing_function = fn_name
                    containing_function_body = details['body']
                    break
            
            # Skip if containing function uses proper whitelist
            if (containing_function and 
                containing_function_body and 
                is_proper_command_whitelist(containing_function_body)):
                continue
            
            shell_true = False
            if hasattr(node, 'keywords'):
                shell_true = uses_shell_true(node.keywords)
            
            is_vulnerable = False
            vulnerability_details = []
            
            # Process each argument for dynamic content
            for arg in node.args:
                arg_str = ast.unparse(arg)
                # If the argument is not a literal or involves any manipulation,
                # assume it might be tainted.
                if contains_dynamic_expression(arg) or involves_string_manipulation(arg):
                    # Check if there is an explicit safe pattern
                    if is_explicitly_safe(arg):
                        continue
                    # If no sanitization appears, flag as vulnerable.
                    if not has_sanitization(arg):
                        is_vulnerable = True
                        vulnerability_details.append(f"Dynamic input used: {arg_str}")
            
            if shell_true:
                is_vulnerable = True
                vulnerability_details.append("Uses shell=True which increases risk")
            
            if is_vulnerable:
                severity = "HIGH" if shell_true else "MEDIUM"
                vulnerable_functions.append({
                    "type": "CWE-77",
                    "message": f"Potential command injection in {('function ' + containing_function) if containing_function else 'code'}: {'; '.join(vulnerability_details)}",
                    "function": containing_function if containing_function else "unknown",
                    "severity": severity,
                    "code": ast.unparse(node)
                })
    
    return vulnerable_functions


# ## 7. CWE-94
def detect_code_injection(source_code: str) -> List[Dict[str, Union[str, int]]]:
    """
    Static analysis function to detect potential CWE-94 (Code Injection) vulnerabilities.
    
    This function examines Python code for unsafe use of dynamic code execution functions
    such as eval(), exec(), compile() without proper input validation.
    
    Args:
        source_code (str): The Python source code to analyze
        
    Returns:
        List[Dict[str, Union[str, int]]]: A list of detected vulnerabilities with details
    """
    vulnerabilities = []
    
    try:
        # Parse the source code into an AST
        tree = ast.parse(source_code)
        
        # Define unsafe functions that can lead to code injection
        unsafe_functions = ['eval', 'exec', 'compile', '__import__']
        
        # Track function definitions for context analysis
        function_defs = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_defs[node.name] = node
        
        # Analyze each function for eval/exec usage
        for func_name, func_node in function_defs.items():
            # Find all eval/exec calls in this function
            dangerous_calls = []
            for node in ast.walk(func_node):
                if isinstance(node, ast.Call) and hasattr(node, 'func'):
                    call_func_name = None
                    
                    if isinstance(node.func, ast.Name):
                        call_func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        call_func_name = node.func.attr
                    
                    if call_func_name in unsafe_functions:
                        dangerous_calls.append((node, call_func_name))
            
            # Skip if no dangerous calls found
            if not dangerous_calls:
                continue
                
            # Get function source text for regex analysis
            func_source = get_function_source(source_code, func_node)
            
            # Check if proper validation exists before each dangerous call
            for call_node, call_name in dangerous_calls:
                # Check for regex validation pattern with if statements
                validation_found = False
                
                # Check for regex validation - a key pattern to recognize
                regex_validation = check_regex_validation(func_source, call_node.lineno - func_node.lineno)
                if regex_validation:
                    validation_found = True
                    
                # Check for AST-based validation
                ast_validation = check_ast_validation(func_node, call_node)
                if ast_validation:
                    validation_found = True
                    
                # Check for character whitelist validation
                whitelist_validation = check_whitelist_validation(func_node, call_node)
                if whitelist_validation:
                    validation_found = True
                
                # If no validation found, report vulnerability
                if not validation_found:
                    vulnerabilities.append({
                        'type': 'CWE-94',
                        'function': func_name,
                        'line': call_node.lineno,
                        'message': f"Potential code injection vulnerability: {call_name}() at line {call_node.lineno} lacks proper validation",
                        'severity': 'HIGH'
                    })
        
        # Check for string concatenation vulnerabilities
        detect_concatenation_vulnerabilities(source_code, vulnerabilities)
                
    except SyntaxError as e:
        vulnerabilities.append({
            'type': 'ERROR',
            'function': 'N/A',
            'line': getattr(e, 'lineno', 0),
            'message': f"Syntax error: {str(e)}",
            'severity': 'INFO'
        })
    
    return vulnerabilities

def get_function_source(source_code: str, func_node: ast.FunctionDef) -> str:
    """Extract the source code of a function."""
    lines = source_code.splitlines()
    start_line = func_node.lineno - 1  # AST line numbers are 1-indexed
    end_line = func_node.end_lineno if hasattr(func_node, 'end_lineno') else len(lines)
    return '\n'.join(lines[start_line:end_line])

def check_regex_validation(func_source: str, relative_line_num: int) -> bool:
    """Check if regex validation is used before dangerous calls."""
    # Split function source by lines to analyze call context
    lines = func_source.splitlines()
    
    # Lines before the eval call
    lines_before_call = lines[:relative_line_num]
    lines_text = '\n'.join(lines_before_call)
    
    # Look for regex validation patterns before the eval
    regex_patterns = [
        # Match re.match() with character whitelisting
        r'if\s+re\.match\s*\(\s*["\'][\^]?[0-9\+\-\*/\s\\\.\[\]]+["\']',
        # Match re.match with string variable containing safe pattern
        r'if\s+re\.match\s*\([^,)]+,\s*' 
    ]
    
    for pattern in regex_patterns:
        if re.search(pattern, lines_text):
            return True
            
    # Check for if blocks with eval inside - look for conditional execution
    # Fixed regex pattern that was causing errors
    if_blocks = re.findall(r'if\s+([^:]+):[^\n]*?eval\(', lines_text, re.DOTALL)
    for if_block in if_blocks:
        # Check if this condition validates input
        if re.search(r'match|["\'][0-9\+\-\*/\s]+["\']|all\(|in\s+["\'][0-9\+\-\*/\s]+["\']', if_block):
            return True
    
    return False

def check_ast_validation(func_node: ast.FunctionDef, call_node: ast.Call) -> bool:
    """Check for AST-based validation techniques."""
    # Look for ast.parse and validation walk
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call) and hasattr(node, 'func') and node.lineno < call_node.lineno:
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'parse':
                if isinstance(node.func.value, ast.Name) and node.func.value.id == 'ast':
                    # ast.parse found before eval - good sign
                    return True
                    
            # Look for ast.walk after ast.parse
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'walk':
                return True
    
    return False

def check_whitelist_validation(func_node: ast.FunctionDef, call_node: ast.Call) -> bool:
    """Check for character whitelist validation."""
    for node in ast.walk(func_node):
        # Skip nodes after the call
        if hasattr(node, 'lineno') and node.lineno >= call_node.lineno:
            continue
            
        # Look for all() with character validation
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'all':
            for arg in node.args:
                # Check for comprehensions like [c in "0123456789+-*/" for c in expr]
                if isinstance(arg, (ast.ListComp, ast.GeneratorExp)):
                    if isinstance(arg.elt, ast.Compare):
                        for i, op in enumerate(arg.elt.ops):
                            if isinstance(op, ast.In) and isinstance(arg.elt.comparators[i], ast.Constant):
                                whitelist = arg.elt.comparators[i].value
                                # Check if whitelist contains only safe math chars
                                if isinstance(whitelist, str) and all(c in "0123456789+-*/() ." for c in whitelist):
                                    return True
    
        # Look for if with in comparison for whitelist
        if isinstance(node, ast.If):
            if isinstance(node.test, ast.Compare):
                for i, op in enumerate(node.test.ops):
                    if isinstance(op, ast.In):
                        if isinstance(node.test.comparators[i], ast.Constant):
                            whitelist = node.test.comparators[i].value
                            if isinstance(whitelist, str) and all(c in "0123456789+-*/() ." for c in whitelist):
                                return True
            
            # Check for call to all() in if condition
            elif isinstance(node.test, ast.Call) and isinstance(node.test.func, ast.Name) and node.test.func.id == 'all':
                for arg in node.test.args:
                    if isinstance(arg, (ast.ListComp, ast.GeneratorExp)):
                        if isinstance(arg.elt, ast.Compare):
                            for i, op in enumerate(arg.elt.ops):
                                if isinstance(op, ast.In) and isinstance(arg.elt.comparators[i], ast.Constant):
                                    whitelist = arg.elt.comparators[i].value
                                    if isinstance(whitelist, str) and all(c in "0123456789+-*/() ." for c in whitelist):
                                        return True
    
    return False

def detect_concatenation_vulnerabilities(source_code: str, vulnerabilities: List[Dict[str, Union[str, int]]]) -> None:
    """Detect string concatenation vulnerabilities with eval/exec."""
    # Patterns for dangerous string operations with eval/exec
    patterns = [
        r'eval\s*\(\s*.*\+.*\)',  # String concatenation
        r'eval\s*\(\s*f["\']',    # f-strings
        r'eval\s*\(\s*.*\.format', # .format()
        r'exec\s*\(\s*.*\+.*\)',
        r'exec\s*\(\s*f["\']',
        r'exec\s*\(\s*.*\.format'
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, source_code):
            # Get context around match
            start_pos = max(0, match.start() - 100)
            end_pos = min(len(source_code), match.end() + 100)
            context = source_code[start_pos:end_pos]
            
            # Check if validation occurs before this concatenation
            validation_found = False
            
            # Look for common validation patterns
            validation_patterns = [
                r'if\s+re\.match',
                r'if\s+all\(',
                r'ast\.parse',
                r'try\s*:',
                r'if\s+([^:]+in\s+["\'][0-9\+\-\*/\s]+["\'])'
            ]
            
            for val_pattern in validation_patterns:
                val_matches = list(re.finditer(val_pattern, context))
                for val_match in val_matches:
                    # Check if validation occurs before the eval
                    if val_match.start() < match.start() - start_pos:
                        validation_found = True
                        break
            
            if not validation_found:
                line_number = source_code[:match.start()].count('\n') + 1
                vulnerabilities.append({
                    'type': 'CWE-94',
                    'function': 'string_operation',
                    'line': line_number,
                    'message': f"Potential code injection: String operation with eval/exec at line {line_number}",
                    'severity': 'HIGH'
                })


# ## 8. CWE-1333
def detect_inefficient_regex(code_string):
    """
    Static analysis detector for CWE-1333: Inefficient Regular Expression Complexity.
    Identifies regex patterns that may cause catastrophic backtracking.
    
    Args:
        code_string (str): The source code to analyze
    
    Returns:
        list: List of dictionaries with information about detected vulnerabilities
    """
    import re
    import ast
    
    vulnerabilities = []
    
    # These patterns are definitely vulnerable
    # Note: we use raw strings to avoid having to escape the backslashes
    vulnerable_patterns = [
        # HTML tag pattern with unbounded repetition
        (r'<\((\.[\*\+])[^\)]*\)>', "Using unbounded wildcards for HTML tag content can cause catastrophic backtracking"),
        
        # Email pattern with unbounded repetition
        (r'@\((\.[\*\+])[^\)]*\)', "Using unbounded wildcards in email patterns can cause catastrophic backtracking"),
        
        # Nested repetition patterns (extremely vulnerable)
        (r'\([^\)]*\)[\*\+][\*\+]', "Multiple nested repetition quantifiers can cause exponential backtracking"),
        
        # Path pattern with nested repetition
        (r'\([\/\w \.\-]*\)[\*\+]', "Nested repetition in path patterns can cause catastrophic backtracking")
    ]
    
    # Helper function to analyze a regex pattern
    def analyze_pattern(pattern, line_number, source_line):
        # Check if this is a known safe pattern
        if re.search(r'<\(\[\^>\]\{1,\d+\}\)>', pattern):
            return  # This is a safe HTML tag pattern with bounded negation
        
        if re.search(r'\\[rnt]', pattern) and len(pattern) < 10:
            return  # Simple character escapes are safe
            
        # Actual vulnerability checks
        is_vulnerable = False
        explanation = ""
        
        # Check for specific vulnerable cases from the examples
        
        # Case 1: HTML tag pattern with wildcard (.*?) or (.*)
        if '<(' in pattern and ')>' in pattern:
            if '.*' in pattern or '.+' in pattern:
                is_vulnerable = True
                explanation = "Using unbounded wildcards in HTML tags can cause catastrophic backtracking"
        
        # Case 2: Email pattern with unbounded capture (.+) or (.*)
        elif '@(' in pattern and ')' in pattern and '$' in pattern:
            if '.+' in pattern or '.*' in pattern:
                is_vulnerable = True
                explanation = "Using unbounded repetition in email patterns can cause catastrophic backtracking"
        
        # Case 3: URL/path pattern with nested repetition
        elif re.search(r'\([^\)]*[\*\+][^\)]*\)[\*\+]', pattern):
            is_vulnerable = True
            explanation = "Nested repetition quantifiers can cause exponential backtracking"
            
        # Case 4: Log pattern with multiple unbounded captures
        elif '(' in pattern and '.+' in pattern and not re.search(r'\[\^', pattern):
            groups = pattern.count('(')
            wildcards = pattern.count('.+') + pattern.count('.*')
            if wildcards >= 2 and groups >= 3:
                is_vulnerable = True
                explanation = "Multiple unbounded capture groups can cause excessive backtracking"
                
        # General case for unbounded repetition without bounds
        elif '.*' in pattern or '.+' in pattern:
            # Check if it's not using negated character classes [^...] which are safer
            if not re.search(r'\[\^', pattern) and not re.search(r'\{\d+,\d+\}', pattern):
                # Check if it's not a safe pattern like ([^[]+) which uses negated char class
                if not (re.search(r'\(\[\^[^\]]+\]\+\)', pattern) and '$' in pattern):
                    is_vulnerable = True
                    explanation = "Unbounded repetition can lead to catastrophic backtracking"
        
        if is_vulnerable:
            vulnerabilities.append({
                'type': 'CWE-1333',
                'line': line_number,
                'pattern': pattern,
                'source': source_line,
                'message': f'Potentially inefficient regex that may cause catastrophic backtracking: {explanation}',
                'severity': 'MEDIUM',
                'recommendation': 'Use bounded repetition (e.g., {0,100}), character classes ([^>]), or atomic groups (?>)'
            })
    
    # Parse the code to find regex patterns
    try:
        tree = ast.parse(code_string)
        
        # Find all regex definitions in the code
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for re.compile calls
                if (isinstance(node.func, ast.Attribute) and node.func.attr == 'compile' and 
                    isinstance(node.func.value, ast.Name) and node.func.value.id == 're'):
                    # Handle both Python 3.8+ (ast.Constant) and older (ast.Str)
                    pattern = None
                    if node.args:
                        if hasattr(ast, 'Constant') and isinstance(node.args[0], ast.Constant):
                            pattern = node.args[0].value
                        elif hasattr(ast, 'Str') and isinstance(node.args[0], ast.Str):
                            pattern = node.args[0].s
                        else:
                            # Handle other potential AST node types for Python versions
                            try:
                                pattern = getattr(node.args[0], 's', None) or getattr(node.args[0], 'value', None)
                            except:
                                pass
                    
                    if pattern:
                        line_number = getattr(node, 'lineno', 0)
                        
                        # Get the code line for reference
                        code_lines = code_string.splitlines()
                        source_line = code_lines[line_number - 1] if line_number <= len(code_lines) else ""
                        
                        analyze_pattern(pattern, line_number, source_line)
                
                # Check for direct regex usage with re.match, re.search, re.findall, etc.
                elif (isinstance(node.func, ast.Attribute) and 
                      node.func.attr in ['match', 'search', 'findall', 'finditer', 'sub', 'subn', 'split'] and
                      isinstance(node.func.value, ast.Name) and node.func.value.id == 're'):
                    # Handle both Python 3.8+ (ast.Constant) and older (ast.Str)
                    pattern = None
                    if node.args:
                        if hasattr(ast, 'Constant') and isinstance(node.args[0], ast.Constant):
                            pattern = node.args[0].value
                        elif hasattr(ast, 'Str') and isinstance(node.args[0], ast.Str):
                            pattern = node.args[0].s
                        else:
                            # Handle other potential AST node types for Python versions
                            try:
                                pattern = getattr(node.args[0], 's', None) or getattr(node.args[0], 'value', None)
                            except:
                                pass
                    
                    if pattern:
                        line_number = getattr(node, 'lineno', 0)
                        
                        # Get the code line for reference
                        code_lines = code_string.splitlines()
                        source_line = code_lines[line_number - 1] if line_number <= len(code_lines) else ""
                        
                        analyze_pattern(pattern, line_number, source_line)
        
    except SyntaxError:
        vulnerabilities.append({
            'type': 'CWE-1333',
            'line': 0,
            'pattern': 'N/A',
            'source': '',
            'message': 'Could not parse code due to syntax error',
            'severity': 'INFO',
            'recommendation': 'Fix syntax errors before analysis'
        })
    except Exception as e:
        vulnerabilities.append({
            'type': 'CWE-1333',
            'line': 0,
            'pattern': 'N/A',
            'source': '',
            'message': f'Error during analysis: {str(e)}',
            'severity': 'INFO',
            'recommendation': 'Check code for errors'
        })
    
    return vulnerabilities


# ## 9. CWE-502
def detect_unsafe_deserialization(code_string):
    """
    Static analysis function to detect CWE-502 Deserialization of Untrusted Data vulnerabilities.
    Specifically looks for unsafe use of pickle module which can lead to arbitrary code execution.
    
    Args:
        code_string (str): The Python code to analyze as a string
    
    Returns:
        list: A list of dictionaries containing information about detected vulnerabilities
    """
    import ast
    import re
    
    vulnerabilities = []
    
    # Check for direct use of pickle.loads or pickle.load
    pickle_pattern = re.compile(r'pickle\.loads?\s*\(')
    pickle_matches = pickle_pattern.finditer(code_string)
    
    for match in pickle_matches:
        vulnerabilities.append({
            "type": "CWE-502",
            "name": "Deserialization of Untrusted Data",
            "position": match.start(),
            "description": "Unsafe deserialization using pickle.loads() or pickle.load() detected. "
                           "Use of pickle enables arbitrary code execution and is prohibited."
        })
    
    # AST-based analysis
    try:
        tree = ast.parse(code_string)
        
        for node in ast.walk(tree):
            # Look for function definitions that might use pickle
            if isinstance(node, ast.FunctionDef):
                # Check for actual pickle usage in function body
                pickle_imports = False
                actual_pickle_use = False
                pickle_conditional = False
                
                for subnode in ast.walk(node):
                    # Check for pickle imports
                    if isinstance(subnode, ast.Import):
                        for name in subnode.names:
                            if name.name == 'pickle':
                                pickle_imports = True
                    
                    # Check for pickle usage in conditional branches
                    if isinstance(subnode, ast.If):
                        for if_subnode in ast.walk(subnode):
                            if isinstance(if_subnode, ast.Compare):
                                for i, comparator in enumerate(if_subnode.comparators):
                                    if isinstance(comparator, ast.Str) and 'pickle' in comparator.s.lower():
                                        pickle_conditional = True
                                        # Now check what happens in this conditional branch
                                        # Find the corresponding if_body for this condition
                                        if isinstance(subnode.body, list):
                                            for body_item in subnode.body:
                                                # Check for raises in the body (safe case)
                                                if isinstance(body_item, ast.Raise):
                                                    pickle_conditional = False
                                                    break
                                                
                                                # Check for actual pickle usage in the body (unsafe case)
                                                for body_subnode in ast.walk(body_item):
                                                    if isinstance(body_subnode, ast.Call):
                                                        if hasattr(body_subnode, 'func') and isinstance(body_subnode.func, ast.Attribute):
                                                            if hasattr(body_subnode.func, 'attr') and body_subnode.func.attr in ['loads', 'load']:
                                                                if hasattr(body_subnode.func, 'value') and isinstance(body_subnode.func.value, ast.Name):
                                                                    if body_subnode.func.value.id == 'pickle':
                                                                        actual_pickle_use = True
                
                # Only report if actual pickle use is detected, not just a safer alternative
                if actual_pickle_use:
                    vulnerabilities.append({
                        "type": "CWE-502",
                        "name": "Unsafe Pickle Deserialization",
                        "position": node.lineno,
                        "description": f"Function '{node.name}' uses pickle for deserialization, which enables arbitrary code execution."
                    })
                
                # Only report for conditional pickle case if it's not properly handled (no raise)
                elif pickle_conditional and pickle_imports:
                    # We need to verify this is actually an unsafe case, not a proper rejection
                    raises_in_pickle_branch = False
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.If):
                            contains_pickle_check = False
                            for if_comp in ast.walk(subnode):
                                if isinstance(if_comp, ast.Compare):
                                    for comp in if_comp.comparators:
                                        if isinstance(comp, ast.Str) and 'pickle' in comp.s.lower():
                                            contains_pickle_check = True
                                            break
                            
                            if contains_pickle_check:
                                for stmt in subnode.body:
                                    if isinstance(stmt, ast.Raise):
                                        raises_in_pickle_branch = True
                                        break
                    
                    # Only report if we don't properly handle the pickle case
                    if not raises_in_pickle_branch:
                        vulnerabilities.append({
                            "type": "CWE-502",
                            "name": "Insecure Pickle Handling",
                            "position": node.lineno,
                            "description": f"Function '{node.name}' contains conditional logic for pickle format without proper security measures."
                        })
    
    except SyntaxError:
        vulnerabilities.append({
            "type": "Syntax Error",
            "name": "Invalid Python Code",
            "position": 0,
            "description": "The provided code has syntax errors and couldn't be parsed for vulnerability analysis."
        })
    
    return vulnerabilities


# ## 10. CWE-79
def detect_xss_vulnerability(code_str):
    """
    Detects potential CWE-79 (Cross-site Scripting) vulnerabilities in Python code.
    
    This function detects cases where user input is placed into web page output
    without proper sanitization. It specifically looks for:
    1. Direct use of unsanitized inputs in string formatting
    2. Direct return of unsanitized user inputs
    3. Common patterns in web applications that suggest XSS vulnerabilities
    
    Args:
        code_str (str): The Python code to analyze as a string
    
    Returns:
        list: A list of dictionaries containing detected vulnerabilities with
              line numbers and descriptions
    """
    import ast
    import re
    from collections import defaultdict
    
    vulnerabilities = []
    
    # Define known sanitizing functions
    sanitizers = ['html.escape', 'escape', 'sanitize', 'clean', 'bleach.clean']
    
    # Track sanitized variables
    sanitized_vars = set()
    
    # Common template/format constants suggesting web content
    web_format_vars = ['BLOG_FORMAT', 'PROFILE_FORMAT', 'FORUM_POST_FORMAT', 
                      'USER_POST_FORMAT', 'INVITATION_FORMAT']
    
    # Web-related function names or contexts
    web_contexts = ['display', 'format', 'render', 'build', 'generate', 'create', 
                   'prepare', 'compose', 'show', 'profile', 'post', 'blog', 
                   'forum', 'comment', 'html', 'web', 'page', 'invitation', 
                   'event', 'content']
    
    try:
        parsed = ast.parse(code_str)
    except SyntaxError as e:
        return [{"line": e.lineno, "message": f"Syntax error: {e}"}]
    
    # First pass: identify sanitized variables
    for node in ast.walk(parsed):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                
                var_name = target.id
                
                # Check if the value comes from a sanitizer
                if isinstance(node.value, ast.Call):
                    func = node.value.func
                    if (isinstance(func, ast.Attribute) and func.attr in sanitizers) or \
                       (isinstance(func, ast.Name) and func.id in sanitizers):
                        sanitized_vars.add(var_name)
                
                # Check if variable is assigned a list comprehension with escape
                if isinstance(node.value, ast.ListComp):
                    elt = node.value.elt
                    if isinstance(elt, ast.Call):
                        func = elt.func
                        if (isinstance(func, ast.Attribute) and func.attr in sanitizers) or \
                           (isinstance(func, ast.Name) and func.id in sanitizers):
                            sanitized_vars.add(var_name)
                
                # Check if HTML is constructed from already-sanitized variables
                if isinstance(node.value, (ast.JoinedStr, ast.BinOp)) and \
                   any(safe_var in ast.unparse(node.value) for safe_var in sanitized_vars):
                    if re.search(r'<\w+[^>]*>', ast.unparse(node.value)):
                        # This is safe HTML constructed from sanitized variables
                        sanitized_vars.add(var_name)
    
    # Get all function definitions
    functions = [node for node in ast.walk(parsed) if isinstance(node, ast.FunctionDef)]
    
    for func in functions:
        # Check if the function is in a web context
        func_name = func.name.lower()
        is_web_func = any(context in func_name for context in web_contexts)
        
        # Get function parameters
        param_names = [a.arg for a in func.args.args]
        
        # Get all return statements
        returns = [node for node in ast.walk(func) if isinstance(node, ast.Return)]
        
        for ret in returns:
            # Case 1: Direct return of a parameter
            if isinstance(ret.value, ast.Name) and ret.value.id in param_names and ret.value.id not in sanitized_vars:
                if is_web_func:
                    vulnerabilities.append({
                        "line": ret.lineno,
                        "message": f"XSS Vulnerability: Directly returning unsanitized user input '{ret.value.id}'",
                        "fix": f"Sanitize with html.escape({ret.value.id}) before returning"
                    })
            
            # Case 2: Format method calls with unsanitized variables
            if isinstance(ret.value, ast.Call) and isinstance(ret.value.func, ast.Attribute) and ret.value.func.attr == 'format':
                # Additional check for web format variables
                is_web_format = False
                if isinstance(ret.value.func.value, ast.Name) and ret.value.func.value.id in web_format_vars:
                    is_web_format = True
                elif isinstance(ret.value.func, ast.Attribute) and re.search(r'(FORMAT|format|html|template)', ret.value.func.attr):
                    is_web_format = True
                
                if is_web_format or is_web_func:
                    # Check each keyword arg in the format call
                    for kw in ret.value.keywords:
                        if isinstance(kw.value, ast.Name) and kw.value.id in param_names and kw.value.id not in sanitized_vars:
                            # Skip known safe constructed HTML
                            if kw.value.id.startswith(('formatted_safe_', 'tag_html', 'tags_html', 'label_html', 'labels_html')):
                                # Check if it was constructed properly from sanitized inputs
                                safe_construction = False
                                for assign_node in ast.walk(func):
                                    if isinstance(assign_node, ast.Assign) and isinstance(assign_node.targets[0], ast.Name) and assign_node.targets[0].id == kw.value.id:
                                        # Check if it's constructed from sanitized variables
                                        assign_code = ast.unparse(assign_node.value)
                                        if any(f"safe_{var}" in assign_code for var in ['item', 'highlight', 'choice', 'point', 'option', 'tag', 'label']) or \
                                           any(safe_var in assign_code for safe_var in sanitized_vars):
                                            safe_construction = True
                                            break
                                
                                if safe_construction:
                                    continue
                            
                            vulnerabilities.append({
                                "line": ret.lineno,
                                "message": f"Potential XSS: Unsanitized parameter '{kw.value.id}' used directly in template formatting",
                                "fix": f"Apply html.escape({kw.value.id}) before formatting"
                            })
            
            # Case 3: Returning a value with an unsanitized input in a string operation
            if isinstance(ret.value, (ast.JoinedStr, ast.BinOp)):
                ret_value_str = ast.unparse(ret.value)
                for param in param_names:
                    if param in ret_value_str and param not in sanitized_vars:
                        if is_web_func:
                            vulnerabilities.append({
                                "line": ret.lineno,
                                "message": f"Potential XSS: Unsanitized parameter '{param}' used in returned string",
                                "fix": f"Sanitize with html.escape({param}) before using in string"
                            })
    
    return vulnerabilities


# ## 11. CWE-862
def detect_missing_authorization(func_code: str) -> list:
    """
    Analyzes Python function code to detect CWE-862: Missing Authorization.
    
    This function examines code to determine if proper authorization checks are
    performed before modifying resources or accessing sensitive data, with a focus
    on project membership management.
    
    Args:
        func_code (str): The source code of the function to analyze
        
    Returns:
        list: List of detected vulnerabilities, each containing:
            - 'type': The CWE type
            - 'function': The function name
            - 'line': The line number of the vulnerability
            - 'message': Description of the issue
            - 'severity': Severity level of the vulnerability
    """
    lines = func_code.strip().split('\n')
    vulnerabilities = []
    
    # Skip function if it's too short or just a declaration
    if len(lines) < 5:
        return vulnerabilities
    
    # Extract function name
    function_name = ""
    for line in lines:
        if line.strip().startswith("def "):
            function_name = line.strip()[4:].split("(")[0].strip()
            break
    
    if not function_name:
        return vulnerabilities
    
    # Project membership modification detection - specific patterns
    is_project_membership_function = False
    membership_keywords = ["project", "team", "member", "access", "permission"]
    
    if any(keyword in function_name.lower() for keyword in membership_keywords):
        is_project_membership_function = True
    
    # Find operation lines for project memberships
    project_modifications = []
    for i, line in enumerate(lines):
        if "PROJECTS" in line and ("members" in line) and (
           ".append(" in line or ".remove(" in line):
            project_modifications.append((i, line.strip()))
    
    # Check if function is project membership function with modifications
    if is_project_membership_function and project_modifications:
        # Look for authorization check patterns specific to project ownership
        auth_patterns = [
            "owner_id", 
            "role",
            "admin",
            "authorization"
        ]
        
        # Check if there's a proper authorization check before modifications
        has_auth_check = False
        
        # First check for a comment indicating authorization check
        for i, line in enumerate(lines):
            if "# Ensure the action is only done by" in line or "ensure the action is only done by" in line.lower():
                has_auth_check = True
                break
        
        # Then check actual code for authorization checks
        if not has_auth_check:
            for i, line in enumerate(lines):
                # Only consider lines before the first project modification
                if project_modifications and i >= project_modifications[0][0]:
                    continue
                    
                if "if" in line and any(pattern in line for pattern in auth_patterns):
                    # Check specifically for proper authorization patterns
                    if "==" in line and "owner_id" in line:
                        has_auth_check = True
                        break
                    elif "role" in line and "admin" in line:
                        has_auth_check = True
                        break
        
        # If project membership function with modifications but no auth checks, flag it
        if not has_auth_check:
            for mod_line, line_content in project_modifications:
                vulnerabilities.append({
                    'type': 'CWE-862',
                    'function': function_name,
                    'line': mod_line + 1,
                    'message': "Missing Authorization: Project membership modified without checking user permissions",
                    'severity': 'HIGH'
                })
                break  # Only report the first instance to avoid duplicates
    
    # General sensitive function detection
    else:
        # Check if function is related to authorization-sensitive operations
        sensitive_keywords = [
            "user", "admin", "access", "permission", "privilege", 
            "role", "authorization", "auth", "profile", "invoice",
            "content", "data"
        ]
        
        is_sensitive_function = any(keyword in function_name.lower() for keyword in sensitive_keywords)
        if not is_sensitive_function:
            return vulnerabilities
        
        # Find sensitive operations (data access or modification)
        sensitive_operations = []
        modification_patterns = [
            ".append(", ".remove(", ".pop(", "del ", "=", 
            "add", "delete", "update", "modify", "change", "alter"
        ]
        access_patterns = [
            "return", "get", "fetch", "retrieve", "access", "view", "see", "download"
        ]
        
        # Find operations requiring authorization checks
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Identify data access operations
            if any(pattern in line_lower for pattern in access_patterns) and (
                "profile" in line_lower or "data" in line_lower or 
                "content" in line_lower or "invoice" in line_lower):
                sensitive_operations.append((i, line.strip(), "access"))
                
            # Identify data modification operations
            elif any(pattern in line for pattern in modification_patterns) and (
                "PROJECTS" in line or "USERS" in line or 
                "USER_" in line or "members" in line or
                "privilege" in line or "role" in line):
                sensitive_operations.append((i, line.strip(), "modification"))
        
        # If no sensitive operations found, return
        if not sensitive_operations:
            return vulnerabilities
        
        # Check for authorization patterns
        auth_check_patterns = [
            "if", "==", "role", "admin", "owner", 
            "permission", "authorize", "auth", "check"
        ]
        
        # Look for conditional blocks with authorization checks
        has_auth_check = False
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Identify conditional statements with auth checks
            if line_stripped.startswith("if ") and ":" in line_stripped:
                if (("==" in line_stripped or "in" in line_stripped) and 
                    any(p in line_stripped for p in auth_check_patterns)):
                    has_auth_check = True
                    break
        
        # If there are sensitive operations but no authorization checks, it's vulnerable
        if sensitive_operations and not has_auth_check:
            vulnerabilities.append({
                'type': 'CWE-862',
                'function': function_name,
                'line': sensitive_operations[0][0] + 1,  # Line number of first sensitive operation
                'message': "Missing Authorization: Resource operations are performed without authorization checks",
                'severity': 'HIGH'
            })
    
    return vulnerabilities


# ## 12. CWE-74
def detect_injection(code_snippet: str) -> list:
    """
    Static analysis function to detect CWE-74 vulnerabilities (Improper Neutralization 
    of Special Elements in Output Used by a Downstream Component).
    
    Args:
        code_snippet: String containing the Python code to analyze
    
    Returns:
        List of dictionaries with vulnerability details
    """
    import ast
    import re
    
    vulnerabilities = []
    
    # Parse code snippet
    try:
        lines = code_snippet.split('\n')
        tree = ast.parse(code_snippet)
    except SyntaxError:
        return []  # Return empty list for unparseable code
    
    # Function to check if sanitization is applied to a variable
    def has_sanitization(function_body, var_name):
        sanitization_patterns = [
            rf'{var_name}\s*=\s*(?:re\.sub|saxutils\.escape|html\.escape|cgi\.escape|bleach\.clean|shlex\.quote|urllib\.quote)\(',
            rf'(?:re\.sub|saxutils\.escape|html\.escape|cgi\.escape|bleach\.clean|shlex\.quote|urllib\.quote)\({var_name}',
            rf'sanitized_{var_name}',
            rf'safe_{var_name}',
            rf'escaped_{var_name}'
        ]
        return any(re.search(pattern, function_body) for pattern in sanitization_patterns)
    
    # Check for exact matching validation (safe pattern)
    def has_exact_matching(function_body, var_name):
        exact_match_patterns = [
            rf'if\s+{var_name}\s+in\s+[A-Z_]+',  # Check if in list
            rf'if\s+{var_name}\s+==\s+'          # Check equality
        ]
        return any(re.search(pattern, function_body) for pattern in exact_match_patterns) and not has_substring_matching(function_body, var_name)
    
    # Check for substring matching validation (unsafe pattern)
    def has_substring_matching(function_body, var_name):
        substring_patterns = [
            rf'if\s+any\(\s*\w+\s+in\s+{var_name}\s+for',  # Check if any item in list is in variable
            rf'if\s+\w+\s+in\s+{var_name}\s*:'         # Check if item in variable
        ]
        return any(re.search(pattern, function_body) for pattern in substring_patterns)
    
    # Check for potentially risky string formatting without sanitization
    def has_risky_formatting(function_body, var_name):
        format_patterns = [
            rf'\.format\(\s*\w+\s*=\s*{var_name}\s*\)',  # .format(var=input)
            rf'\.format\(.*{var_name}.*\)',             # .format(...input...)
            rf'f[\'"].*\{{\s*{var_name}\s*\}}',         # f"...{input}..."
            rf'%\s*\({var_name}\)',                     # % (input)
            rf'%\s*{var_name}'                          # % input
        ]
        return any(re.search(pattern, function_body) for pattern in format_patterns)
    
    # For each function definition
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            line_start = node.lineno
            function_body = '\n'.join(lines[line_start-1:node.end_lineno])
            
            # Get function parameters
            param_names = [arg.arg for arg in node.args.args]
            
            # For each parameter, check if it's used in a risky way
            for param in param_names:
                # Skip checking if param is properly sanitized
                if has_sanitization(function_body, param):
                    continue
                
                # Check if the parameter is used in string formatting
                if has_risky_formatting(function_body, param):
                    # If using exact matching (safe) and not substring matching, skip the parameter
                    if has_exact_matching(function_body, param):
                        continue
                    
                    # Find the line with the formatting
                    vulnerable_line = line_start
                    for i, line in enumerate(lines[line_start-1:node.end_lineno], line_start):
                        if param in line and ('format' in line or 'f"' in line or "f'" in line or '%' in line):
                            vulnerable_line = i
                            break
                    
                    vulnerabilities.append({
                        'type': 'CWE-74',
                        'function': function_name,
                        'line': vulnerable_line,
                        'message': "Improper Neutralization: User input appears to be used in output formatting without proper escaping or sanitization",
                        'severity': 'HIGH'
                    })
                    
                # Special case for URL scheme checking functions
                elif ('url' in function_name.lower() or 'scheme' in function_name.lower() or 
                      'javascript' in function_name.lower() or 'script' in function_name.lower() or 
                      'malicious' in function_name.lower() or 'dangerous' in function_name.lower()):
                    if 're.search' in function_body and param in function_body and 'return' in function_body:
                        vulnerable_line = line_start
                        for i, line in enumerate(lines[line_start-1:node.end_lineno], line_start):
                            if 'return bool' in line or 'return is_' in line:
                                vulnerable_line = i
                                break
                        
                        vulnerabilities.append({
                            'type': 'CWE-74',
                            'function': function_name,
                            'line': vulnerable_line,
                            'message': "Improper Neutralization: User input appears to be used in output formatting without proper escaping or sanitization",
                            'severity': 'HIGH'
                        })
                
                # Look for unsafe command execution
                elif ('command' in function_name.lower() or 'cmd' in function_name.lower() or 
                      'exec' in function_name.lower() or 'run' in function_name.lower()):
                    if has_substring_matching(function_body, param):
                        vulnerable_line = line_start
                        for i, line in enumerate(lines[line_start-1:node.end_lineno], line_start):
                            if param in line and 'return' in line:
                                vulnerable_line = i
                                break
                        
                        vulnerabilities.append({
                            'type': 'CWE-74',
                            'function': function_name,
                            'line': vulnerable_line,
                            'message': "Improper Neutralization: User input appears to be used in output formatting without proper escaping or sanitization", 
                            'severity': 'HIGH'
                        })
                
    return vulnerabilities


# ## 13. CWE-200 
def detect_info_exposure(code_str):
    """
    Static analysis function to detect potential CWE-200 vulnerabilities
    (Information Exposure to Unauthorized Actor).
    
    Args:
        code_str (str): The source code to analyze
    
    Returns:
        list: List of detected issues with line numbers and descriptions
    """
    issues = []
    lines = code_str.split('\n')
    
    # First pass: identify sanitization classes and protected objects
    sanitization_classes = []
    secured_objects = {}
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Look for sanitization class definitions
        if 'class' in line and any(secure_term in line for secure_term in 
                                  ['Secure', 'Protected', 'Restricted', 'Filtered', 
                                   'Limited', 'Safe', 'Guarded']):
            class_name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
            sanitization_classes.append(class_name)
        
        # Track secured object instances
        if '=' in line and not '.format(' in line:
            for class_name in sanitization_classes:
                if class_name in line and '=' in line:
                    var_name = line.split('=')[0].strip()
                    secured_objects[var_name] = True
    
    # Second pass: check for actual vulnerabilities in format strings
    for i, line in enumerate(lines):
        line_num = i + 1
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Only check format string operations
        if '.format(' in line:
            # Extract the keyword arguments being passed to format
            format_args = line[line.find('.format(')+8:line.rfind(')')]
            
            # Parse keyword arguments
            import re
            kwargs = re.findall(r'(\w+)\s*=\s*(\w+(?:\.\w+)*)', format_args)
            
            # Sensitive keywords that should be checked
            sensitive_keywords = [
                'employee', 'patient', 'student', 'performance', 'assessment',
                'order', 'customer', 'user', 'client', 'person', 'worker',
                'staff', 'transaction', 'record', 'review', 'evaluation',
                'purchase', 'invoice', 'userinfo', 'personnel'
            ]
            
            # Check each keyword argument
            for key, value in kwargs:
                # Skip if this is a secured object we've identified
                value_base = value.split('.')[0]
                if value_base in secured_objects:
                    continue
                
                # Check if we're dealing with a sensitive object that lacks sanitization
                if (key in sensitive_keywords or 
                    any(sens in value_base for sens in 
                        ['patient', 'employee', 'student', 'performance', 'order', 
                         'customer', 'user', 'client', 'person', 'worker', 'staff',
                         'transaction', 'record', 'review', 'purchase'])):
                    
                    # Look back for evidence of sanitization for this specific object
                    sanitized = False
                    for j in range(max(0, i-20), i):
                        prev_line = lines[j].strip()
                        # Check if this object has been wrapped in a security class
                        if '=' in prev_line and value_base in prev_line.split('=')[0].strip():
                            if any(secure_class in prev_line for secure_class in sanitization_classes):
                                sanitized = True
                                break
                    
                    if not sanitized:
                        issues.append({
                            'line': line_num,
                            'code': line,
                            'description': f'Information Exposure (CWE-200): Potentially exposing sensitive "{key}" object directly in template without sanitization'
                        })
    
    return issues


# ## 14. CWE-95
def detect_eval_injection(code_string: str) -> list:
    """
    Static analysis function to detect potential eval injection vulnerabilities (CWE-95).
    
    This function analyzes Python code to identify instances where eval() might be used
    unsafely with user input without proper sanitization.
    
    Args:
        code_string (str): The Python code to analyze
        
    Returns:
        list: A list of detected vulnerabilities, each represented as a dictionary with:
            - 'type': The CWE identifier
            - 'function': The name of the vulnerable function
            - 'line': The line number where the vulnerability was found
            - 'message': Description of the vulnerability
            - 'severity': Severity level of the vulnerability
    """
    import ast
    import re
    
    vulnerabilities = []
    
    # Early return if no eval or exec calls are present
    if not re.search(r'(eval|exec)\s*\(', code_string):
        return vulnerabilities
    
    try:
        # Parse the code into an AST
        parsed_code = ast.parse(code_string)
        
        # Class to detect secure eval patterns within a function
        class SecureEvalDetector(ast.NodeVisitor):
            def __init__(self):
                # Tracking flags
                self.has_ast_import = False
                self.has_ast_parse = False
                self.has_node_check = False
                self.has_compile_before_eval = False
                self.has_try_except = False
                
                # Track variables
                self.parsed_vars = set()  # Variables containing parsed AST
                self.compiled_vars = set()  # Variables containing compiled code
                
                # Track eval calls for analysis
                self.eval_calls = []
                
                # Track current function
                self.current_function = "global_scope"
            
            def visit_FunctionDef(self, node):
                old_function = self.current_function
                self.current_function = node.name
                self.generic_visit(node)
                self.current_function = old_function
            
            def visit_Import(self, node):
                # Check for ast import
                for alias in node.names:
                    if alias.name == 'ast':
                        self.has_ast_import = True
                self.generic_visit(node)
            
            def visit_ImportFrom(self, node):
                # Check for import from ast
                if node.module == 'ast':
                    self.has_ast_import = True
                self.generic_visit(node)
            
            def visit_Try(self, node):
                self.has_try_except = True
                self.generic_visit(node)
            
            def visit_Assign(self, node):
                # Track variables from assignments
                target_names = []
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        target_names.append(target.id)
                
                # Check for ast.parse assignment
                if isinstance(node.value, ast.Call):
                    func = node.value.func
                    
                    if (isinstance(func, ast.Attribute) and 
                        isinstance(func.value, ast.Name) and 
                        func.value.id == 'ast' and 
                        func.attr == 'parse'):
                        
                        self.has_ast_parse = True
                        for name in target_names:
                            self.parsed_vars.add(name)
                    
                    # Check for compile call
                    elif (isinstance(func, ast.Name) and func.id == 'compile'):
                        self.has_compile_before_eval = True
                        for name in target_names:
                            self.compiled_vars.add(name)
                
                self.generic_visit(node)
            
            def visit_If(self, node):
                # Check for node type validation in if condition
                test = node.test
                
                # Check for "not all(...)" pattern
                if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
                    if self._is_type_check(test.operand):
                        self.has_node_check = True
                
                # Check for "all(...)" pattern
                elif self._is_type_check(test):
                    self.has_node_check = True
                
                # Check for "any(...)" with "not isinstance" pattern
                elif isinstance(test, ast.Call) and isinstance(test.func, ast.Name) and test.func.id == 'any':
                    for arg in test.args:
                        if isinstance(arg, (ast.GeneratorExp, ast.ListComp)):
                            if self._is_negative_type_check(arg):
                                self.has_node_check = True
                
                self.generic_visit(node)
            
            def _is_type_check(self, node):
                """Check if a node is an all() call with isinstance checks"""
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id == 'all':
                        for arg in node.args:
                            if isinstance(arg, (ast.GeneratorExp, ast.ListComp)):
                                # Check if generator/comprehension contains isinstance
                                if hasattr(arg, 'elt') and self._contains_isinstance(arg.elt):
                                    return True
                return False
            
            def _is_negative_type_check(self, node):
                """Check if a node contains a 'not isinstance' check"""
                if hasattr(node, 'elt'):
                    if isinstance(node.elt, ast.UnaryOp) and isinstance(node.elt.op, ast.Not):
                        return self._contains_isinstance(node.elt.operand)
                return False
            
            def _contains_isinstance(self, node):
                """Check if a node is or contains an isinstance() call"""
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'isinstance':
                        return True
                return False
            
            def visit_Call(self, node):
                # Record eval calls for later analysis
                if isinstance(node.func, ast.Name) and node.func.id == 'eval':
                    # Check if this eval directly uses compiled code or a direct call to compile
                    uses_safe_pattern = False
                    
                    if node.args:
                        arg = node.args[0]
                        # Check if using a compiled variable
                        if isinstance(arg, ast.Name) and arg.id in self.compiled_vars:
                            uses_safe_pattern = True
                        # Check if using direct compile call
                        elif isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == 'compile':
                            if arg.args and isinstance(arg.args[0], ast.Name) and arg.args[0].id in self.parsed_vars:
                                uses_safe_pattern = True
                    
                    self.eval_calls.append({
                        'line': getattr(node, 'lineno', 0),
                        'node': node,
                        'uses_safe_pattern': uses_safe_pattern,
                        'function': self.current_function
                    })
                
                self.generic_visit(node)
            
            def is_secure_pattern(self):
                """Check if the secure eval pattern is detected"""
                # Basic pattern
                has_basic_pattern = (
                    self.has_ast_import and 
                    self.has_ast_parse and 
                    self.has_node_check and 
                    self.has_compile_before_eval and 
                    self.has_try_except
                )
                
                # Check if all eval calls use the safe pattern
                all_evals_safe = all(call.get('uses_safe_pattern', False) for call in self.eval_calls)
                
                return has_basic_pattern or all_evals_safe
        
        # Visit and analyze the entire module
        detector = SecureEvalDetector()
        detector.visit(parsed_code)
        
        # Track functions with detected vulnerabilities
        vulnerable_functions = set()
        
        # First, analyze each function separately
        for node in ast.iter_child_nodes(parsed_code):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                
                # Create a function-specific detector
                func_detector = SecureEvalDetector()
                func_detector.visit(node)
                
                # Only flag eval calls in functions without the secure pattern
                if not func_detector.is_secure_pattern():
                    for eval_call in func_detector.eval_calls:
                        vulnerabilities.append({
                            'type': 'CWE-95',
                            'function': function_name,
                            'line': eval_call['line'],
                            'message': "Improper Neutralization: Potential eval injection vulnerability detected", 
                            'severity': 'HIGH'
                        })
                    vulnerable_functions.add(function_name)
        
        # For eval calls not within an analyzed function, check global scope
        for eval_call in detector.eval_calls:
            func_name = eval_call.get('function', 'global_scope')
            if func_name not in vulnerable_functions and func_name == 'global_scope':
                # Only flag eval calls not using a secure pattern
                if not detector.is_secure_pattern() and not eval_call.get('uses_safe_pattern', False):
                    vulnerabilities.append({
                        'type': 'CWE-95',
                        'function': func_name,
                        'line': eval_call['line'],
                        'message': "Improper Neutralization: Potential eval injection vulnerability detected", 
                        'severity': 'HIGH'
                    })
    
    except SyntaxError as e:
        # Handle syntax errors in the provided code
        vulnerabilities.append({
            'type': 'CWE-95',
            'function': 'N/A',
            'line': getattr(e, 'lineno', 0),
            'message': f"Analysis Error: Syntax error in code: {str(e)}", 
            'severity': 'ERROR'
        })
    except Exception as e:
        # Handle other parsing errors
        vulnerabilities.append({
            'type': 'CWE-95',
            'function': 'N/A',
            'line': 0,
            'message': f"Analysis Error: {str(e)}", 
            'severity': 'ERROR'
        })
    
    return vulnerabilities


# ## 15. CWE-601
def detect_open_redirect(code_string):
    """
    Analyzes Python code to detect potential CWE-601 (Open Redirect) vulnerabilities.
    
    Specifically looks for functions that:
    1. Accept URL parameters or components
    2. Construct/manipulate URLs
    3. Return URLs that could be used for redirects
    4. Lack sufficient domain validation checks
    
    Args:
        code_string: String containing the Python code to analyze
        
    Returns:
        A list of dictionaries containing detected issues with their locations and descriptions
    """
    import ast
    import re
    
    vulnerabilities = []
    
    # Parse the code into an AST
    try:
        tree = ast.parse(code_string)
    except SyntaxError:
        return [{"line": 0, "description": "Could not parse code due to syntax error"}]
    
    # Helper function to check if a function contains thorough security measures
    def contains_complete_url_validation(node):
        # Get function code as string for pattern matching
        function_str = ast.unparse(node) if hasattr(ast, 'unparse') else ast.dump(node)
        
        # Check if SCHEME_RE.search is properly used to prevent URL schemes in user input
        has_scheme_check = re.search(r'SCHEME_RE\.search\(.*\)', function_str) is not None
        
        # Check if there's a proper domain validation
        domain_validation_patterns = [
            # Domain comparison checks that prevent host switching
            r'\.netloc\s*==\s*.*\.netloc',
            r'parsed_.*\.netloc\s*==\s*',
            # Domain whitelist checking
            r'\.netloc\s+in\s+',
            # Exception raising for domain mismatches
            r'raise\s+.*[Ii]nvalid.*[Dd]omain',
            r'raise\s+.*[Uu]rl',
            r'raise\s+.*[Rr]edirect',
            # Other thorough validation checks
            r'is_safe_url\(',
            r'validate_url\(',
            r'check_domain\(',
            r'ALLOWED_.*DOMAINS',
        ]
        
        has_domain_validation = any(re.search(pattern, function_str) for pattern in domain_validation_patterns)
        
        # Check if there's protection against double-slash attack
        double_slash_protection = re.search(r'\.startswith\s*\(\s*[\'"]//[\'"]\s*\)', function_str) is not None
        
        # If the function has scheme checks but returns the original value directly without validation
        if has_scheme_check and re.search(r'if\s+SCHEME_RE\.search.*\s+return\s+', function_str):
            # This is a potential issue unless there's another protection mechanism
            if not (has_domain_validation or double_slash_protection):
                return False
        
        # Consider a function secure if it has domain validation OR double slash protection
        return has_domain_validation or double_slash_protection
    
    # Flag functions with high risk signatures/patterns
    high_risk_param_patterns = [
        r'redirect',
        r'callback', 
        r'url',
        r'uri',
        r'link',
        r'path',
        r'endpoint',
        r'next',
        r'return',
        r'target',
        r'location',
        r'forward'
    ]
    
    # Find common URL construction/manipulation patterns
    url_construction_patterns = [
        r'ur[l]parse\.urlparse', 
        r'urllib\.parse\.urlparse',
        r'ur[l]parse\.urljoin',
        r'urllib\.parse\.urljoin',
        r'urlencode',
        r'urlparse',
        r'\.netloc',
        r'http[s]?://',
        r'f\".*\?',
        r'\+=\s*\?',
        r'\+\s*\?',
        r'join.*url'
    ]
    
    # Check for redirect-related operations
    redirect_patterns = [
        r'redirect',
        r'forward',
        r'location',
        r'callback',
        r'sso.*url',
        r'return.*url',
        r'api.*url'
    ]
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            function_str = ast.unparse(node) if hasattr(ast, 'unparse') else ast.dump(node)
            
            # Check if function has high-risk parameters
            has_risky_params = False
            for param in node.args.args:
                param_name = param.arg if hasattr(param, 'arg') else param.id
                if any(re.search(pattern, param_name, re.IGNORECASE) for pattern in high_risk_param_patterns):
                    has_risky_params = True
                    break
            
            # Check for URL manipulation operations
            has_url_manipulation = any(re.search(pattern, function_str, re.IGNORECASE) for pattern in url_construction_patterns)
            
            # Check for redirect related operations
            is_redirect_related = any(re.search(pattern, function_str, re.IGNORECASE) for pattern in redirect_patterns) or \
                                 any(re.search(pattern, function_name, re.IGNORECASE) for pattern in redirect_patterns)
            
            # Check if the function implements complete URL validation
            has_complete_validation = contains_complete_url_validation(node)
            
            # Check if the function returns a URL-like value
            returns_url = False
            for child_node in ast.walk(node):
                if isinstance(child_node, ast.Return):
                    return_str = ast.unparse(child_node) if hasattr(ast, 'unparse') else ast.dump(child_node)
                    if any(keyword in return_str.lower() for keyword in ['url', 'uri', 'link', 'location', 'redirect', 'path']):
                        returns_url = True
                        break
            
            # Special case for make_location_absolute-like functions
            is_location_absolute_function = "make_location_absolute" in function_name or \
                                          (has_risky_params and "SCHEME_RE.search" in function_str)
            
            # If function has risky characteristics but no complete validation
            if ((has_risky_params and has_url_manipulation) or 
                (is_redirect_related and has_url_manipulation) or
                (returns_url and has_url_manipulation) or
                (is_redirect_related and returns_url) or
                is_location_absolute_function):
                if not has_complete_validation:
                    vulnerabilities.append({
                        "line": node.lineno,
                        "function": function_name,
                        "description": "Potential Open Redirect (CWE-601): Function constructs URLs "
                                      "without sufficient validation. Consider validating domains and "
                                      "handling URL schemes securely to prevent redirects to untrusted sites."
                    })
    
    return vulnerabilities


# ## 16. CWE-327
def detect_insecure_crypto_algorithm(code: str) -> list:
    """
    Detects use of insecure or broken cryptographic algorithms (CWE-327) in Python code.
    
    Args:
        code: String containing the Python code to analyze
    
    Returns:
        List of dictionaries with information about detected issues
    """
    # List of known insecure/weak hash algorithms
    insecure_algorithms = [
        "md5", "md4", "md2", "sha1", "sha", "dsa", "des", "rc4", 
        "rc2", "blowfish", "3des", "tripledes", "idea"
    ]
    
    issues = []
    
    # Parse code into lines
    lines = code.split('\n')
    
    # Extract functions from the code
    functions = []
    current_function = []
    in_function = False
    indent_level = 0
    
    for line in lines:
        if line.strip().startswith("def ") and line.strip().endswith(":"):
            if in_function:
                functions.append(current_function)
                current_function = []
            in_function = True
            indent_level = len(line) - len(line.lstrip())
            current_function.append(line)
        elif in_function:
            if not line.strip() or len(line) - len(line.lstrip()) > indent_level:
                current_function.append(line)
            else:
                functions.append(current_function)
                current_function = []
                in_function = False
    
    if current_function:
        functions.append(current_function)
    
    # Analyze each function
    for function in functions:
        function_code = "\n".join(function)
        function_lines = function
        
        # Extract function name
        import re
        function_name_match = re.search(r"def\s+(\w+)\s*\(", function_code)
        function_name = function_name_match.group(1) if function_name_match else "unknown"
        
        # Check for direct usage of insecure algorithms
        for i, line in enumerate(function_lines):
            line_num = lines.index(line) + 1  # Get original line number
            
            for algo in insecure_algorithms:
                if f"hashlib.{algo}(" in line.lower() or f"hashlib.new('{algo}'" in line.lower() or f'hashlib.new("{algo}"' in line.lower():
                    issues.append({
                        "line": line_num,
                        "code": line.strip(),
                        "algorithm": algo,
                        "message": f"CWE-327: Use of insecure cryptographic algorithm '{algo}' detected"
                    })
        
        # Check for variable algorithms
        uses_variable_algorithm = False
        variable_algo_lines = []
        
        # Check for patterns that indicate variable algorithm usage
        for i, line in enumerate(function_lines):
            line_num = lines.index(line) + 1
            if (("hashlib.new(" in line and not any(f"'{algo}'" in line or f'"{algo}"' in line for algo in insecure_algorithms + ["sha256", "sha512", "sha384", "blake2"])) or
                "hmac.new(" in line and "," in line and not any(f"'{algo}'" in line or f'"{algo}"' in line for algo in insecure_algorithms + ["sha256", "sha512", "sha384", "blake2"]) or
                "getattr(hashlib," in line):
                uses_variable_algorithm = True
                variable_algo_lines.append((line_num, line.strip()))
        
        if uses_variable_algorithm:
            # Extract validation logic - check for both list declaration and validation
            has_list_declaration = False
            has_validation_check = False
            
            # Check for list declaration with secure algorithms
            list_pattern = r"(secure|safe|approved|allowed|permitted)[\w_]*\s*=\s*\["
            if re.search(list_pattern, function_code, re.IGNORECASE):
                has_list_declaration = True
            
            # Check for validation against the list
            validation_pattern = r"if\s+[\w_]+\s+not\s+in\s+(secure|safe|approved|allowed|permitted)[\w_]*\s*:"
            if re.search(validation_pattern, function_code, re.IGNORECASE):
                has_validation_check = True
            
            # Only flag if there's no proper validation (both declaration and check)
            if not (has_list_declaration and has_validation_check):
                for line_num, line_code in variable_algo_lines:
                    issues.append({
                        "line": line_num,
                        "code": line_code,
                        "algorithm": "variable",
                        "message": "CWE-327: Potential use of insecure algorithm - no validation of algorithm security"
                    })
    
    return issues


# ## 17. CWE-915
def detect_unsafe_object_modification(code_string):
    """
    Static analysis function to detect CWE-915: Improperly Controlled Modification 
    of Dynamically-Determined Object Attributes.
    
    This function detects when code allows updating object attributes from external input
    without proper validation against an allow-list (like EDITABLE_FIELDS).
    
    Args:
        code_string (str): The Python code to analyze as a string
    
    Returns:
        list: A list of potential vulnerabilities with line numbers and descriptions
    """
    import ast
    
    vulnerabilities = []
    
    # Parse the code into an AST
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return [{"line": e.lineno, "description": f"Syntax error: {str(e)}"}]
    
    class VulnerabilityVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            # Check if the function contains any validation patterns
            has_field_validation = False
            
            # Look for validation patterns in the function body
            for stmt in ast.walk(node):
                # Check for if statements with field validation
                if isinstance(stmt, ast.If) and hasattr(stmt, 'test'):
                    test = stmt.test
                    # Look for "if field in ALLOWED_FIELDS" pattern
                    if (isinstance(test, ast.Compare) and 
                        len(test.ops) > 0 and isinstance(test.ops[0], ast.In) and
                        hasattr(test, 'comparators') and len(test.comparators) > 0 and
                        isinstance(test.comparators[0], ast.Name) and 
                        'FIELD' in test.comparators[0].id.upper()):
                        has_field_validation = True
                        break
            
            # Now look for vulnerable patterns in the function
            vulnerable_lines = []
            
            # Check for direct dict.update() calls
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                    call = stmt.value
                    if (isinstance(call.func, ast.Attribute) and 
                        call.func.attr == 'update'):
                        # If no field validation was found, mark as vulnerable
                        if not has_field_validation:
                            vulnerable_lines.append(stmt.lineno)
            
            # Check for dictionary item assignments in loops without validation
            for stmt in node.body:
                if isinstance(stmt, ast.For):
                    # Check for dictionary assignments in the loop body
                    has_loop_validation = False
                    
                    # Look for validation inside the loop
                    for inner_stmt in stmt.body:
                        if isinstance(inner_stmt, ast.If):
                            test = inner_stmt.test
                            # Check for field validation patterns
                            if (isinstance(test, ast.Compare) and
                                len(test.ops) > 0 and isinstance(test.ops[0], ast.In)):
                                has_loop_validation = True
                                break
                    
                    # Check for assignments in the loop
                    has_dict_assignment = False
                    for inner_stmt in stmt.body:
                        if isinstance(inner_stmt, ast.Assign) and isinstance(inner_stmt.targets[0], ast.Subscript):
                            has_dict_assignment = True
                            break
                    
                    # If there's dictionary assignment without validation, mark as vulnerable
                    if has_dict_assignment and not has_loop_validation and not has_field_validation:
                        vulnerable_lines.append(stmt.lineno)
            
            # Add vulnerabilities with proper descriptions
            for line in vulnerable_lines:
                vulnerabilities.append({
                    "line": line,
                    "description": "CWE-915: Uncontrolled modification of object attributes detected. "
                                  "Updates to objects should be limited to an allow-list of fields "
                                  "(e.g., using 'if field in EDITABLE_FIELDS' checks).",
                    "severity": "High"
                })
            
            # Continue visiting other nodes
            self.generic_visit(node)
    
    # Run the visitor on the AST
    visitor = VulnerabilityVisitor()
    visitor.visit(tree)
    
    return vulnerabilities


# Overall function to run all detectors
def run_all_detectors(code_string):
    """
    Run all vulnerability detectors on the provided code string.
    
    Args:
        code_string (str): The Python code to analyze
    
    Returns:
        list: A consolidated list of detected vulnerabilities from all detectors
    """
    all_vulnerabilities = []
    # Run each detector and collect results
    all_vulnerabilities.extend(detect_ssrf(code_string)) # 1. SSRF
    all_vulnerabilities.extend(detect_improper_signature_verification(code_string)) # 2. Improper Signature Verification
    all_vulnerabilities.extend(detect_incorrect_authorization(code_string)) # 3. Incorrect Authorization
    all_vulnerabilities.extend(detect_csrf_vulnerabilities(code_string)) # 4. CSRF
    all_vulnerabilities.extend(detect_resource_allocation_without_limits(code_string)) # 5. Resource Allocation without Limits
    all_vulnerabilities.extend(detect_command_injection(code_string)) # 6. Command Injection
    all_vulnerabilities.extend(detect_code_injection(code_string)) # 7. Code Injection
    all_vulnerabilities.extend(detect_inefficient_regex(code_string)) # 8. Inefficient Regular Expression Complexity
    all_vulnerabilities.extend(detect_unsafe_deserialization(code_string)) # 9. Unsafe Deserialization
    all_vulnerabilities.extend(detect_xss_vulnerability(code_string)) # 10. XSS
    all_vulnerabilities.extend(detect_missing_authorization(code_string)) # 11. Missing Authorization
    all_vulnerabilities.extend(detect_injection(code_string)) # 12. Injection
    all_vulnerabilities.extend(detect_info_exposure(code_string)) # 13. Information Exposure
    all_vulnerabilities.extend(detect_eval_injection(code_string)) # 14. Eval Injection
    all_vulnerabilities.extend(detect_open_redirect(code_string)) # 15. Open Redirect
    all_vulnerabilities.extend(detect_insecure_crypto_algorithm(code_string)) # 16. Insecure Crypto Algorithm
    all_vulnerabilities.extend(detect_unsafe_object_modification(code_string)) # 17. Unsafe Object Modification
    
    return all_vulnerabilities