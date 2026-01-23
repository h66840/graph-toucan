from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for variant search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - variant_0_id (str): Genomic identifier for the variant
        - variant_0_score (float): Score associated with the variant
        - variant_0_chrom (str): Chromosome number where the variant is located
        - variant_0_cadd_phred (float): CADD phred score
        - variant_0_cadd_license (str): CADD license information
        - variant_0_civic_id (int): CIViC variant ID
        - variant_0_civic_url (str): CIViC URL
        - variant_0_civic_open_cravat_url (str): CIViC OpenCRAVAT URL
        - variant_0_civic_license (str): CIViC license information
        - variant_0_clinvar_variant_id (int): ClinVar variant ID
        - variant_0_clinvar_url (str): ClinVar URL
        - variant_0_clinvar_license (str): ClinVar license
        - variant_0_clinvar_rcv_0_clinical_significance (str): Clinical significance from RCV submission
        - variant_0_cosmic_cosmic_id (str): COSMIC ID
        - variant_0_cosmic_url (str): COSMIC URL
        - variant_0_cosmic_license (str): COSMIC license
        - variant_0_dbnsfp_polyphen2_hdiv_pred_0 (str): PolyPhen-2 HDIV prediction
        - variant_0_dbnsfp_polyphen2_hdiv_score_0 (float): PolyPhen-2 HDIV score
        - variant_0_dbnsfp_sift_pred_0 (str): SIFT prediction
        - variant_0_dbnsfp_sift_score_0 (float): SIFT score
        - variant_0_dbnsfp_genename (str): Gene symbol
        - variant_0_dbnsfp_hgvsc_0 (str): cDNA notation (HGVS.c)
        - variant_0_dbnsfp_hgvsp_0 (str): Protein change notation (HGVS.p)
        - variant_0_dbsnp_rsid (str): dbSNP rsID
        - variant_0_dbsnp_url (str): dbSNP URL
        - variant_0_dbsnp_license (str): dbSNP license
        - variant_0_exac_af (float): ExAC allele frequency
        - variant_0_exac_license (str): ExAC license
        - variant_0_gnomad_exome_af (float): gnomAD exome allele frequency
        - variant_0_gnomad_exome_license (str): gnomAD exome license
        - variant_0_vcf_ref (str): Reference allele in VCF
        - variant_0_vcf_alt (str): Alternate allele in VCF
        - variant_0_vcf_position (int): Genomic position in VCF
        - variant_0_urls_ensembl (str): Ensembl browser URL
        - variant_0_urls_ucsc_genome_browser (str): UCSC Genome Browser URL
        - variant_0_urls_hgnc (str): HGNC URL
    """
    return {
        "variant_0_id": "chr7:140453136-A-T",
        "variant_0_score": 0.95,
        "variant_0_chrom": "7",
        "variant_0_cadd_phred": 28.4,
        "variant_0_cadd_license": "CC0",
        "variant_0_civic_id": 12345,
        "variant_0_civic_url": "https://civic.genome.wustl.edu/events/variants/12345",
        "variant_0_civic_open_cravat_url": "https://run.opencravat.org/webapps/civic/report/12345",
        "variant_0_civic_license": "CC BY 4.0",
        "variant_0_clinvar_variant_id": 67890,
        "variant_0_clinvar_url": "https://www.ncbi.nlm.nih.gov/clinvar/variation/67890/",
        "variant_0_clinvar_license": "public domain",
        "variant_0_clinvar_rcv_0_clinical_significance": "Pathogenic",
        "variant_0_cosmic_cosmic_id": "COSM12345",
        "variant_0_cosmic_url": "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=12345",
        "variant_0_cosmic_license": "CC BY 4.0",
        "variant_0_dbnsfp_polyphen2_hdiv_pred_0": "probably_damaging",
        "variant_0_dbnsfp_polyphen2_hdiv_score_0": 0.998,
        "variant_0_dbnsfp_sift_pred_0": "deleterious",
        "variant_0_dbnsfp_sift_score_0": 0.01,
        "variant_0_dbnsfp_genename": "BRAF",
        "variant_0_dbnsfp_hgvsc_0": "c.1799T>A",
        "variant_0_dbnsfp_hgvsp_0": "p.V600E",
        "variant_0_dbsnp_rsid": "rs113488022",
        "variant_0_dbsnp_url": "https://www.ncbi.nlm.nih.gov/snp/rs113488022",
        "variant_0_dbsnp_license": "public domain",
        "variant_0_exac_af": 0.00012,
        "variant_0_exac_license": "MIT",
        "variant_0_gnomad_exome_af": 0.00015,
        "variant_0_gnomad_exome_license": "MIT",
        "variant_0_vcf_ref": "A",
        "variant_0_vcf_alt": "T",
        "variant_0_vcf_position": 140453136,
        "variant_0_urls_ensembl": "https://www.ensembl.org/Homo_sapiens/Variation/Explore?v=rs113488022",
        "variant_0_urls_ucsc_genome_browser": "https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=chr7:140453136-140453136",
        "variant_0_urls_hgnc": "https://www.genenames.org/data/gene-symbol-report/#!/hgnc:1097",
    }

def biomcp_variant_searcher(
    call_benefit: str,
    gene: Optional[str] = None,
    hgvsp: Optional[str] = None,
    hgvsc: Optional[str] = None,
    rsid: Optional[str] = None,
    region: Optional[str] = None,
    significance: Optional[str] = None,
    max_frequency: Optional[float] = None,
    min_frequency: Optional[float] = None,
    cadd: Optional[float] = None,
    polyphen: Optional[str] = None,
    sift: Optional[str] = None,
    sources: Optional[str] = None,
    size: Optional[int] = 40,
    offset: Optional[int] = 0,
) -> Dict[str, Any]:
    """
    Searches for genetic variants based on specified criteria.
    
    This function simulates querying a genetic database to find variants matching
    the provided filters such as gene symbol, protein change, cDNA change, rsID,
    genomic region, clinical significance, frequency thresholds, and functional
    prediction scores.
    
    Parameters:
        call_benefit (str): Explanation of why this function is being called and the intended benefit.
        gene (str, optional): Gene symbol to search for (e.g. BRAF, TP53).
        hgvsp (str, optional): Protein change notation (e.g., p.V600E, p.Arg557His).
        hgvsc (str, optional): cDNA notation (e.g., c.1799T>A).
        rsid (str, optional): dbSNP rsID (e.g., rs113488022).
        region (str, optional): Genomic region as chr:start-end (e.g. chr1:12345-67890).
        significance (str, optional): ClinVar clinical significance.
        max_frequency (float, optional): Maximum population allele frequency threshold.
        min_frequency (float, optional): Minimum population allele frequency threshold.
        cadd (float, optional): Minimum CADD phred score.
        polyphen (str, optional): PolyPhen-2 prediction (e.g., 'probably_damaging').
        sift (str, optional): SIFT prediction (e.g., 'deleterious').
        sources (str, optional): Comma-separated list of data sources to include.
        size (int, optional): Number of results to return (default: 40).
        offset (int, optional): Result offset for pagination (default: 0).
    
    Returns:
        Dict containing a list of variant records with detailed annotations.
        Each variant includes:
        - id: genomic identifier
        - score: prioritization score
        - chrom: chromosome
        - cadd: CADD scores and metadata
        - civic: CIViC clinical interpretations
        - clinvar: ClinVar annotations including clinical significance
        - cosmic: COSMIC cancer mutation data
        - dbnsfp: Functional predictions (PolyPhen, SIFT), gene name, HGVS notations
        - dbsnp: dbSNP identifiers and links
        - exac: ExAC frequency data
        - gnomad_exome: gnomAD exome frequency data
        - vcf: VCF format details (ref, alt, position)
        - urls: External links (Ensembl, UCSC, HGNC)
    
    Raises:
        ValueError: If required parameter call_benefit is empty or None.
    """
    if not call_benefit.strip():
        raise ValueError("Parameter 'call_benefit' is required and cannot be empty.")

    # Validate size and offset
    if size is not None and size < 1:
        raise ValueError("Parameter 'size' must be a positive integer.")
    if offset is not None and offset < 0:
        raise ValueError("Parameter 'offset' must be non-negative.")

    # Simulate API call to get flattened data
    api_data = call_external_api("biomcp-variant_searcher")

    # Construct nested variant structure from flattened API data
    variant = {
        "id": api_data["variant_0_id"],
        "score": api_data["variant_0_score"],
        "chrom": api_data["variant_0_chrom"],
        "cadd": {
            "phred": api_data["variant_0_cadd_phred"],
            "license": api_data["variant_0_cadd_license"],
        },
        "civic": {
            "id": api_data["variant_0_civic_id"],
            "url": api_data["variant_0_civic_url"],
            "open_cravat_url": api_data["variant_0_civic_open_cravat_url"],
            "license": api_data["variant_0_civic_license"],
        },
        "clinvar": {
            "variant_id": api_data["variant_0_clinvar_variant_id"],
            "url": api_data["variant_0_clinvar_url"],
            "license": api_data["variant_0_clinvar_license"],
            "rcv": [
                {
                    "clinical_significance": api_data["variant_0_clinvar_rcv_0_clinical_significance"]
                }
            ],
        },
        "cosmic": {
            "cosmic_id": api_data["variant_0_cosmic_cosmic_id"],
            "url": api_data["variant_0_cosmic_url"],
            "license": api_data["variant_0_cosmic_license"],
        },
        "dbnsfp": {
            "polyphen2": {
                "hdiv": {
                    "pred": [api_data["variant_0_dbnsfp_polyphen2_hdiv_pred_0"]],
                    "score": [api_data["variant_0_dbnsfp_polyphen2_hdiv_score_0"]],
                }
            },
            "sift": {
                "pred": [api_data["variant_0_dbnsfp_sift_pred_0"]],
                "score": [api_data["variant_0_dbnsfp_sift_score_0"]],
            },
            "genename": api_data["variant_0_dbnsfp_genename"],
            "hgvsc": [api_data["variant_0_dbnsfp_hgvsc_0"]],
            "hgvsp": [api_data["variant_0_dbnsfp_hgvsp_0"]],
        },
        "dbsnp": {
            "rsid": api_data["variant_0_dbsnp_rsid"],
            "url": api_data["variant_0_dbsnp_url"],
            "license": api_data["variant_0_dbsnp_license"],
        },
        "exac": {
            "af": api_data["variant_0_exac_af"],
            "license": api_data["variant_0_exac_license"],
        },
        "gnomad_exome": {
            "af": api_data["variant_0_gnomad_exome_af"],
            "license": api_data["variant_0_gnomad_exome_license"],
        },
        "vcf": {
            "ref": api_data["variant_0_vcf_ref"],
            "alt": api_data["variant_0_vcf_alt"],
            "position": api_data["variant_0_vcf_position"],
        },
        "urls": {
            "ensembl": api_data["variant_0_urls_ensembl"],
            "ucsc_genome_browser": api_data["variant_0_urls_ucsc_genome_browser"],
            "hgnc": api_data["variant_0_urls_hgnc"],
        },
    }

    # Return list of variants (only one simulated result)
    return {"variants": [variant]}