from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Textract analysis.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - text_detections_0_id (int): ID of the first detected text element
        - text_detections_0_text (str): Text content of the first detection
        - text_detections_0_type (str): Type of detection (e.g., LINE or WORD)
        - text_detections_0_bounding_box_left (float): Left coordinate of bounding box
        - text_detections_0_bounding_box_top (float): Top coordinate of bounding box
        - text_detections_0_bounding_box_width (float): Width of bounding box
        - text_detections_0_bounding_box_height (float): Height of bounding box
        - text_detections_0_confidence (float): Confidence score of detection
        - text_detections_0_relationships (str): Relationships (e.g., child word IDs as comma-separated string)
        - pages (int): Total number of pages processed
        - metadata_request_id (str): Request ID from processing job
        - metadata_timestamp (str): Timestamp of processing job
        - metadata_api_version (str): API version used
        - metadata_input_file (str): Input file path
        - detected_languages_0_code (str): Detected language code (e.g., 'en')
        - detected_languages_0_confidence (float): Confidence of language detection
        - blocks_count_lines (int): Number of lines detected
        - blocks_count_words (int): Number of words detected
        - blocks_count_tables (int): Number of tables detected
        - blocks_count_cells (int): Number of cells detected
        - blocks_count_forms (int): Number of forms detected
        - blocks_count_key_values (int): Number of key-value pairs detected
        - tables_0_rows_count (int): Number of rows in the first table
        - tables_0_cells_count (int): Number of cells in the first table
        - tables_0_cell_0_text (str): Text of first cell in first table
        - tables_0_cell_0_row_index (int): Row index of first cell
        - tables_0_cell_0_col_index (int): Column index of first cell
        - form_fields_0_key (str): Key of first form field
        - form_fields_0_value (str): Value of first form field
        - form_fields_0_key_confidence (float): Confidence of key detection
        - form_fields_0_value_confidence (float): Confidence of value detection
        - form_fields_0_bounding_box_left (float): Left coordinate of form field bounding box
        - form_fields_0_bounding_box_top (float): Top coordinate of form field bounding box
        - form_fields_0_bounding_box_width (float): Width of form field bounding box
        - form_fields_0_bounding_box_height (float): Height of form field bounding box
        - processing_time_ms (float): Processing time in milliseconds
        - has_text (bool): Whether any readable text was found
    """
    return {
        "text_detections_0_id": 1,
        "text_detections_0_text": "Sample text from image",
        "text_detections_0_type": "LINE",
        "text_detections_0_bounding_box_left": 0.1,
        "text_detections_0_bounding_box_top": 0.2,
        "text_detections_0_bounding_box_width": 0.5,
        "text_detections_0_bounding_box_height": 0.05,
        "text_detections_0_confidence": 0.95,
        "text_detections_0_relationships": "2,3",
        "pages": 1,
        "metadata_request_id": "req-12345",
        "metadata_timestamp": "2023-10-01T12:00:00Z",
        "metadata_api_version": "1.0",
        "metadata_input_file": "/path/to/image.jpg",
        "detected_languages_0_code": "en",
        "detected_languages_0_confidence": 0.98,
        "blocks_count_lines": 10,
        "blocks_count_words": 50,
        "blocks_count_tables": 1,
        "blocks_count_cells": 8,
        "blocks_count_forms": 2,
        "blocks_count_key_values": 5,
        "tables_0_rows_count": 2,
        "tables_0_cells_count": 8,
        "tables_0_cell_0_text": "Header 1",
        "tables_0_cell_0_row_index": 0,
        "tables_0_cell_0_col_index": 0,
        "form_fields_0_key": "Name",
        "form_fields_0_value": "John Doe",
        "form_fields_0_key_confidence": 0.97,
        "form_fields_0_value_confidence": 0.96,
        "form_fields_0_bounding_box_left": 0.15,
        "form_fields_0_bounding_box_top": 0.3,
        "form_fields_0_bounding_box_width": 0.2,
        "form_fields_0_bounding_box_height": 0.04,
        "processing_time_ms": 125.5,
        "has_text": True,
    }

def ai_agent_with_mcp_Textract_Tool(filePath: str) -> Dict[str, Any]:
    """
    Sends an image to the Textract API for analysis.
    
    This function simulates calling an external Textract service to analyze an image
    and extract text, tables, forms, and other document elements. It returns structured
    results including detected text, metadata, language detection, block counts, tables,
    form fields, and processing statistics.
    
    Args:
        filePath (str): The local path to the image file to be uploaded. Must be a non-empty string.
    
    Returns:
        Dict containing the following keys:
        - text_detections (List[Dict]): List of detected text elements with bounding boxes, confidence scores, and relationships
        - pages (int): Total number of pages processed in the document
        - metadata (Dict): Information about the processing job including request_id, timestamp, api_version, and input_file
        - detected_languages (List[Dict]): List of detected languages with code and confidence
        - blocks_count (Dict): Counts of different block types detected
        - tables (List[Dict]): Structured representation of detected tables
        - form_fields (List[Dict]): Key-value pairs extracted from forms
        - processing_time_ms (float): Time taken by Textract API to process the image in milliseconds
        - has_text (bool): Whether any readable text was found in the image
    
    Raises:
        ValueError: If filePath is empty or not a string
        FileNotFoundError: If the file does not exist at the given path (simulated)
    """
    # Input validation
    if not isinstance(filePath, str):
        raise ValueError("filePath must be a string")
    if not filePath.strip():
        raise ValueError("filePath cannot be empty")
    
    # Simulate file existence check
    # In real implementation, this would check actual file system
    if "invalid" in filePath.lower() or "missing" in filePath.lower():
        raise FileNotFoundError(f"File not found: {filePath}")
    
    # Call external API (simulated)
    api_data = call_external_api("ai-agent-with-mcp-Textract Tool")
    
    # Construct text_detections list
    text_detections = [
        {
            "id": api_data["text_detections_0_id"],
            "text": api_data["text_detections_0_text"],
            "type": api_data["text_detections_0_type"],
            "bounding_box": {
                "left": api_data["text_detections_0_bounding_box_left"],
                "top": api_data["text_detections_0_bounding_box_top"],
                "width": api_data["text_detections_0_bounding_box_width"],
                "height": api_data["text_detections_0_bounding_box_height"],
            },
            "confidence": api_data["text_detections_0_confidence"],
            "relationships": api_data["text_detections_0_relationships"].split(",") if api_data["text_detections_0_relationships"] else [],
        }
    ]
    
    # Construct detected_languages list
    detected_languages = [
        {
            "code": api_data["detected_languages_0_code"],
            "confidence": api_data["detected_languages_0_confidence"],
        }
    ]
    
    # Construct blocks_count dict
    blocks_count = {
        "lines": api_data["blocks_count_lines"],
        "words": api_data["blocks_count_words"],
        "tables": api_data["blocks_count_tables"],
        "cells": api_data["blocks_count_cells"],
        "forms": api_data["blocks_count_forms"],
        "key_values": api_data["blocks_count_key_values"],
    }
    
    # Construct tables list
    tables = [
        {
            "rows": [
                {
                    "cells": [
                        {
                            "text": api_data["tables_0_cell_0_text"],
                            "row_index": api_data["tables_0_cell_0_row_index"],
                            "col_index": api_data["tables_0_cell_0_col_index"],
                            "bounding_box": None,  # Not available in flattened data
                            "confidence": None,     # Not available in flattened data
                        }
                    ]
                }
            ],
            "dimensions": {
                "rows": api_data["tables_0_rows_count"],
                "columns": api_data["tables_0_cells_count"] // api_data["tables_0_rows_count"] if api_data["tables_0_rows_count"] > 0 else 0,
            },
            "table_confidence": None  # Not available in flattened data
        }
    ]
    
    # Construct form_fields list
    form_fields = [
        {
            "key": api_data["form_fields_0_key"],
            "value": api_data["form_fields_0_value"],
            "key_confidence": api_data["form_fields_0_key_confidence"],
            "value_confidence": api_data["form_fields_0_value_confidence"],
            "bounding_box": {
                "left": api_data["form_fields_0_bounding_box_left"],
                "top": api_data["form_fields_0_bounding_box_top"],
                "width": api_data["form_fields_0_bounding_box_width"],
                "height": api_data["form_fields_0_bounding_box_height"],
            }
        }
    ]
    
    # Construct metadata dict
    metadata = {
        "request_id": api_data["metadata_request_id"],
        "timestamp": api_data["metadata_timestamp"],
        "api_version": api_data["metadata_api_version"],
        "input_file": api_data["metadata_input_file"],
    }
    
    # Construct final result
    result = {
        "text_detections": text_detections,
        "pages": api_data["pages"],
        "metadata": metadata,
        "detected_languages": detected_languages,
        "blocks_count": blocks_count,
        "tables": tables,
        "form_fields": form_fields,
        "processing_time_ms": api_data["processing_time_ms"],
        "has_text": api_data["has_text"],
    }
    
    return result