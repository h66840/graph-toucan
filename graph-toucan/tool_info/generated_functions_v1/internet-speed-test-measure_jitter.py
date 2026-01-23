from typing import Dict, Any, Optional
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for internet speed test jitter measurement.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - jitter (float): measured jitter value in milliseconds
        - unit (str): unit of the jitter measurement, typically "ms"
        - average_latency (float): average round-trip latency across all samples in milliseconds
        - samples (int): number of latency measurements taken to compute jitter
        - url (str): the URL used for the test
        - server_info_cdn_provider (str): CDN provider name
        - server_info_pop_code (str): POP location code
        - server_info_pop_location (str): POP physical location
        - server_info_cf_ray (str): Cloudflare Ray ID (if applicable)
    """
    return {
        "jitter": round(random.uniform(1.0, 50.0), 3),
        "unit": "ms",
        "average_latency": round(random.uniform(20.0, 200.0), 3),
        "samples": 10 if random.randint(1, 10) > 1 else 5,  # mostly 10, sometimes 5
        "url": "http://speedtest.example.com/ping",
        "server_info_cdn_provider": random.choice(["Cloudflare", "Akamai", "Fastly", "Amazon CloudFront"]),
        "server_info_pop_code": random.choice(["SFO", "LAX", "IAD", "AMS", "FRA", "SIN"]),
        "server_info_pop_location": random.choice([
            "San Francisco, CA, US",
            "Los Angeles, CA, US",
            "Washington, DC, US",
            "Amsterdam, NL",
            "Frankfurt, DE",
            "Singapore, SG"
        ]),
        "server_info_cf_ray": f"{random.randint(1000000, 9999999):07x}-SFO"
    }


def internet_speed_test_measure_jitter(samples: Optional[int] = None, url: Optional[str] = None) -> Dict[str, Any]:
    """
    Measures network jitter by simulating multiple latency samples.

    Jitter is calculated as the average of absolute differences between consecutive latency measurements.
    This function simulates an internet speed test that measures round-trip latency variations.

    Args:
        samples (Optional[int]): Number of latency samples to take. Default is 10 if not provided.
        url (Optional[str]): Target URL to ping. If not provided, a default speed test endpoint is used.

    Returns:
        Dict[str, Any] containing:
            - jitter (float): measured jitter value in milliseconds
            - unit (str): unit of the jitter measurement, typically "ms"
            - average_latency (float): average round-trip latency across all samples in milliseconds
            - samples (int): number of latency measurements taken to compute jitter
            - url (str): the URL used for the test
            - server_info (Dict): contains information about the server and CDN POP that responded,
              including 'cdn_provider', 'pop_code', 'pop_location', 'cf_ray', and other optional headers or network info

    Example:
        {
            "jitter": 4.5,
            "unit": "ms",
            "average_latency": 89.2,
            "samples": 10,
            "url": "http://speedtest.example.com/ping",
            "server_info": {
                "cdn_provider": "Cloudflare",
                "pop_code": "SFO",
                "pop_location": "San Francisco, CA, US",
                "cf_ray": "abc123456-SFO"
            }
        }
    """
    # Input validation
    if samples is not None:
        if not isinstance(samples, int):
            raise TypeError("samples must be an integer")
        if samples < 2:
            raise ValueError("samples must be at least 2 to calculate jitter")
        if samples > 100:
            raise ValueError("samples cannot exceed 100")

    if url is not None and not isinstance(url, str):
        raise TypeError("url must be a string")

    # Use default values if not provided
    effective_samples = samples if samples is not None else 10
    effective_url = url if url is not None else "http://speedtest.example.com/ping"

    # Call external API to get simulated test results
    api_data = call_external_api("internet-speed-test-measure_jitter")

    # Construct server_info dict from flattened fields
    server_info = {
        "cdn_provider": api_data["server_info_cdn_provider"],
        "pop_code": api_data["server_info_pop_code"],
        "pop_location": api_data["server_info_pop_location"],
        "cf_ray": api_data["server_info_cf_ray"]
    }

    # Build final result with proper nested structure
    result = {
        "jitter": api_data["jitter"],
        "unit": api_data["unit"],
        "average_latency": api_data["average_latency"],
        "samples": effective_samples,  # Use the actual requested/used sample count
        "url": effective_url,
        "server_info": server_info
    }

    return result