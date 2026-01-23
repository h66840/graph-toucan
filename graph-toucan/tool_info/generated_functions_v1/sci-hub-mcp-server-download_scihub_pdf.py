from typing import Dict, Any
import time
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Sci-Hub PDF download.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Whether the PDF download was successful
        - file_path (str): The local file system path where the PDF was saved
        - file_size (int): Size of the downloaded PDF in bytes
        - download_time_ms (int): Time taken to complete the download in milliseconds
        - status_code (int): HTTP status code received during the download attempt
        - error_message (str): Error description if the download failed; otherwise null
        - metadata_title (str): Extracted document title
        - metadata_authors (str): Extracted document authors (comma-separated)
        - metadata_doi (str): Document DOI
        - metadata_publication_date (str): Publication date in YYYY-MM-DD format
    """
    # Simulate random success/failure
    success = random.choice([True, True, True, False])  # 75% success rate
    status_code = 200 if success else random.choice([404, 500, 403])
    error_message = None if success else random.choice([
        "PDF not found on Sci-Hub", "Access denied", "Server error"
    ])
    file_size = random.randint(1024, 5 * 1024 * 1024) if success else 0
    download_time_ms = random.randint(200, 5000)
    file_path = "/tmp/downloaded_paper.pdf" if success else ""

    # Metadata (may be present even on partial success)
    metadata_title = "Advances in Machine Learning for Scientific Research" if success else ""
    metadata_authors = "Alice Johnson, Bob Smith, Carol Davis" if success else ""
    metadata_doi = "10.1038/s41586-023-00123-4" if success else ""
    metadata_publication_date = "2023-06-15" if success else ""

    return {
        "success": success,
        "file_path": file_path,
        "file_size": file_size,
        "download_time_ms": download_time_ms,
        "status_code": status_code,
        "error_message": error_message,
        "metadata_title": metadata_title,
        "metadata_authors": metadata_authors,
        "metadata_doi": metadata_doi,
        "metadata_publication_date": metadata_publication_date,
    }


def sci_hub_mcp_server_download_scihub_pdf(output_path: str, pdf_url: str) -> Dict[str, Any]:
    """
    Downloads a PDF from Sci-Hub using the provided URL and saves it to the specified output path.

    This function simulates interaction with an external Sci-Hub service to download academic papers.
    It returns detailed information about the download attempt, including success status, file metadata,
    and performance metrics.

    Args:
        output_path (str): The local file system path where the PDF should be saved.
        pdf_url (str): The URL of the PDF to download (e.g., DOI link or article URL).

    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - success (bool): Whether the PDF download was successful.
            - file_path (str): The local file system path where the PDF was saved.
            - file_size (int): Size of the downloaded PDF in bytes.
            - download_time_ms (int): Time taken to complete the download in milliseconds.
            - status_code (int): HTTP status code received during the download attempt.
            - error_message (str | None): Error description if the download failed; otherwise None.
            - metadata (Dict): Extracted document metadata such as title, authors, DOI, publication date.
                Contains keys: 'title', 'authors', 'doi', 'publication_date'

    Raises:
        ValueError: If output_path or pdf_url is empty or invalid.
        TypeError: If input parameters are not strings.
    """
    # Input validation
    if not isinstance(output_path, str) or not output_path.strip():
        raise ValueError("output_path must be a non-empty string")
    if not isinstance(pdf_url, str) or not pdf_url.strip():
        raise ValueError("pdf_url must be a non-empty string")

    output_path = output_path.strip()
    pdf_url = pdf_url.strip()

    # Simulate calling external API
    api_data = call_external_api("sci-hub-mcp-server-download_scihub_pdf")

    # Construct metadata dictionary from flattened API response
    metadata = {
        "title": api_data["metadata_title"] or None,
        "authors": api_data["metadata_authors"] or None,
        "doi": api_data["metadata_doi"] or None,
        "publication_date": api_data["metadata_publication_date"] or None,
    }

    # Build final result structure
    result = {
        "success": api_data["success"],
        "file_path": output_path if api_data["success"] else None,
        "file_size": api_data["file_size"] if api_data["success"] else 0,
        "download_time_ms": api_data["download_time_ms"],
        "status_code": api_data["status_code"],
        "error_message": api_data["error_message"] if not api_data["success"] else None,
        "metadata": metadata,
    }

    return result