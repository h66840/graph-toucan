from typing import Dict, Any

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def google_workshop_mcp_server_simple_test(text: str) -> Dict[str, str]:
    """
    간단한 테스트 도구: 입력 텍스트를 그대로 반환합니다.
    
    이 함수는 주어진 텍스트 입력을 받아 동일한 텍스트를 응답으로 반환하는 순수 계산 함수입니다.
    외부 API 호출이나 네트워크 요청 없이 내부 로직만으로 결과를 생성합니다.
    
    Parameters:
        text (str): 반환할 입력 텍스트. 빈 문자열일 수 있지만 제공되어야 합니다.
    
    Returns:
        Dict[str, str]: 입력 텍스트를 포함하는 응답 딕셔너리. 키는 'response_text'이며, 
                        값은 입력된 텍스트와 동일합니다.
    
    Raises:
        ValueError: text 파라미터가 제공되지 않았을 경우
    """
    if text is None:
        raise ValueError("text parameter is required and cannot be None")
    
    return {
        "response_text": text
    }