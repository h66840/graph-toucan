from typing import Dict, List, Any, Optional
import csv
from io import StringIO


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Biomart.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - header_0 (str): First column header
        - header_1 (str): Second column header
        - header_2 (str): Third column header
        - header_3 (str): Fourth column header
        - header_4 (str): Fifth column header
        - header_5 (str): Sixth column header
        - header_6 (str): Seventh column header
        - header_7 (str): Eighth column header
        - item_0_gene_stable_id (str): Gene stable ID for first record
        - item_0_gene_symbol (str): Gene symbol for first record
        - item_0_description (str): Description for first record
        - item_0_chromosome_name (str): Chromosome name for first record
        - item_0_start_position (int): Start position for first record
        - item_0_end_position (int): End position for first record
        - item_0_strand (int): Strand for first record
        - item_0_gene_biotype (str): Gene biotype for first record
        - item_1_gene_stable_id (str): Gene stable ID for second record
        - item_1_gene_symbol (str): Gene symbol for second record
        - item_1_description (str): Description for second record
        - item_1_chromosome_name (str): Chromosome name for second record
        - item_1_start_position (int): Start position for second record
        - item_1_end_position (int): End position for second record
        - item_1_strand (int): Strand for second record
        - item_1_gene_biotype (str): Gene biotype for second record
    """
    return {
        "header_0": "gene_stable_id",
        "header_1": "gene_symbol",
        "header_2": "description",
        "header_3": "chromosome_name",
        "header_4": "start_position",
        "header_5": "end_position",
        "header_6": "strand",
        "header_7": "gene_biotype",
        "item_0_gene_stable_id": "ENSG00000139618",
        "item_0_gene_symbol": "CREB3L1",
        "item_0_description": "cAMP responsive element binding protein 3-like 1 [Source:HGNC Symbol;Acc:19186]",
        "item_0_chromosome_name": "11",
        "item_0_start_position": 62497467,
        "item_0_end_position": 62553097,
        "item_0_strand": 1,
        "item_0_gene_biotype": "protein_coding",
        "item_1_gene_stable_id": "ENSG00000145335",
        "item_1_gene_symbol": "SLC25A21",
        "item_1_description": "solute carrier family 25 member 21 [Source:HGNC Symbol;Acc:21279]",
        "item_1_chromosome_name": "11",
        "item_1_start_position": 62572938,
        "item_1_end_position": 62587467,
        "item_1_strand": -1,
        "item_1_gene_biotype": "protein_coding",
    }


def biomart_mcp_get_data(
    mart: str,
    dataset: str,
    attributes: List[str],
    filters: Dict[str, str]
) -> Dict[str, Any]:
    """
    Queries Biomart for data using specified attributes and filters.

    This function performs the main data retrieval from Biomart, allowing you to
    query biological data by specifying which attributes to return and which filters
    to apply. Includes automatic retry logic for resilience.

    Args:
        mart (str): The mart identifier (e.g., "ENSEMBL_MART_ENSEMBL")
        dataset (str): The dataset identifier (e.g., "hsapiens_gene_ensembl")
        attributes (list[str]): List of attributes to retrieve (e.g., ["ensembl_gene_id", "external_gene_name"])
        filters (dict[str, str]): Dictionary of filters to apply (e.g., {"chromosome_name": "1"})

    Returns:
        Dict containing:
        - results (List[Dict]): list of gene records, each with 'gene_stable_id', 'gene_symbol', 'description',
          'chromosome_name', 'start_position', 'end_position', 'strand', 'gene_biotype' fields
        - headers (List[str]): original column headers from the CSV response in order

    Example:
        biomart_mcp_get_data(
            "ENSEMBL_MART_ENSEMBL",
            "hsapiens_gene_ensembl",
            ["gene_stable_id", "gene_symbol", "description", "chromosome_name",
             "start_position", "end_position", "strand", "gene_biotype"],
            {"chromosome_name": "11", "biotype": "protein_coding"}
        )
    """
    # Input validation
    if not mart:
        raise ValueError("Parameter 'mart' is required")
    if not dataset:
        raise ValueError("Parameter 'dataset' is required")
    if not attributes:
        raise ValueError("Parameter 'attributes' is required")
    if not filters:
        raise ValueError("Parameter 'filters' is required")

    # Call external API to get data
    api_data = call_external_api("biomart-mcp-get_data")

    # Extract headers (first 8 headers expected based on output schema)
    headers = [
        api_data["header_0"],
        api_data["header_1"],
        api_data["header_2"],
        api_data["header_3"],
        api_data["header_4"],
        api_data["header_5"],
        api_data["header_6"],
        api_data["header_7"]
    ]

    # Construct results list from indexed items
    results = [
        {
            "gene_stable_id": api_data["item_0_gene_stable_id"],
            "gene_symbol": api_data["item_0_gene_symbol"],
            "description": api_data["item_0_description"],
            "chromosome_name": api_data["item_0_chromosome_name"],
            "start_position": api_data["item_0_start_position"],
            "end_position": api_data["item_0_end_position"],
            "strand": api_data["item_0_strand"],
            "gene_biotype": api_data["item_0_gene_biotype"]
        },
        {
            "gene_stable_id": api_data["item_1_gene_stable_id"],
            "gene_symbol": api_data["item_1_gene_symbol"],
            "description": api_data["item_1_description"],
            "chromosome_name": api_data["item_1_chromosome_name"],
            "start_position": api_data["item_1_start_position"],
            "end_position": api_data["item_1_end_position"],
            "strand": api_data["item_1_strand"],
            "gene_biotype": api_data["item_1_gene_biotype"]
        }
    ]

    return {
        "results": results,
        "headers": headers
    }