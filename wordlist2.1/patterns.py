import re
from itertools import product

class PatternTemplates:
    def __init__(self):
        self.templates = {
            'common': [
                '{name}{year}',
                '{name}{number}',
                '{name}{special}',
                '{name}{year}{number}',
                '{name}{number}{year}',
                '{name}{special}{number}',
                '{year}{name}',
                '{number}{name}',
                '{special}{name}',
                '{name}{name}',
                '{name}{name}{year}',
                '{name}{name}{number}'
            ],
            'corporate': [
                '{company}{year}',
                '{company}{number}',
                '{company}{special}',
                '{company}{department}{year}',
                '{company}{location}{year}',
                '{company}{year}{quarter}',
                '{company}{project}{year}',
                '{company}{name}{year}',
                'Admin{year}',
                'Admin{number}',
                'Password{year}',
                'Password{number}'
            ],
            'personal': [
                '{name}{birthdate}',
                '{name}{anniversary}',
                '{name}{phone_last4}',
                '{name}{zipcode}',
                '{name}{pet}{year}',
                '{child}{name}{year}',
                '{spouse}{name}{year}',
                '{name}{sports}{year}',
                '{name}{hobby}{year}',
                '{name}{car}{year}'
            ],
            'gaming': [
                '{gamer}{tag}{year}',
                '{gamer}{number}',
                '{gamer}{special}',
                '{game}{name}{year}',
                '{clan}{name}{year}',
                '{character}{name}{year}',
                '{weapon}{name}{year}',
                '{server}{name}{year}',
                '{rank}{name}{year}',
                '{team}{name}{year}'
            ],
            'social': [
                '{name}{platform}{year}',
                '{name}{handle}{year}',
                '{name}{follower}{year}',
                '{name}{post}{year}',
                '{name}{story}{year}',
                '{name}{like}{year}',
                '{name}{share}{year}',
                '{name}{comment}{year}',
                '{name}{friend}{year}',
                '{name}{group}{year}'
            ]
        }
        
        self.common_words = {
            'special': ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '.', ','],
            'number': ['123', '456', '789', '007', '999', '666', '111', '222', '333', '444'],
            'year': ['2023', '2024', '2025', '2022', '2021', '2020', '2019', '2018'],
            'quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
            'department': ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Support', 'Admin'],
            'location': ['NYC', 'LA', 'SF', 'London', 'Paris', 'Tokyo', 'Berlin', 'Mumbai'],
            'project': ['Project', 'Proj', 'Work', 'Task', 'Job'],
            'birthdate': ['BD', 'Bday', 'Birthday', 'DOB'],
            'anniversary': ['Ann', 'Anniversary', 'Wedding'],
            'phone_last4': ['1234', '5678', '9012', '3456'],
            'zipcode': ['10001', '90210', '60601', '33101'],
            'pet': ['Dog', 'Cat', 'Bird', 'Fish', 'Pet'],
            'child': ['Son', 'Daughter', 'Kid', 'Baby'],
            'spouse': ['Wife', 'Husband', 'Partner', 'Love'],
            'sports': ['Football', 'Soccer', 'Basketball', 'Baseball', 'Tennis'],
            'hobby': ['Music', 'Art', 'Travel', 'Food', 'Game'],
            'car': ['Car', 'Auto', 'Vehicle', 'Drive'],
            'gamer': ['Player', 'Gamer', 'User', 'Pro', 'Noob'],
            'tag': ['Tag', 'Pro', 'Elite', 'Master', 'King'],
            'game': ['Game', 'Play', 'Win', 'Score', 'Level'],
            'clan': ['Clan', 'Team', 'Guild', 'Squad', 'Group'],
            'character': ['Hero', 'Character', 'Avatar', 'Player'],
            'weapon': ['Weapon', 'Gun', 'Sword', 'Knife', 'Bow'],
            'server': ['Server', 'Host', 'Node', 'Cloud'],
            'rank': ['Rank', 'Level', 'Score', 'Points'],
            'platform': ['FB', 'IG', 'TW', 'YT', 'TK'],
            'handle': ['Handle', 'User', 'Name', 'ID'],
            'follower': ['Follow', 'Fan', 'Like', 'Heart'],
            'post': ['Post', 'Share', 'Update', 'Status'],
            'story': ['Story', 'Tale', 'Life', 'Day'],
            'like': ['Like', 'Heart', 'Love', 'Star'],
            'share': ['Share', 'Post', 'Send', 'Give'],
            'comment': ['Comment', 'Reply', 'Talk', 'Chat'],
            'friend': ['Friend', 'Buddy', 'Pal', 'Mate'],
            'group': ['Group', 'Team', 'Circle', 'Club']
        }
    
    def generate_from_template(self, template_name, data_dict):
        passwords = set()
        
        if template_name not in self.templates:
            return passwords
        
        templates = self.templates[template_name]
        
        for template in templates:
            # Replace placeholders with actual data
            password = template
            
            # Replace name placeholders
            if '{name}' in password:
                names = data_dict.get('names', [])
                for name in names:
                    temp_password = password.replace('{name}', name)
                    passwords.add(self._replace_common_placeholders(temp_password, data_dict))
            
            # Replace other placeholders
            passwords.add(self._replace_common_placeholders(password, data_dict))
        
        return passwords
    
    def _replace_common_placeholders(self, template, data_dict):
        passwords = set()
        current_passwords = [template]
        
        # Replace each placeholder type
        for placeholder_type, values in self.common_words.items():
            new_passwords = set()
            f'{{{placeholder_type}}}'
            
            for password in current_passwords:
                if f'{{{placeholder_type}}}' in password:
                    for value in values:
                        new_password = password.replace(f'{{{placeholder_type}}}', value)
                        new_passwords.add(new_password)
                else:
                    new_passwords.add(password)
            
            current_passwords = list(new_passwords)
        
        # Replace data-specific placeholders
        for key, values in data_dict.items():
            if values:
                new_passwords = set()
                for password in current_passwords:
                    if f'{{{key}}}' in password:
                        for value in values:
                            if isinstance(value, str):
                                new_password = password.replace(f'{{{key}}}', value)
                                new_passwords.add(new_password)
                    else:
                        new_passwords.add(password)
                current_passwords = list(new_passwords)
        
        return set(current_passwords)
    
    def get_all_templates(self):
        return list(self.templates.keys())
    
    def add_custom_template(self, name, template_list):
        if isinstance(template_list, str):
            template_list = [template_list]
        self.templates[name] = template_list
    
    def generate_all_patterns(self, data_dict):
        all_passwords = set()
        
        for template_name in self.templates:
            passwords = self.generate_from_template(template_name, data_dict)
            all_passwords.update(passwords)
        
        return all_passwords
