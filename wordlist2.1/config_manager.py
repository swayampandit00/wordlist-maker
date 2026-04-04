import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_file="wordlist_config.json"):
        self.config_file = config_file
        self.default_config = {
            "level": 0,
            "min_length": 8,
            "max_length": 12,
            "num_range": 0,
            "years": 0,
            "chars": False,
            "leet": False,
            "verbose": False,
            "export_file": "passwords.txt",
            "names": [],
            "keywords": [],
            "dates": [],
            "phones": [],
            "old_passwords": [],
            "languages": [],
            "templates": [],
            "threads": 4
        }
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_file):
            return self.default_config.copy()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Merge with default config to ensure all keys exist
            merged_config = self.default_config.copy()
            merged_config.update(config)
            return merged_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def export_config(self, config: Dict[str, Any], filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, filename: str) -> Dict[str, Any]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Merge with default config
            merged_config = self.default_config.copy()
            merged_config.update(config)
            return merged_config
        except Exception as e:
            print(f"Error importing config: {e}")
            return self.default_config.copy()
    
    def create_preset(self, name: str, description: str, config: Dict[str, Any]) -> bool:
        presets = self.get_presets()
        presets[name] = {
            "description": description,
            "config": config
        }
        
        try:
            with open("presets.json", 'w', encoding='utf-8') as f:
                json.dump(presets, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving preset: {e}")
            return False
    
    def get_presets(self) -> Dict[str, Any]:
        if not os.path.exists("presets.json"):
            return {}
        
        try:
            with open("presets.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading presets: {e}")
            return {}
    
    def load_preset(self, name: str) -> Dict[str, Any]:
        presets = self.get_presets()
        if name in presets:
            return presets[name]["config"]
        return self.default_config.copy()
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_keys = self.default_config.keys()
        
        # Check if all required keys exist
        for key in required_keys:
            if key not in config:
                return False
        
        # Validate specific fields
        if not isinstance(config["level"], int) or config["level"] < 0 or config["level"] > 5:
            return False
        
        if not isinstance(config["min_length"], int) or config["min_length"] < 1:
            return False
        
        if not isinstance(config["max_length"], int) or config["max_length"] < config["min_length"]:
            return False
        
        if not isinstance(config["num_range"], int) or config["num_range"] < 0:
            return False
        
        if not isinstance(config["years"], int) or config["years"] < 0:
            return False
        
        if not isinstance(config["threads"], int) or config["threads"] < 1:
            return False
        
        return True
