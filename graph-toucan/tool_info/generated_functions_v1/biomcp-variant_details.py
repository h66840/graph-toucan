from typing import Dict, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching variant data from external API (e.g., MyVariant.info).
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - variant_data_genomic_context (str): Genomic context description
        - variant_data_frequencies (str): Population frequencies as JSON string
        - variant_data_predictions (str): Functional predictions as JSON string
        - variant_data_clinical_annotations (str): Clinical significance data as JSON string
        - variant_data_source_links (str): Source URLs as JSON string
        - formatted_summary (str): Markdown-formatted summary of the variant
        - success (bool): Whether the query was successful
        - error_message (str): Error message if any, otherwise empty string
        - query_id (str): The variant ID used in the query
        - timestamp (str): ISO 8601 timestamp of response generation
        - source_api (str): Name of the source API (e.g., 'MyVariant.info')
    """
    return {
        "variant_data_genomic_context": "Chromosome 7, position 140453136, reference allele A, alternate allele T",
        "variant_data_frequencies": '{"gnomad_exome": {"all": {"af": 0.0002}}, "gnomad_genome": {"all": {"af": 0.0001}}}',
        "variant_data_predictions": '{"sift": {"score": 0.05, "prediction": "deleterious"}, "polyphen": {"score": 0.987, "prediction": "probably_damaging"}}',
        "variant_data_clinical_annotations": '{"clinvar": {"rcv": "RCV000012345", "clinical_significance": "Pathogenic", "conditions": "Cystic Fibrosis"}}',
        "variant_data_source_links": '{"myvariant": "https://myvariant.info/v1/variant/chr7:g.140453136A%3ET", "clinvar": "https://www.ncbi.nlm.nih.gov/clinvar/RCV000012345/"}',
        "formatted_summary": (
            "## Variant Summary: chr7:g.140453136A>T\n"
            "**Genomic Context:** Chromosome 7, position 140453136, A>T\n\n"
            "**Population Frequencies:**\n- gnomAD Exome: AF = 0.0002\n- gnomAD Genome: AF = 0.0001\n\n"
            "**Functional Predictions:**\n- SIFT: deleterious (score: 0.05)\n- PolyPhen: probably damaging (score: 0.987)\n\n"
            "**Clinical Significance:**\n- ClinVar: Pathogenic (RCV000012345)\n- Associated Condition: Cystic Fibrosis\n\n"
            "[MyVariant.info](https://myvariant.info/v1/variant/chr7:g.140453136A%3ET) | "
            "[ClinVar Entry](https://www.ncbi.nlm.nih.gov/clinvar/RCV000012345/)"
        ),
        "success": True,
        "error_message": "",
        "query_id": "chr7:g.140453136A>T",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source_api": "MyVariant.info"
    }

def biomcp_variant_details(call_benefit: str, variant_id: str) -> Dict[str, Any]:
    """
    Retrieves detailed information for a single genetic variant using simulated external API call.
    
    Parameters:
        call_benefit (str): Explanation of why this function is being called and the intended benefit.
        variant_id (str): A variant identifier in the format like "chr7:g.140453136A>T".
    
    Returns:
        Dict containing the following keys:
            - variant_data (Dict): Nested dictionary with genomic context, frequencies, predictions,
              clinical annotations, and source links.
            - formatted_summary (str): Markdown-formatted string summarizing the variant.
            - success (bool): True if the lookup was successful, False otherwise.
            - error_message (str): Description of error if any occurred; None if successful.
            - query_id (str): Echoed back the input variant_id for reference.
            - timestamp (str): ISO 8601 timestamp when the response was generated.
            - source_api (str): Identifier of the external service used.
    """
    # Input validation
    if not call_benefit.strip():
        return {
            "variant_data": {},
            "formatted_summary": "",
            "success": False,
            "error_message": "Parameter 'call_benefit' is required and cannot be empty.",
            "query_id": variant_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source_api": ""
        }
    
    if not variant_id.strip():
        return {
            "variant_data": {},
            "formatted_summary": "",
            "success": False,
            "error_message": "Parameter 'variant_id' is required and cannot be empty.",
            "query_id": variant_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source_api": ""
        }

    # Simulate external API call
    try:
        api_data = call_external_api("biomcp-variant_details")
    except Exception as e:
        return {
            "variant_data": {},
            "formatted_summary": "",
            "success": False,
            "error_message": f"Failed to retrieve data: {str(e)}",
            "query_id": variant_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source_api": ""
        }

    # Construct variant_data dictionary from flattened API response
    import json
    variant_data = {
        "genomic_context": api_data["variant_data_genomic_context"],
        "frequencies": json.loads(api_data["variant_data_frequencies"]),
        "predictions": json.loads(api_data["variant_data_predictions"]),
        "clinical_annotations": json.loads(api_data["variant_data_clinical_annotations"]),
        "source_links": json.loads(api_data["variant_data_source_links"])
    }

    # Build final result
    result = {
        "variant_data": variant_data,
        "formatted_summary": api_data["formatted_summary"],
        "success": api_data["success"],
        "error_message": api_data["error_message"] if api_data["error_message"] else None,
        "query_id": api_data["query_id"],
        "timestamp": api_data["timestamp"],
        "source_api": api_data["source_api"]
    }

    return result