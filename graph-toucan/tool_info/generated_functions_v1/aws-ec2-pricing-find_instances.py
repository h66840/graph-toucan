from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching EC2 instance pricing data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - instance_0_Instance_Type (str): Instance type identifier
        - instance_0_Region (str): AWS region
        - instance_0_Platform (str): OS platform
        - instance_0_Tenancy (str): Instance tenancy
        - instance_0_Pricing_Model (str): Pricing model
        - instance_0_Effective_Price_per_hour_USD (float): Hourly price
        - instance_0_Effective_Price_per_month_USD (float): Monthly price
        - instance_0_Effective_Price_per_year_USD (float): Annual price
        - instance_0_CloudFix_RightSpend_Price_per_hour_USD (float): RightSpend hourly price
        - instance_0_CloudFix_RightSpend_Price_per_month_USD (float): RightSpend monthly price
        - instance_0_CloudFix_RightSpend_Price_per_year_USD (float): RightSpend annual price
        - instance_0_CloudFix_RightSpend_Upfront_Payment_USD (float): RightSpend upfront cost
        - instance_0_Current_Generation (bool): Whether instance is current gen
        - instance_0_Instance_Family (str): Instance family (e.g., m5)
        - instance_0_Physical_Processor (str): CPU type (e.g., Graviton)
        - instance_0_Clock_Speed_GHz (float): CPU clock speed
        - instance_0_Processor_Features (str): CPU features
        - instance_0_Enhanced_Networking_Supported (bool): Enhanced networking support
        - instance_0_vCPU_cores (int): Number of vCPUs
        - instance_0_Memory_GB (float): RAM in GB
        - instance_0_Ephemeral_Storage_GB (int): Ephemeral storage size
        - instance_0_Network_Performance_Mbps (int): Network performance
        - instance_0_Dedicated_EBS_Throughput_Mbps (int): EBS throughput
        - instance_0_GPU_cores (int): Number of GPU cores
        - instance_0_GPU_Memory_GB (int): GPU memory in GB
        - instance_1_Instance_Type (str): Second instance type
        - instance_1_Region (str): Second instance region
        - instance_1_Platform (str): Second instance platform
        - instance_1_Tenancy (str): Second instance tenancy
        - instance_1_Pricing_Model (str): Second instance pricing model
        - instance_1_Effective_Price_per_hour_USD (float): Second instance hourly price
        - instance_1_Effective_Price_per_month_USD (float): Second instance monthly price
        - instance_1_Effective_Price_per_year_USD (float): Second instance annual price
        - instance_1_CloudFix_RightSpend_Price_per_hour_USD (float): Second instance RightSpend hourly price
        - instance_1_CloudFix_RightSpend_Price_per_month_USD (float): Second instance RightSpend monthly price
        - instance_1_CloudFix_RightSpend_Price_per_year_USD (float): Second instance RightSpend annual price
        - instance_1_CloudFix_RightSpend_Upfront_Payment_USD (float): Second instance RightSpend upfront
        - instance_1_Current_Generation (bool): Second instance current gen status
        - instance_1_Instance_Family (str): Second instance family
        - instance_1_Physical_Processor (str): Second instance processor
        - instance_1_Clock_Speed_GHz (float): Second instance clock speed
        - instance_1_Processor_Features (str): Second instance processor features
        - instance_1_Enhanced_Networking_Supported (bool): Second instance enhanced networking
        - instance_1_vCPU_cores (int): Second instance vCPU count
        - instance_1_Memory_GB (float): Second instance RAM
        - instance_1_Ephemeral_Storage_GB (int): Second instance ephemeral storage
        - instance_1_Network_Performance_Mbps (int): Second instance network performance
        - instance_1_Dedicated_EBS_Throughput_Mbps (int): Second instance EBS throughput
        - instance_1_GPU_cores (int): Second instance GPU cores
        - instance_1_GPU_Memory_GB (int): Second instance GPU memory
    """
    return {
        "instance_0_Instance_Type": "m5.large",
        "instance_0_Region": "us-east-1",
        "instance_0_Platform": "Linux/UNIX",
        "instance_0_Tenancy": "Shared",
        "instance_0_Pricing_Model": "On Demand",
        "instance_0_Effective_Price_per_hour_USD": 0.096,
        "instance_0_Effective_Price_per_month_USD": 70.08,
        "instance_0_Effective_Price_per_year_USD": 840.96,
        "instance_0_CloudFix_RightSpend_Price_per_hour_USD": 0.0672,
        "instance_0_CloudFix_RightSpend_Price_per_month_USD": 49.06,
        "instance_0_CloudFix_RightSpend_Price_per_year_USD": 588.67,
        "instance_0_CloudFix_RightSpend_Upfront_Payment_USD": 0.0,
        "instance_0_Current_Generation": True,
        "instance_0_Instance_Family": "m5",
        "instance_0_Physical_Processor": "Xeon",
        "instance_0_Clock_Speed_GHz": 3.1,
        "instance_0_Processor_Features": "Intel AVX, Intel AVX2, Intel AVX512, Intel Turbo",
        "instance_0_Enhanced_Networking_Supported": True,
        "instance_0_vCPU_cores": 2,
        "instance_0_Memory_GB": 8.0,
        "instance_0_Ephemeral_Storage_GB": 0,
        "instance_0_Network_Performance_Mbps": 4500,
        "instance_0_Dedicated_EBS_Throughput_Mbps": 4625,
        "instance_0_GPU_cores": 0,
        "instance_0_GPU_Memory_GB": 0,
        
        "instance_1_Instance_Type": "c6g.xlarge",
        "instance_1_Region": "us-east-1",
        "instance_1_Platform": "Linux/UNIX",
        "instance_1_Tenancy": "Shared",
        "instance_1_Pricing_Model": "On Demand",
        "instance_1_Effective_Price_per_hour_USD": 0.085,
        "instance_1_Effective_Price_per_month_USD": 62.05,
        "instance_1_Effective_Price_per_year_USD": 744.60,
        "instance_1_CloudFix_RightSpend_Price_per_hour_USD": 0.0595,
        "instance_1_CloudFix_RightSpend_Price_per_month_USD": 43.44,
        "instance_1_CloudFix_RightSpend_Price_per_year_USD": 521.22,
        "instance_1_CloudFix_RightSpend_Upfront_Payment_USD": 0.0,
        "instance_1_Current_Generation": True,
        "instance_1_Instance_Family": "c6g",
        "instance_1_Physical_Processor": "Graviton",
        "instance_1_Clock_Speed_GHz": 2.5,
        "instance_1_Processor_Features": "AWS Graviton2 Processor",
        "instance_1_Enhanced_Networking_Supported": True,
        "instance_1_vCPU_cores": 4,
        "instance_1_Memory_GB": 8.0,
        "instance_1_Ephemeral_Storage_GB": 0,
        "instance_1_Network_Performance_Mbps": 10000,
        "instance_1_Dedicated_EBS_Throughput_Mbps": 4750,
        "instance_1_GPU_cores": 0,
        "instance_1_GPU_Memory_GB": 0,
    }

def aws_ec2_pricing_find_instances(
    filter_family: Optional[str] = None,
    filter_max_price_per_hour: Optional[float] = None,
    filter_min_cpu_ghz: Optional[float] = None,
    filter_min_ebs_throughput: Optional[int] = None,
    filter_min_gpu: Optional[int] = None,
    filter_min_gpu_memory: Optional[int] = None,
    filter_min_network_performance: Optional[int] = None,
    filter_min_ram: Optional[float] = None,
    filter_min_vcpu: Optional[int] = None,
    filter_platform: Optional[str] = None,
    filter_pricing_model: Optional[str] = None,
    filter_processor: Optional[str] = None,
    filter_region: Optional[str] = None,
    filter_size: Optional[str] = None,
    page_num: Optional[int] = 0,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None
):
    pass