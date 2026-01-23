from typing import Dict, Any, Optional
import re
import unicodedata

def japanese_text_analyzer_count_clipboard_words(language: Optional[str] = None, text: str = "") -> Dict[str, Any]:
    """
    テキストの単語数を計測します。英語ではスペースで区切られた単語をカウントし、日本語では形態素解析に近い方法（単純な文字種ベースの分割）を使用します。
    
    Parameters:
        language (Optional[str]): テキストの言語 ('en' for English, 'ja' for Japanese). 自動検出可能。
        text (str): 単語数をカウントするテキスト。必須。
    
    Returns:
        Dict[str, Any]: 以下のキーを持つ辞書
            - word_count (int): テキスト内の単語数
            - language_mode (str): 使用された言語モード ('en' または 'ja')
            - unit (str): 測定単位（例: '単語'）
            - raw_result (str): ツールの応答として返された完全なテキスト
    """
    if not text or not text.strip():
        return {
            "word_count": 0,
            "language_mode": language or "en",
            "unit": "単語",
            "raw_result": "テキストが空です。"
        }

    # 自動言語検出（languageが指定されていない場合）
    detected_language = language
    if not language:
        if re.search(r'[\u3040-\u309F]', text) or re.search(r'[\u30A0-\u30FF]', text) or re.search(r'[\u4E00-\u9FAF]', text):
            detected_language = 'ja'
        else:
            detected_language = 'en'
    else:
        detected_language = language

    word_count = 0

    if detected_language == 'en':
        # 英語: スペース、タブ、改行で単語を分割
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
    elif detected_language == 'ja':
        # 日本語: 空白以外の連続する文字列を「単語」としてカウント（簡易形態素解析の代用）
        # ひらがな、カタカナ、漢字、英数字などを含む連続する非空白文字列
        words = re.findall(r'\S+', text)
        word_count = len(words)
    else:
        # サポートされていない言語の場合、デフォルトで英語として扱う
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        detected_language = 'en'

    # raw_result の生成（例のような自然な応答文）
    if detected_language == 'ja':
        raw_result = f"テキストに含まれる単語数は {word_count} 単語です。"
    else:
        raw_result = f"The text contains {word_count} words."

    return {
        "word_count": word_count,
        "language_mode": detected_language,
        "unit": "単語",
        "raw_result": raw_result
    }