from typing import Dict, List, Any, Optional
import time
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
import html

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for xpath-server-xpath tool.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_value (str): Text content of first matched node
        - result_0_path (str): Full XPath to first matched node
        - result_0_attributes_json (str): JSON string of attributes for first node
        - result_1_value (str): Text content of second matched node
        - result_1_path (str): Full XPath to second matched node
        - result_1_attributes_json (str): JSON string of attributes for second node
        - count (int): Total number of matched nodes
        - has_results (bool): Whether any nodes were found
        - query_valid (bool): Whether the XPath query was valid
        - execution_time_ms (float): Time taken to execute query in milliseconds
        - parsed_mime_type (str): Effective MIME type used for parsing
    """
    return {
        "result_0_value": "John Doe",
        "result_0_path": "/root/person/name",
        "result_0_attributes_json": '{"id": "1", "type": "employee"}',
        "result_1_value": "jane@example.com",
        "result_1_path": "/root/person/email",
        "result_1_attributes_json": '{"priority": "high"}',
        "count": 2,
        "has_results": True,
        "query_valid": True,
        "execution_time_ms": 12.5,
        "parsed_mime_type": "text/xml"
    }

def xpath_server_xpath(mimeType: Optional[str] = None, query: str = "", xml: str = "") -> Dict[str, Any]:
    """
    Select and query XML content using XPath.
    
    Args:
        mimeType (Optional[str]): The MIME type (e.g. text/xml, application/xml, text/html, application/xhtml+xml)
        query (str): The XPath query to execute (required)
        xml (str): The XML content to query (required)
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries representing matched XML nodes.
          Each dictionary contains 'value' (text content), 'attributes' (dict), and 'path' (str).
        - count (int): Total number of nodes matched.
        - has_results (bool): Whether any nodes were found.
        - metadata (Dict): Additional info including 'query_valid', 'execution_time_ms', 'parsed_mime_type'.
    
    Raises:
        ValueError: If query or xml is empty
    """
    if not query:
        raise ValueError("Parameter 'query' is required")
    if not xml:
        raise ValueError("Parameter 'xml' is required")
    
    start_time = time.time()
    
    # Determine MIME type
    parsed_mime_type = mimeType or "text/xml"
    if "html" in parsed_mime_type:
        # For HTML content, we'll use a more forgiving parser
        try:
            # Simple HTML to XML conversion for basic parsing
            xml_content = f"<root>{xml}</root>"
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            # Fallback: escape and wrap
            escaped_xml = html.escape(xml)
            xml_content = f"<root>{escaped_xml}</root>"
            root = ET.fromstring(xml_content)
    else:
        # Standard XML parsing
        try:
            root = ET.fromstring(xml.strip())
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML content: {str(e)}")
    
    try:
        # Execute XPath query
        # Note: ElementTree has limited XPath support
        # We'll handle basic cases
        matched_elements = root.findall(query) if query.startswith(".") or "/" in query else root.findall(f".//{query}")
        
        # Simulate external API call to get "real" results
        api_data = call_external_api("xpath-server-xpath")
        
        # Construct results from API data
        results = []
        for i in range(2):  # We know we have 2 results from call_external_api
            value_key = f"result_{i}_value"
            path_key = f"result_{i}_path"
            attr_key = f"result_{i}_attributes_json"
            
            if value_key in api_data and path_key in api_data and attr_key in api_data:
                try:
                    import json
                    attributes = json.loads(api_data[attr_key])
                except:
                    attributes = {}
                    
                results.append({
                    "value": api_data[value_key],
                    "path": api_data[path_key],
                    "attributes": attributes
                })
        
        count = api_data["count"]
        has_results = api_data["has_results"]
        query_valid = api_data["query_valid"]
        execution_time_ms = api_data["execution_time_ms"]
        
    except Exception as e:
        # Fallback: create minimal valid response
        results = []
        count = 0
        has_results = False
        query_valid = False
        execution_time_ms = (time.time() - start_time) * 1000
        parsed_mime_type = mimeType or "text/xml"
    
    # Final execution time
    if 'execution_time_ms' not in locals():
        execution_time_ms = (time.time() - start_time) * 1000
    
    metadata = {
        "query_valid": query_valid,
        "execution_time_ms": execution_time_ms,
        "parsed_mime_type": parsed_mime_type
    }
    
    return {
        "results": results,
        "count": count,
        "has_results": has_results,
        "metadata": metadata
    }