from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for NASA Earthdata granule search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_meta_concept_id (str): Concept ID for first granule
        - result_0_meta_revision_id (int): Revision ID for first granule
        - result_0_meta_format (str): Metadata format for first granule
        - result_0_meta_revision_date (str): Revision date in ISO 8601 for first granule
        - result_0_meta_provider_id (str): Provider ID for first granule
        - result_0_meta_concept_type (str): Concept type (always 'granule')
        - result_0_umm_temporal_extent_begin (str): Beginning datetime for first granule
        - result_0_umm_temporal_extent_end (str): Ending datetime for first granule
        - result_0_umm_granule_ur (str): Granule UR for first granule
        - result_0_umm_spatial_west (float): West bounding coordinate for first granule
        - result_0_umm_spatial_east (float): East bounding coordinate for first granule
        - result_0_umm_spatial_south (float): South bounding coordinate for first granule
        - result_0_umm_spatial_north (float): North bounding coordinate for first granule
        - result_0_umm_collection_short_name (str): Short name of collection for first granule
        - result_0_umm_collection_version (str): Version of collection for first granule
        - result_0_umm_data_granule_name (str): Filename for first granule
        - result_0_umm_data_granule_size_bytes (int): Size in bytes for first granule
        - result_0_umm_data_granule_size_mb (float): Size in MB for first granule
        - result_0_umm_data_granule_checksum_algorithm (str): Checksum algorithm for first granule
        - result_0_umm_data_granule_checksum_value (str): Checksum value for first granule
        - result_0_umm_data_granule_production_date (str): Production datetime for first granule
        - result_0_umm_data_granule_day_night_flag (str): Day/night flag for first granule
        - result_0_umm_related_url_0_url (str): First related URL for first granule
        - result_0_umm_related_url_0_type (str): Type of first related URL for first granule
        - result_0_umm_related_url_0_subtype (str): Subtype of first related URL for first granule
        - result_0_umm_related_url_0_description (str): Description of first related URL for first granule
        - result_0_umm_provider_date_insert (str): Insert date for first granule
        - result_0_umm_provider_date_update (str): Update date for first granule
        - result_0_umm_metadata_spec_name (str): Metadata spec name for first granule
        - result_0_umm_metadata_spec_version (str): Metadata spec version for first granule
        - result_0_umm_metadata_spec_url (str): Metadata spec URL for first granule
        - result_0_size (float): Total size in MB for first granule
        - result_1_meta_concept_id (str): Concept ID for second granule
        - result_1_meta_revision_id (int): Revision ID for second granule
        - result_1_meta_format (str): Metadata format for second granule
        - result_1_meta_revision_date (str): Revision date in ISO 8601 for second granule
        - result_1_meta_provider_id (str): Provider ID for second granule
        - result_1_meta_concept_type (str): Concept type (always 'granule')
        - result_1_umm_temporal_extent_begin (str): Beginning datetime for second granule
        - result_1_umm_temporal_extent_end (str): Ending datetime for second granule
        - result_1_umm_granule_ur (str): Granule UR for second granule
        - result_1_umm_spatial_west (float): West bounding coordinate for second granule
        - result_1_umm_spatial_east (float): East bounding coordinate for second granule
        - result_1_umm_spatial_south (float): South bounding coordinate for second granule
        - result_1_umm_spatial_north (float): North bounding coordinate for second granule
        - result_1_umm_collection_short_name (str): Short name of collection for second granule
        - result_1_umm_collection_version (str): Version of collection for second granule
        - result_1_umm_data_granule_name (str): Filename for second granule
        - result_1_umm_data_granule_size_bytes (int): Size in bytes for second granule
        - result_1_umm_data_granule_size_mb (float): Size in MB for second granule
        - result_1_umm_data_granule_checksum_algorithm (str): Checksum algorithm for second granule
        - result_1_umm_data_granule_checksum_value (str): Checksum value for second granule
        - result_1_umm_data_granule_production_date (str): Production datetime for second granule
        - result_1_umm_data_granule_day_night_flag (str): Day/night flag for second granule
        - result_1_umm_related_url_0_url (str): First related URL for second granule
        - result_1_umm_related_url_0_type (str): Type of first related URL for second granule
        - result_1_umm_related_url_0_subtype (str): Subtype of first related URL for second granule
        - result_1_umm_related_url_0_description (str): Description of first related URL for second granule
        - result_1_umm_provider_date_insert (str): Insert date for second granule
        - result_1_umm_provider_date_update (str): Update date for second granule
        - result_1_umm_metadata_spec_name (str): Metadata spec name for second granule
        - result_1_umm_metadata_spec_version (str): Metadata spec version for second granule
        - result_1_umm_metadata_spec_url (str): Metadata spec URL for second granule
        - result_1_size (float): Total size in MB for second granule
    """
    # Generate deterministic but realistic values based on tool name
    random.seed(tool_name.__hash__() % (2**32))
    
    def earthdata_mcp_server_search_earth_datagranules(start_year: int = 2020) -> str:
        dt = datetime(
            year=random.randint(start_year, 2023),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        return dt.isoformat() + "Z"
    
    def random_checksum() -> str:
        return ''.join(random.choices(string.hexdigits.lower(), k=32))
    
    def random_provider_id() -> str:
        providers = ["POCLOUD", "OB_CLOUD", "NSIDC", "LPDAAC", "GES_DISC"]
        return random.choice(providers)
    
    result = {
        # Result 0
        "result_0_meta_concept_id": f"G{random.randint(1000000, 9999999)}.POCLOUD",
        "result_0_meta_revision_id": random.randint(1, 5),
        "result_0_meta_format": "application/vnd.nasa.cmr.umm+json",
        "result_0_meta_revision_date": random_datetime(),
        "result_0_meta_provider_id": random_provider_id(),
        "result_0_meta_concept_type": "granule",
        "result_0_umm_temporal_extent_begin": random_datetime(2022),
        "result_0_umm_temporal_extent_end": random_datetime(2022),
        "result_0_umm_granule_ur": f"MYD09GQ.A{random.randint(2022001, 2022365)}.{random.randint(0, 23):02d}{random.randint(0, 59):02d}.061.{random.randint(1000000000, 9999999999)}.hdf",
        "result_0_umm_spatial_west": round(random.uniform(-180, 0), 6),
        "result_0_umm_spatial_east": round(random.uniform(0, 180), 6),
        "result_0_umm_spatial_south": round(random.uniform(-90, 0), 6),
        "result_0_umm_spatial_north": round(random.uniform(0, 90), 6),
        "result_0_umm_collection_short_name": "MYD09GQ",
        "result_0_umm_collection_version": "061",
        "result_0_umm_data_granule_name": f"MYD09GQ.A{random.randint(2022001, 2022365)}.{random.randint(0, 23):02d}{random.randint(0, 59):02d}.061.{random.randint(1000000000, 9999999999)}.hdf",
        "result_0_umm_data_granule_size_bytes": random.randint(1000000, 5000000),
        "result_0_umm_data_granule_size_mb": round(random.uniform(1.0, 5.0), 2),
        "result_0_umm_data_granule_checksum_algorithm": "MD5",
        "result_0_umm_data_granule_checksum_value": random_checksum(),
        "result_0_umm_data_granule_production_date": random_datetime(),
        "result_0_umm_data_granule_day_night_flag": random.choice(["DAY", "NIGHT"]),
        "result_0_umm_related_url_0_url": "https://example.com/data/MYD09GQ",
        "result_0_umm_related_url_0_type": "DOWNLOAD",
        "result_0_umm_related_url_0_subtype": "DIRECT DOWNLOAD",
        "result_0_umm_related_url_0_description": "Direct download link for granule",
        "result_0_umm_provider_date_insert": random_datetime(),
        "result_0_umm_provider_date_update": random_datetime(),
        "result_0_umm_metadata_spec_name": "UMM-G",
        "result_0_umm_metadata_spec_version": "1.6.4",
        "result_0_umm_metadata_spec_url": "https://example.com/umm-g/v1.6.4",
        "result_0_size": round(random.uniform(1.0, 5.0), 2),
        
        # Result 1
        "result_1_meta_concept_id": f"G{random.randint(1000000, 9999999)}.POCLOUD",
        "result_1_meta_revision_id": random.randint(1, 5),
        "result_1_meta_format": "application/vnd.nasa.cmr.umm+json",
        "result_1_meta_revision_date": random_datetime(),
        "result_1_meta_provider_id": random_provider_id(),
        "result_1_meta_concept_type": "granule",
        "result_1_umm_temporal_extent_begin": random_datetime(2022),
        "result_1_umm_temporal_extent_end": random_datetime(2022),
        "result_1_umm_granule_ur": f"MYD09GQ.A{random.randint(2022001, 2022365)}.{random.randint(0, 23):02d}{random.randint(0, 59):02d}.061.{random.randint(1000000000, 9999999999)}.hdf",
        "result_1_umm_spatial_west": round(random.uniform(-180, 0), 6),
        "result_1_umm_spatial_east": round(random.uniform(0, 180), 6),
        "result_1_umm_spatial_south": round(random.uniform(-90, 0), 6),
        "result_1_umm_spatial_north": round(random.uniform(0, 90), 6),
        "result_1_umm_collection_short_name": "MYD09GQ",
        "result_1_umm_collection_version": "061",
        "result_1_umm_data_granule_name": f"MYD09GQ.A{random.randint(2022001, 2022365)}.{random.randint(0, 23):02d}{random.randint(0, 59):02d}.061.{random.randint(1000000000, 9999999999)}.hdf",
        "result_1_umm_data_granule_size_bytes": random.randint(1000000, 5000000),
        "result_1_umm_data_granule_size_mb": round(random.uniform(1.0, 5.0), 2),
        "result_1_umm_data_granule_checksum_algorithm": "MD5",
        "result_1_umm_data_granule_checksum_value": random_checksum(),
        "result_1_umm_data_granule_production_date": random_datetime(),
        "result_1_umm_data_granule_day_night_flag": random.choice(["DAY", "NIGHT"]),
        "result_1_umm_related_url_0_url": "https://example.com/data/MYD09GQ",
        "result_1_umm_related_url_0_type": "DOWNLOAD",
        "result_1_umm_related_url_0_subtype": "DIRECT DOWNLOAD",
        "result_1_umm_related_url_0_description": "Direct download link for granule",
        "result_1_umm_provider_date_insert": random_datetime(),
        "result_1_umm_provider_date_update": random_datetime(),
        "result_1_umm_metadata_spec_name": "UMM-G",
        "result_1_umm_metadata_spec_version": "1.6.4",
        "result_1_umm_metadata_spec_url": "https://example.com/umm-g/v1.6.4",
        "result_1_size": round(random.uniform(1.0, 5.0), 2),
    }
    
    return result