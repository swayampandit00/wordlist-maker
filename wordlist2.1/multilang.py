import re
import unicodedata

class MultiLanguageSupport:
    def __init__(self):
        self.supported_chars = set()
        self.language_patterns = {
            'hindi': r'[\u0900-\u097F]',
            'arabic': r'[\u0600-\u06FF]',
            'chinese': r'[\u4E00-\u9FFF]',
            'japanese': r'[\u3040-\u309F\u30A0-\u30FF]',
            'russian': r'[\u0400-\u04FF]',
            'european': r'[\u00C0-\u00FF\u0100-\u017F]'
        }
    
    def add_language_support(self, languages):
        for lang in languages:
            if lang.lower() in self.language_patterns:
                self.supported_chars.update(self.get_charset(lang))
    
    def get_charset(self, language):
        charset = set()
        pattern = self.language_patterns.get(language.lower(), '')
        if pattern:
            for char in range(0x10000):
                char_str = chr(char)
                if re.match(pattern, char_str):
                    charset.add(char_str)
        return charset
    
    def normalize_text(self, text):
        return unicodedata.normalize('NFKC', text)
    
    def is_supported_char(self, char):
        return char in self.supported_chars or char.isascii()
    
    def filter_text(self, text):
        return ''.join(char for char in text if self.is_supported_char(char))
