from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Magic UI components.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - widgets_0_name (str): Name of first UI component
        - widgets_0_description (str): Description of first component
        - widgets_0_usage_scenario (str): Usage scenario of first component
        - widgets_0_code_snippets_react (str): React code snippet for first component
        - widgets_0_code_snippets_vue (str): Vue code snippet for first component
        - widgets_0_animation_type_0 (str): First animation type of first component
        - widgets_0_animation_type_1 (str): Second animation type of first component
        - widgets_0_dependencies_0 (str): First dependency of first component
        - widgets_0_dependencies_1 (str): Second dependency of first component
        - widgets_0_props_0_name (str): First prop name of first component
        - widgets_0_props_0_type (str): Type of first prop of first component
        - widgets_0_props_0_default (str): Default value of first prop of first component
        - widgets_0_props_0_description (str): Description of first prop of first component
        - widgets_0_props_1_name (str): Second prop name of first component
        - widgets_0_props_1_type (str): Type of second prop of first component
        - widgets_0_props_1_default (str): Default value of second prop of first component
        - widgets_0_props_1_description (str): Description of second prop of first component
        - widgets_0_preview_url (str): Preview URL of first component
        - widgets_1_name (str): Name of second UI component
        - widgets_1_description (str): Description of second component
        - widgets_1_usage_scenario (str): Usage scenario of second component
        - widgets_1_code_snippets_react (str): React code snippet for second component
        - widgets_1_code_snippets_vue (str): Vue code snippet for second component
        - widgets_1_animation_type_0 (str): First animation type of second component
        - widgets_1_animation_type_1 (str): Second animation type of second component
        - widgets_1_dependencies_0 (str): First dependency of second component
        - widgets_1_dependencies_1 (str): Second dependency of second component
        - widgets_1_props_0_name (str): First prop name of second component
        - widgets_1_props_0_type (str): Type of first prop of second component
        - widgets_1_props_0_default (str): Default value of first prop of second component
        - widgets_1_props_0_description (str): Description of first prop of second component
        - widgets_1_props_1_name (str): Second prop name of second component
        - widgets_1_props_1_type (str): Type of second prop of second component
        - widgets_1_props_1_default (str): Default value of second prop of second component
        - widgets_1_props_1_description (str): Description of second prop of second component
        - widgets_1_preview_url (str): Preview URL of second component
        - total_widgets (int): Total number of widgets returned
        - supported_frameworks_0 (str): First supported framework
        - supported_frameworks_1 (str): Second supported framework
        - documentation_url (str): Base URL for full documentation
        - has_more (bool): Whether more widgets are available
    """
    return {
        "widgets_0_name": "animated-list",
        "widgets_0_description": "A list that animates items as they enter or leave the viewport using smooth transitions.",
        "widgets_0_usage_scenario": "Used in dashboards to display dynamic data entries with visual feedback.",
        "widgets_0_code_snippets_react": "<AnimatedList items={data} animation='fade' />",
        "widgets_0_code_snippets_vue": "<AnimatedList :items='data' animation='fade' />",
        "widgets_0_animation_type_0": "fade",
        "widgets_0_animation_type_1": "slide-up",
        "widgets_0_dependencies_0": "framer-motion",
        "widgets_0_dependencies_1": "react-intersection-observer",
        "widgets_0_props_0_name": "items",
        "widgets_0_props_0_type": "Array",
        "widgets_0_props_0_default": "[]",
        "widgets_0_props_0_description": "List of items to render in the animated list",
        "widgets_0_props_1_name": "animation",
        "widgets_0_props_1_type": "String",
        "widgets_0_props_1_default": "'fade'",
        "widgets_0_props_1_description": "Type of animation to apply on item entry/exit",
        "widgets_0_preview_url": "https://magicui.dev/components/animated-list/demo",

        "widgets_1_name": "tweet-card",
        "widgets_1_description": "A responsive card component that displays a tweet with user avatar, content, and engagement metrics.",
        "widgets_1_usage_scenario": "Social media feeds, content previews, and user-generated content sections.",
        "widgets_1_code_snippets_react": "<TweetCard tweet={tweetData} showActions={true} />",
        "widgets_1_code_snippets_vue": "<TweetCard :tweet='tweetData' :show-actions='true' />",
        "widgets_1_animation_type_0": "scale",
        "widgets_1_animation_type_1": "pulse",
        "widgets_1_dependencies_0": "clsx",
        "widgets_1_dependencies_1": "tailwind-merge",
        "widgets_1_props_0_name": "tweet",
        "widgets_1_props_0_type": "Object",
        "widgets_1_props_0_default": "null",
        "widgets_1_props_0_description": "Tweet data object containing user, text, and metadata",
        "widgets_1_props_1_name": "showActions",
        "widgets_1_props_1_type": "Boolean",
        "widgets_1_props_1_default": "true",
        "widgets_1_props_1_description": "Whether to display like, retweet, and reply buttons",
        "widgets_1_preview_url": "https://magicui.dev/components/tweet-card/demo",

        "total_widgets": 2,
        "supported_frameworks_0": "React",
        "supported_frameworks_1": "Vue",
        "documentation_url": "https://magicui.dev/docs",
        "has_more": True
    }

def magic_ui_component_server_getWidgets() -> Dict[str, Any]:
    """
    Fetches implementation details for Magic UI components such as animated-list, tweet-card, etc.

    Returns:
        Dict containing:
        - widgets (List[Dict]): List of component implementation details
        - total_widgets (int): Total number of widgets returned
        - supported_frameworks (List[str]): Frontend frameworks supported
        - documentation_url (str): Base URL for full documentation
        - has_more (bool): Indicates if more widgets are available
    """
    try:
        api_data = call_external_api("magic-ui-component-server-getWidgets")

        widgets = []

        # Construct first widget
        widget_0 = {
            "name": api_data["widgets_0_name"],
            "description": api_data["widgets_0_description"],
            "usage_scenario": api_data["widgets_0_usage_scenario"],
            "code_snippets": {
                "react": api_data["widgets_0_code_snippets_react"],
                "vue": api_data["widgets_0_code_snippets_vue"]
            },
            "animation_type": [
                api_data["widgets_0_animation_type_0"],
                api_data["widgets_0_animation_type_1"]
            ],
            "dependencies": [
                api_data["widgets_0_dependencies_0"],
                api_data["widgets_0_dependencies_1"]
            ],
            "props": [
                {
                    "name": api_data["widgets_0_props_0_name"],
                    "type": api_data["widgets_0_props_0_type"],
                    "default": api_data["widgets_0_props_0_default"],
                    "description": api_data["widgets_0_props_0_description"]
                },
                {
                    "name": api_data["widgets_0_props_1_name"],
                    "type": api_data["widgets_0_props_1_type"],
                    "default": api_data["widgets_0_props_1_default"],
                    "description": api_data["widgets_0_props_1_description"]
                }
            ],
            "preview_url": api_data["widgets_0_preview_url"]
        }
        widgets.append(widget_0)

        # Construct second widget
        widget_1 = {
            "name": api_data["widgets_1_name"],
            "description": api_data["widgets_1_description"],
            "usage_scenario": api_data["widgets_1_usage_scenario"],
            "code_snippets": {
                "react": api_data["widgets_1_code_snippets_react"],
                "vue": api_data["widgets_1_code_snippets_vue"]
            },
            "animation_type": [
                api_data["widgets_1_animation_type_0"],
                api_data["widgets_1_animation_type_1"]
            ],
            "dependencies": [
                api_data["widgets_1_dependencies_0"],
                api_data["widgets_1_dependencies_1"]
            ],
            "props": [
                {
                    "name": api_data["widgets_1_props_0_name"],
                    "type": api_data["widgets_1_props_0_type"],
                    "default": api_data["widgets_1_props_0_default"],
                    "description": api_data["widgets_1_props_0_description"]
                },
                {
                    "name": api_data["widgets_1_props_1_name"],
                    "type": api_data["widgets_1_props_1_type"],
                    "default": api_data["widgets_1_props_1_default"],
                    "description": api_data["widgets_1_props_1_description"]
                }
            ],
            "preview_url": api_data["widgets_1_preview_url"]
        }
        widgets.append(widget_1)

        result = {
            "widgets": widgets,
            "total_widgets": api_data["total_widgets"],
            "supported_frameworks": [
                api_data["supported_frameworks_0"],
                api_data["supported_frameworks_1"]
            ],
            "documentation_url": api_data["documentation_url"],
            "has_more": api_data["has_more"]
        }

        return result

    except Exception as e:
        # In case of any error, return empty structure
        return {
            "widgets": [],
            "total_widgets": 0,
            "supported_frameworks": [],
            "documentation_url": "",
            "has_more": False
        }