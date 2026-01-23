from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Lorenz Woehr's portfolio profile.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Full name of Lorenz Woehr
        - role (str): Professional role or title
        - website (str): Personal/portfolio website URL
        - shortBiography (str): Concise summary of professional background and expertise
        - longBiography_0_children_0_text (str): First text span in first long biography block
        - longBiography_0_children_0_marks_0_type (str): First mark type in first child of first block
        - longBiography_1_children_0_text (str): First text span in second long biography block
        - education_0_degree (str): Degree of first educational entry
        - education_0_institution (str): Institution of first educational entry
        - education_0_gradYear (int): Graduation year of first educational entry
        - education_1_degree (str): Degree of second educational entry
        - education_1_institution (str): Institution of second educational entry
        - education_1_gradYear (int): Graduation year of second educational entry
        - workExperience_0_company (str): Company name of first work experience
        - workExperience_0_role (str): Role at first company
        - workExperience_0_startDate (str): Start date of first work experience
        - workExperience_0_endDate (str): End date of first work experience
        - workExperience_0_current (bool): Whether currently working at first company
        - workExperience_0_location (str): Location of first work experience
        - workExperience_0_description_0_text (str): First description text block of first work experience
        - workExperience_1_company (str): Company name of second work experience
        - workExperience_1_role (str): Role at second company
        - workExperience_1_startDate (str): Start date of second work experience
        - workExperience_1_endDate (str): End date of second work experience
        - workExperience_1_current (bool): Whether currently working at second company
        - workExperience_1_location (str): Location of second work experience
        - workExperience_1_description_0_text (str): First description text block of second work experience
        - skills_0_category (str): Category of first skill set
        - skills_0_item_0 (str): First skill item in first category
        - skills_0_item_1 (str): Second skill item in first category
        - skills_1_category (str): Category of second skill set
        - skills_1_item_0 (str): First skill item in second category
        - skills_1_item_1 (str): Second skill item in second category
        - languages_0_language (str): First spoken language
        - languages_0_proficiency (str): Proficiency level in first language
        - languages_1_language (str): Second spoken language
        - languages_1_proficiency (str): Proficiency level in second language
    """
    return {
        "name": "Lorenz Woehr",
        "role": "Senior Software Engineer & Full-Stack Developer",
        "website": "https://lorenzwoehr.com",
        "shortBiography": "Lorenz Woehr is a senior software engineer specializing in full-stack development with over 10 years of experience building scalable web applications and cloud-native systems.",
        "longBiography_0_children_0_text": "Lorenz began his career in software development after graduating from technical university. He quickly gained recognition for his ability to design robust backend systems.",
        "longBiography_0_children_0_marks_0_type": "bold",
        "longBiography_1_children_0_text": "Over the years, Lorenz has led multiple engineering teams and contributed to open-source projects focused on developer tooling and infrastructure automation.",
        "education_0_degree": "Master of Science in Computer Science",
        "education_0_institution": "Technical University of Munich",
        "education_0_gradYear": 2012,
        "education_1_degree": "Bachelor of Science in Software Engineering",
        "education_1_institution": "University of Stuttgart",
        "education_1_gradYear": 2010,
        "workExperience_0_company": "TechNova Inc.",
        "workExperience_0_role": "Lead Backend Engineer",
        "workExperience_0_startDate": "2018-03-01",
        "workExperience_0_endDate": "present",
        "workExperience_0_current": True,
        "workExperience_0_location": "Berlin, Germany",
        "workExperience_0_description_0_text": "Architected and maintained microservices using Node.js and Python. Led migration to Kubernetes-based infrastructure.",
        "workExperience_1_company": "WebScale Solutions",
        "workExperience_1_role": "Full-Stack Developer",
        "workExperience_1_startDate": "2014-06-01",
        "workExperience_1_endDate": "2018-02-28",
        "workExperience_1_current": False,
        "workExperience_1_location": "Munich, Germany",
        "workExperience_1_description_0_text": "Developed customer-facing applications using React and Django. Implemented CI/CD pipelines and automated testing suites.",
        "skills_0_category": "Programming Languages",
        "skills_0_item_0": "JavaScript/TypeScript",
        "skills_0_item_1": "Python",
        "skills_1_category": "Cloud & DevOps",
        "skills_1_item_0": "AWS",
        "skills_1_item_1": "Docker",
        "languages_0_language": "German",
        "languages_0_proficiency": "Native",
        "languages_1_language": "English",
        "languages_1_proficiency": "Fluent"
    }

def lorenz_woehr_portfolio_get_profile() -> Dict[str, Any]:
    """
    Get the profile information of Lorenz Woehr including personal details, biography,
    education, work experience, skills, and languages.

    Returns:
        Dict containing:
        - name (str): Full name of Lorenz Woehr
        - role (str): Professional role or title
        - website (str): Personal/portfolio website URL
        - shortBiography (str): Concise summary of professional background and expertise
        - longBiography (List[Dict]): Detailed biography blocks with text and formatting
        - education (List[Dict]): Educational background entries
        - workExperience (List[Dict]): Professional work history entries
        - skills (List[Dict]): Categorized skill sets
        - languages (List[Dict]): Spoken languages with proficiency levels
    """
    try:
        api_data = call_external_api("lorenz-woehr-portfolio-get_profile")

        long_biography = [
            {
                "children": [
                    {
                        "text": api_data["longBiography_0_children_0_text"],
                        "marks": [
                            {"type": api_data["longBiography_0_children_0_marks_0_type"]}
                        ]
                    }
                ]
            },
            {
                "children": [
                    {
                        "text": api_data["longBiography_1_children_0_text"]
                    }
                ]
            }
        ]

        education = [
            {
                "degree": api_data["education_0_degree"],
                "institution": api_data["education_0_institution"],
                "gradYear": api_data["education_0_gradYear"]
            },
            {
                "degree": api_data["education_1_degree"],
                "institution": api_data["education_1_institution"],
                "gradYear": api_data["education_1_gradYear"]
            }
        ]

        work_experience = [
            {
                "company": api_data["workExperience_0_company"],
                "role": api_data["workExperience_0_role"],
                "startDate": api_data["workExperience_0_startDate"],
                "endDate": api_data["workExperience_0_endDate"],
                "current": api_data["workExperience_0_current"],
                "location": api_data["workExperience_0_location"],
                "description": [
                    {"text": api_data["workExperience_0_description_0_text"]}
                ]
            },
            {
                "company": api_data["workExperience_1_company"],
                "role": api_data["workExperience_1_role"],
                "startDate": api_data["workExperience_1_startDate"],
                "endDate": api_data["workExperience_1_endDate"],
                "current": api_data["workExperience_1_current"],
                "location": api_data["workExperience_1_location"],
                "description": [
                    {"text": api_data["workExperience_1_description_0_text"]}
                ]
            }
        ]

        skills = [
            {
                "category": api_data["skills_0_category"],
                "items": [
                    api_data["skills_0_item_0"],
                    api_data["skills_0_item_1"]
                ]
            },
            {
                "category": api_data["skills_1_category"],
                "items": [
                    api_data["skills_1_item_0"],
                    api_data["skills_1_item_1"]
                ]
            }
        ]

        languages = [
            {
                "language": api_data["languages_0_language"],
                "proficiency": api_data["languages_0_proficiency"]
            },
            {
                "language": api_data["languages_1_language"],
                "proficiency": api_data["languages_1_proficiency"]
            }
        ]

        return {
            "name": api_data["name"],
            "role": api_data["role"],
            "website": api_data["website"],
            "shortBiography": api_data["shortBiography"],
            "longBiography": long_biography,
            "education": education,
            "workExperience": work_experience,
            "skills": skills,
            "languages": languages
        }
    except Exception as e:
        # In case of any error, return a minimal profile
        return {
            "name": "Lorenz Woehr",
            "role": "Senior Software Engineer & Full-Stack Developer",
            "website": "",
            "shortBiography": "Data unavailable",
            "longBiography": [],
            "education": [],
            "workExperience": [],
            "skills": [],
            "languages": []
        }