from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubChem substance details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - substance_id (int): PubChem Substance ID (SID) of the retrieved substance
        - source_name (str): Name of the data source that submitted the substance
        - deposited_date (str): Date when the substance was deposited into PubChem, in ISO format
        - record_title (str): Title or name of the substance record as provided by the depositor
        - molecular_formula (str): Molecular formula of the substance, if available
        - molecular_weight (float): Exact molecular weight of the substance
        - canonical_smiles (str): Canonical SMILES string representing the chemical structure
        - isomeric_smiles (str): Isomeric SMILES string with stereochemistry information
        - inchi (str): IUPAC International Chemical Identifier (InChI) string
        - inchi_key (str): Hashed version of InChI, used as a unique identifier
        - comment (str): Free-text comment or additional notes from the depositor about the substance
        - status (str): Current status of the substance record (e.g., 'active', 'retracted')
        - synonyms_0 (str): First alternate name or identifier
        - synonyms_1 (str): Second alternate name or identifier
        - components_0_molecular_formula (str): Molecular formula of first component
        - components_0_molecular_weight (float): Molecular weight of first component
        - components_0_cid (int): Compound ID of first component
        - components_0_charge (int): Charge of first component
        - components_1_molecular_formula (str): Molecular formula of second component
        - components_1_molecular_weight (float): Molecular weight of second component
        - components_1_cid (int): Compound ID of second component
        - components_1_charge (int): Charge of second component
        - related_compounds_0 (int): First associated PubChem Compound ID (CID)
        - related_compounds_1 (int): Second associated PubChem Compound ID (CID)
        - depositor_supplied_properties_0_property_name (str): Name of first depositor-supplied property
        - depositor_supplied_properties_0_value (str): Value of first depositor-supplied property
        - depositor_supplied_properties_0_units (str): Units of first depositor-supplied property
        - depositor_supplied_properties_1_property_name (str): Name of second depositor-supplied property
        - depositor_supplied_properties_1_value (str): Value of second depositor-supplied property
        - depositor_supplied_properties_1_units (str): Units of second depositor-supplied property
        - citations_0_title (str): Title of first scientific reference
        - citations_0_journal (str): Journal name of first scientific reference
        - citations_0_authors (str): Authors of first scientific reference
        - citations_0_year (int): Year of first scientific reference
        - citations_0_pubmed_id (str): PubMed ID of first scientific reference
        - citations_1_title (str): Title of second scientific reference
        - citations_1_journal (str): Journal name of second scientific reference
        - citations_1_authors (str): Authors of second scientific reference
        - citations_1_year (int): Year of second scientific reference
        - citations_1_pubmed_id (str): PubMed ID of second scientific reference
        - external_links_0_database_name (str): Name of first external database
        - external_links_0_url (str): URL to first external resource
        - external_links_1_database_name (str): Name of second external database
        - external_links_1_url (str): URL to second external resource
    """
    return {
        "substance_id": 123456,
        "source_name": "ChEMBL",
        "deposited_date": "2015-03-12",
        "record_title": "Aspirin",
        "molecular_formula": "C9H8O4",
        "molecular_weight": 180.157,
        "canonical_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "isomeric_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "inchi": "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
        "inchi_key": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
        "comment": "Common pain reliever and antipyretic",
        "status": "active",
        "synonyms_0": "Acetylsalicylic acid",
        "synonyms_1": "ASA",
        "components_0_molecular_formula": "C9H8O4",
        "components_0_molecular_weight": 180.157,
        "components_0_cid": 2244,
        "components_0_charge": 0,
        "components_1_molecular_formula": "H2O",
        "components_1_molecular_weight": 18.015,
        "components_1_cid": 962,
        "components_1_charge": 0,
        "related_compounds_0": 2244,
        "related_compounds_1": 962,
        "depositor_supplied_properties_0_property_name": "Bioactivity",
        "depositor_supplied_properties_0_value": "IC50 = 1.2 uM",
        "depositor_supplied_properties_0_units": "uM",
        "depositor_supplied_properties_1_property_name": "Solubility",
        "depositor_supplied_properties_1_value": "3 mg/mL",
        "depositor_supplied_properties_1_units": "mg/mL",
        "citations_0_title": "Mechanism of action of aspirin",
        "citations_0_journal": "Nature Reviews Drug Discovery",
        "citations_0_authors": "Smith J, Jones M",
        "citations_0_year": 2010,
        "citations_0_pubmed_id": "12345678",
        "citations_1_title": "Clinical applications of aspirin",
        "citations_1_journal": "The Lancet",
        "citations_1_authors": "Brown A, Green B",
        "citations_1_year": 2008,
        "citations_1_pubmed_id": "18765432",
        "external_links_0_database_name": "ChEMBL",
        "external_links_0_url": "https://www.ebi.ac.uk/chembl/compound/inspect/CHEMBL25",
        "external_links_1_database_name": "DrugBank",
        "external_links_1_url": "https://go.drugbank.com/drugs/DB00945"
    }

def pubchem_data_access_server_get_substance_details(sid: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific substance by its PubChem SID.
    
    Args:
        sid: PubChem Substance ID (SID)
        
    Returns:
        Dictionary with substance details including:
        - substance_id (int): PubChem Substance ID (SID) of the retrieved substance
        - source_name (str): Name of the data source that submitted the substance
        - deposited_date (str): Date when the substance was deposited into PubChem, in ISO format
        - record_title (str): Title or name of the substance record as provided by the depositor
        - molecular_formula (str): Molecular formula of the substance, if available
        - molecular_weight (float): Exact molecular weight of the substance
        - canonical_smiles (str): Canonical SMILES string representing the chemical structure
        - isomeric_smiles (str): Isomeric SMILES string with stereochemistry information
        - inchi (str): IUPAC International Chemical Identifier (InChI) string
        - inchi_key (str): Hashed version of InChI, used as a unique identifier
        - synonyms (List[str]): List of alternate names and identifiers for the substance
        - components (List[Dict]): List of component compounds in the substance; each dict contains 'molecular_formula', 'molecular_weight', 'cid', and 'charge'
        - related_compounds (List[int]): List of associated PubChem Compound IDs (CIDs) derived from this substance
        - depositor_supplied_properties (List[Dict]): List of key-value properties provided by the depositor; each has 'property_name', 'value', and 'units'
        - citations (List[Dict]): List of scientific references related to the substance; each includes 'title', 'journal', 'authors', 'year', and 'pubmed_id'
        - external_links (List[Dict]): List of URLs linking to external databases or resources; each has 'database_name' and 'url'
        - comment (str): Free-text comment or additional notes from the depositor about the substance
        - status (str): Current status of the substance record (e.g., 'active', 'retracted')
    """
    # Simulate calling external API
    raw_data = call_external_api("pubchem_data_access_server_get_substance_details")
    
    # Extract scalar fields directly
    result = {
        "substance_id": raw_data["substance_id"],
        "source_name": raw_data["source_name"],
        "deposited_date": raw_data["deposited_date"],
        "record_title": raw_data["record_title"],
        "molecular_formula": raw_data["molecular_formula"],
        "molecular_weight": raw_data["molecular_weight"],
        "canonical_smiles": raw_data["canonical_smiles"],
        "isomeric_smiles": raw_data["isomeric_smiles"],
        "inchi": raw_data["inchi"],
        "inchi_key": raw_data["inchi_key"],
        "comment": raw_data["comment"],
        "status": raw_data["status"]
    }
    
    # Process synonyms
    synonyms = []
    for i in range(2):
        key = f"synonyms_{i}"
        if key in raw_data and raw_data[key]:
            synonyms.append(raw_data[key])
    result["synonyms"] = synonyms
    
    # Process components
    components = []
    for i in range(2):
        formula_key = f"components_{i}_molecular_formula"
        weight_key = f"components_{i}_molecular_weight"
        cid_key = f"components_{i}_cid"
        charge_key = f"components_{i}_charge"
        if formula_key in raw_data and raw_data[formula_key]:
            components.append({
                "molecular_formula": raw_data[formula_key],
                "molecular_weight": raw_data[weight_key],
                "cid": raw_data[cid_key],
                "charge": raw_data[charge_key]
            })
    result["components"] = components
    
    # Process related compounds
    related_compounds = []
    for i in range(2):
        key = f"related_compounds_{i}"
        if key in raw_data and raw_data[key]:
            related_compounds.append(raw_data[key])
    result["related_compounds"] = related_compounds
    
    # Process depositor supplied properties
    depositor_supplied_properties = []
    for i in range(2):
        name_key = f"depositor_supplied_properties_{i}_property_name"
        value_key = f"depositor_supplied_properties_{i}_value"
        units_key = f"depositor_supplied_properties_{i}_units"
        if name_key in raw_data and raw_data[name_key]:
            depositor_supplied_properties.append({
                "property_name": raw_data[name_key],
                "value": raw_data[value_key],
                "units": raw_data[units_key]
            })
    result["depositor_supplied_properties"] = depositor_supplied_properties
    
    # Process citations
    citations = []
    for i in range(2):
        title_key = f"citations_{i}_title"
        journal_key = f"citations_{i}_journal"
        authors_key = f"citations_{i}_authors"
        year_key = f"citations_{i}_year"
        pubmed_key = f"citations_{i}_pubmed_id"
        if title_key in raw_data and raw_data[title_key]:
            citations.append({
                "title": raw_data[title_key],
                "journal": raw_data[journal_key],
                "authors": raw_data[authors_key],
                "year": raw_data[year_key],
                "pubmed_id": raw_data[pubmed_key]
            })
    result["citations"] = citations
    
    # Process external links
    external_links = []
    for i in range(2):
        name_key = f"external_links_{i}_database_name"
        url_key = f"external_links_{i}_url"
        if name_key in raw_data and raw_data[name_key]:
            external_links.append({
                "database_name": raw_data[name_key],
                "url": raw_data[url_key]
            })
    result["external_links"] = external_links
    
    return result