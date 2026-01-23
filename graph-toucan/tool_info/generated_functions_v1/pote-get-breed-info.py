from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for dog breed information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): The name of the dog breed
        - summary (str): A brief overview of the breed's key traits and suitability as a companion
        - physical_characteristics_male_height_min (float): Minimum height for males in cm
        - physical_characteristics_male_height_max (float): Maximum height for males in cm
        - physical_characteristics_male_weight_min (float): Minimum weight for males in kg
        - physical_characteristics_male_weight_max (float): Maximum weight for males in kg
        - physical_characteristics_male_life_expectancy_min (int): Minimum life expectancy for males in years
        - physical_characteristics_male_life_expectancy_max (int): Maximum life expectancy for males in years
        - physical_characteristics_female_height_min (float): Minimum height for females in cm
        - physical_characteristics_female_height_max (float): Maximum height for females in cm
        - physical_characteristics_female_weight_min (float): Minimum weight for females in kg
        - physical_characteristics_female_weight_max (float): Maximum weight for females in kg
        - physical_characteristics_female_life_expectancy_min (int): Minimum life expectancy for females in years
        - physical_characteristics_female_life_expectancy_max (int): Maximum life expectancy for females in years
        - temperament_characteristics_affection_with_family (int): Rating for affection with family (1-10)
        - temperament_characteristics_playfulness (int): Rating for playfulness (1-10)
        - temperament_characteristics_trainability (int): Rating for trainability (1-10)
        - temperament_characteristics_energy_level (int): Rating for energy level (1-10)
        - temperament_characteristics_barking_tendency (int): Rating for barking tendency (1-10)
        - description_mentality (str): Detailed description of the breed's mentality
        - description_history (str): Historical background of the breed
        - description_grooming_needs (str): Information about grooming requirements
        - description_size_and_appearance (str): Description of size and physical appearance
        - description_important_considerations (str): Important considerations for ownership
        - additional_information_popularity_rank (int): Popularity rank of the breed
        - additional_information_tags_0 (str): First tag associated with the breed
        - additional_information_tags_1 (str): Second tag associated with the breed
        - additional_information_guide_link (str): URL to official breed standard or guide
        - images_0 (str): URL of the first high-quality image
        - images_1 (str): URL of the second high-quality image
    """
    return {
        "name": "Golden Retriever",
        "summary": "Friendly, intelligent, and devoted companions ideal for families and active individuals.",
        "physical_characteristics_male_height_min": 56.0,
        "physical_characteristics_male_height_max": 61.0,
        "physical_characteristics_male_weight_min": 30.0,
        "physical_characteristics_male_weight_max": 34.0,
        "physical_characteristics_male_life_expectancy_min": 10,
        "physical_characteristics_male_life_expectancy_max": 12,
        "physical_characteristics_female_height_min": 51.0,
        "physical_characteristics_female_height_max": 56.0,
        "physical_characteristics_female_weight_min": 25.0,
        "physical_characteristics_female_weight_max": 32.0,
        "physical_characteristics_female_life_expectancy_min": 10,
        "physical_characteristics_female_life_expectancy_max": 12,
        "temperament_characteristics_affection_with_family": 10,
        "temperament_characteristics_playfulness": 9,
        "temperament_characteristics_trainability": 10,
        "temperament_characteristics_energy_level": 8,
        "temperament_characteristics_barking_tendency": 5,
        "description_mentality": "Golden Retrievers are known for their friendly, tolerant, and eager-to-please nature. They are highly social and thrive on human interaction.",
        "description_history": "Originating in Scotland during the 19th century, Golden Retrievers were bred as gundogs to retrieve shot waterfowl during hunting.",
        "description_grooming_needs": "Regular brushing several times a week is required to prevent matting and reduce shedding. Professional grooming every few months is recommended.",
        "description_size_and_appearance": "Medium to large-sized dogs with a dense, water-repellent coat that can be straight or wavy. They have a strong, muscular build and a friendly expression.",
        "description_important_considerations": "Prone to hip and elbow dysplasia. Require regular exercise and mental stimulation to prevent boredom-related behaviors.",
        "additional_information_popularity_rank": 3,
        "additional_information_tags_0": "Family Dog",
        "additional_information_tags_1": "Service Dog",
        "additional_information_guide_link": "https://www.akc.org/dog-breeds/golden-retriever/",
        "images_0": "https://example.com/images/golden-retriever-1.jpg",
        "images_1": "https://example.com/images/golden-retriever-2.jpg"
    }

def pote_get_breed_info(breedId: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific dog breed by ID.
    
    Args:
        breedId (str): The ID of the dog breed (required)
        
    Returns:
        Dict containing detailed breed information with the following structure:
        - name (str): the name of the dog breed
        - summary (str): a brief overview of the breed's key traits and suitability as a companion
        - physical_characteristics (Dict): contains physical attributes including height, weight, 
          and life expectancy ranges and averages for males and females
        - temperament_characteristics (Dict): ratings for behavioral traits such as affection with 
          family, playfulness, trainability, energy level, and barking tendency on a 10-point scale
        - description (Dict): detailed sections covering the breed's mentality, history, grooming needs, 
          size and appearance, and important considerations for ownership
        - additional_information (Dict): includes popularity rank, tags associated with the breed, 
          and a link to a detailed official guide or standard document
        - images (List[str]): list of URLs pointing to high-quality images of the breed
    
    Raises:
        ValueError: If breedId is empty or None
    """
    if not breedId:
        raise ValueError("breedId is required and cannot be empty")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("pote-get-breed-info")
    
    # Construct physical_characteristics structure
    physical_characteristics = {
        "male": {
            "height": {
                "min": api_data["physical_characteristics_male_height_min"],
                "max": api_data["physical_characteristics_male_height_max"]
            },
            "weight": {
                "min": api_data["physical_characteristics_male_weight_min"],
                "max": api_data["physical_characteristics_male_weight_max"]
            },
            "life_expectancy": {
                "min": api_data["physical_characteristics_male_life_expectancy_min"],
                "max": api_data["physical_characteristics_male_life_expectancy_max"]
            }
        },
        "female": {
            "height": {
                "min": api_data["physical_characteristics_female_height_min"],
                "max": api_data["physical_characteristics_female_height_max"]
            },
            "weight": {
                "min": api_data["physical_characteristics_female_weight_min"],
                "max": api_data["physical_characteristics_female_weight_max"]
            },
            "life_expectancy": {
                "min": api_data["physical_characteristics_female_life_expectancy_min"],
                "max": api_data["physical_characteristics_female_life_expectancy_max"]
            }
        }
    }
    
    # Construct temperament_characteristics structure
    temperament_characteristics = {
        "affection_with_family": api_data["temperament_characteristics_affection_with_family"],
        "playfulness": api_data["temperament_characteristics_playfulness"],
        "trainability": api_data["temperament_characteristics_trainability"],
        "energy_level": api_data["temperament_characteristics_energy_level"],
        "barking_tendency": api_data["temperament_characteristics_barking_tendency"]
    }
    
    # Construct description structure
    description = {
        "mentality": api_data["description_mentality"],
        "history": api_data["description_history"],
        "grooming_needs": api_data["description_grooming_needs"],
        "size_and_appearance": api_data["description_size_and_appearance"],
        "important_considerations": api_data["description_important_considerations"]
    }
    
    # Construct additional_information structure
    additional_information = {
        "popularity_rank": api_data["additional_information_popularity_rank"],
        "tags": [
            api_data["additional_information_tags_0"],
            api_data["additional_information_tags_1"]
        ],
        "guide_link": api_data["additional_information_guide_link"]
    }
    
    # Construct images list
    images = [
        api_data["images_0"],
        api_data["images_1"]
    ]
    
    # Assemble final result
    result = {
        "name": api_data["name"],
        "summary": api_data["summary"],
        "physical_characteristics": physical_characteristics,
        "temperament_characteristics": temperament_characteristics,
        "description": description,
        "additional_information": additional_information,
        "images": images
    }
    
    return result