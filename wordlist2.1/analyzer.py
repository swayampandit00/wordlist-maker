import re
import collections
import math
from typing import Dict, List, Tuple, Any

class WordlistAnalyzer:
    def __init__(self):
        self.common_patterns = {
            'numeric_only': r'^\d+$',
            'alpha_only': r'^[a-zA-Z]+$',
            'alphanumeric': r'^[a-zA-Z0-9]+$',
            'with_special': r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]+$',
            'starts_with_capital': r'^[A-Z]',
            'ends_with_number': r'\d+$',
            'contains_year': r'(19|20)\d{2}',
            'common_words': r'\b(password|admin|user|login|welcome|123|qwerty)\b',
            'repeated_chars': r'(.)\1{2,}',
            'keyboard_patterns': r'(qwerty|asdf|zxcv|1234|abcd)'
        }
        
        self.strength_indicators = {
            'length_score': 0,
            'complexity_score': 0,
            'pattern_score': 0,
            'uniqueness_score': 0
        }
    
    def analyze_wordlist(self, file_path: str) -> Dict[str, Any]:
        """Analyze a wordlist file and return comprehensive statistics"""
        
        if not self._load_wordlist(file_path):
            return {'error': 'Could not load wordlist file'}
        
        analysis = {
            'basic_stats': self._get_basic_stats(),
            'length_distribution': self._analyze_length_distribution(),
            'character_analysis': self._analyze_characters(),
            'pattern_analysis': self._analyze_patterns(),
            'strength_analysis': self._analyze_strength(),
            'common_passwords': self._find_common_passwords(),
            'recommendations': self._generate_recommendations()
        }
        
        return analysis
    
    def _load_wordlist(self, file_path: str) -> bool:
        """Load wordlist from file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.passwords = [line.strip() for line in f if line.strip()]
            return True
        except Exception as e:
            print(f"Error loading wordlist: {e}")
            return False
    
    def _get_basic_stats(self) -> Dict[str, Any]:
        """Get basic statistics about the wordlist"""
        total_passwords = len(self.passwords)
        unique_passwords = len(set(self.passwords))
        
        lengths = [len(pwd) for pwd in self.passwords]
        avg_length = sum(lengths) / len(lengths) if lengths else 0
        min_length = min(lengths) if lengths else 0
        max_length = max(lengths) if lengths else 0
        
        return {
            'total_passwords': total_passwords,
            'unique_passwords': unique_passwords,
            'duplicate_percentage': ((total_passwords - unique_passwords) / total_passwords * 100) if total_passwords > 0 else 0,
            'average_length': round(avg_length, 2),
            'min_length': min_length,
            'max_length': max_length
        }
    
    def _analyze_length_distribution(self) -> Dict[str, Any]:
        """Analyze password length distribution"""
        length_counts = collections.Counter(len(pwd) for pwd in self.passwords)
        
        # Categorize lengths
        categories = {
            'very_short': 0,    # < 6
            'short': 0,         # 6-8
            'medium': 0,        # 9-12
            'long': 0,          # 13-16
            'very_long': 0      # > 16
        }
        
        for length, count in length_counts.items():
            if length < 6:
                categories['very_short'] += count
            elif length <= 8:
                categories['short'] += count
            elif length <= 12:
                categories['medium'] += count
            elif length <= 16:
                categories['long'] += count
            else:
                categories['very_long'] += count
        
        return {
            'distribution': dict(length_counts),
            'categories': categories,
            'most_common_length': length_counts.most_common(1)[0] if length_counts else (0, 0)
        }
    
    def _analyze_characters(self) -> Dict[str, Any]:
        """Analyze character usage in passwords"""
        char_counts = collections.Counter()
        digit_counts = collections.Counter()
        upper_counts = collections.Counter()
        lower_counts = collections.Counter()
        special_counts = collections.Counter()
        
        total_chars = 0
        for pwd in self.passwords:
            for char in pwd:
                char_counts[char] += 1
                total_chars += 1
                
                if char.isdigit():
                    digit_counts[char] += 1
                elif char.isupper():
                    upper_counts[char] += 1
                elif char.islower():
                    lower_counts[char] += 1
                else:
                    special_counts[char] += 1
        
        # Calculate percentages
        char_percentages = {char: (count / total_chars * 100) for char, count in char_counts.items()}
        
        return {
            'total_characters': total_chars,
            'unique_characters': len(char_counts),
            'character_frequencies': dict(char_counts.most_common(20)),
            'character_percentages': dict(sorted(char_percentages.items(), key=lambda x: x[1], reverse=True)[:20]),
            'digit_frequencies': dict(digit_counts.most_common()),
            'uppercase_frequencies': dict(upper_counts.most_common()),
            'lowercase_frequencies': dict(lower_counts.most_common()),
            'special_frequencies': dict(special_counts.most_common())
        }
    
    def _analyze_patterns(self) -> Dict[str, Any]:
        """Analyze common patterns in passwords"""
        pattern_matches = {}
        
        for pattern_name, pattern in self.common_patterns.items():
            matches = 0
            for pwd in self.passwords:
                if re.search(pattern, pwd, re.IGNORECASE):
                    matches += 1
            pattern_matches[pattern_name] = {
                'count': matches,
                'percentage': (matches / len(self.passwords) * 100) if self.passwords else 0
            }
        
        # Find common prefixes and suffixes
        prefixes = collections.Counter(pwd[:3] for pwd in self.passwords if len(pwd) >= 3)
        suffixes = collections.Counter(pwd[-3:] for pwd in self.passwords if len(pwd) >= 3)
        
        return {
            'pattern_matches': pattern_matches,
            'common_prefixes': dict(prefixes.most_common(10)),
            'common_suffixes': dict(suffixes.most_common(10))
        }
    
    def _analyze_strength(self) -> Dict[str, Any]:
        """Analyze password strength distribution"""
        strength_scores = []
        strength_categories = {
            'very_weak': 0,
            'weak': 0,
            'medium': 0,
            'strong': 0,
            'very_strong': 0
        }
        
        for pwd in self.passwords:
            score = self._calculate_password_strength(pwd)
            strength_scores.append(score)
            
            if score < 20:
                strength_categories['very_weak'] += 1
            elif score < 40:
                strength_categories['weak'] += 1
            elif score < 60:
                strength_categories['medium'] += 1
            elif score < 80:
                strength_categories['strong'] += 1
            else:
                strength_categories['very_strong'] += 1
        
        return {
            'average_strength': sum(strength_scores) / len(strength_scores) if strength_scores else 0,
            'strength_distribution': strength_categories,
            'strength_scores': strength_scores
        }
    
    def _calculate_password_strength(self, password: str) -> float:
        """Calculate strength score for a single password"""
        score = 0
        
        # Length component (0-30 points)
        length = len(password)
        if length >= 8:
            score += min(30, length * 2)
        
        # Character variety (0-30 points)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        variety_score = sum([has_lower, has_upper, has_digit, has_special]) * 7.5
        score += variety_score
        
        # Complexity (0-20 points)
        unique_chars = len(set(password))
        complexity_score = min(20, unique_chars * 2)
        score += complexity_score
        
        # Pattern penalty (0-20 points)
        pattern_penalty = 0
        if re.search(r'(.)\1{2,}', password):  # Repeated characters
            pattern_penalty += 10
        if re.search(r'(qwerty|asdf|zxcv|1234|abcd)', password.lower()):  # Keyboard patterns
            pattern_penalty += 10
        
        score = max(0, score - pattern_penalty)
        
        return min(100, score)
    
    def _find_common_passwords(self) -> Dict[str, Any]:
        """Find most common passwords in the list"""
        password_counts = collections.Counter(self.passwords)
        
        # Check against known weak passwords
        weak_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey'
        ]
        
        found_weak = []
        for weak_pwd in weak_passwords:
            if weak_pwd in password_counts:
                found_weak.append((weak_pwd, password_counts[weak_pwd]))
        
        return {
            'most_common': password_counts.most_common(20),
            'weak_passwords_found': found_weak,
            'duplicate_passwords': [(pwd, count) for pwd, count in password_counts.items() if count > 1][:10]
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        basic_stats = self._get_basic_stats()
        length_dist = self._analyze_length_distribution()
        pattern_analysis = self._analyze_patterns()
        strength_analysis = self._analyze_strength()
        
        # Length recommendations
        if basic_stats['average_length'] < 10:
            recommendations.append("Consider increasing minimum password length to improve security")
        
        if length_dist['categories']['short'] > len(self.passwords) * 0.3:
            recommendations.append("Too many short passwords (6-8 chars). Consider longer passwords")
        
        # Pattern recommendations
        if pattern_analysis['pattern_matches']['numeric_only']['percentage'] > 20:
            recommendations.append("High percentage of numeric-only passwords. Add more variety")
        
        if pattern_analysis['pattern_matches']['alpha_only']['percentage'] > 30:
            recommendations.append("Many alphabetic-only passwords. Include numbers and special characters")
        
        # Strength recommendations
        if strength_analysis['average_strength'] < 50:
            recommendations.append("Average password strength is low. Focus on more complex combinations")
        
        if strength_analysis['strength_distribution']['very_weak'] > len(self.passwords) * 0.2:
            recommendations.append("Too many very weak passwords. Review generation parameters")
        
        # Duplicate recommendations
        if basic_stats['duplicate_percentage'] > 5:
            recommendations.append("High duplicate percentage. Consider more diverse generation methods")
        
        if not recommendations:
            recommendations.append("Wordlist quality appears good. Continue with current parameters")
        
        return recommendations
    
    def generate_report(self, file_path: str, output_file: str = None) -> str:
        """Generate a comprehensive analysis report"""
        analysis = self.analyze_wordlist(file_path)
        
        if 'error' in analysis:
            return f"Error: {analysis['error']}"
        
        report = []
        report.append("=" * 60)
        report.append("WORDLIST ANALYSIS REPORT")
        report.append("=" * 60)
        
        # Basic Statistics
        report.append("\nBASIC STATISTICS:")
        report.append("-" * 20)
        stats = analysis['basic_stats']
        report.append(f"Total Passwords: {stats['total_passwords']:,}")
        report.append(f"Unique Passwords: {stats['unique_passwords']:,}")
        report.append(f"Duplicate Percentage: {stats['duplicate_percentage']:.2f}%")
        report.append(f"Average Length: {stats['average_length']}")
        report.append(f"Length Range: {stats['min_length']} - {stats['max_length']}")
        
        # Length Distribution
        report.append("\nLENGTH DISTRIBUTION:")
        report.append("-" * 20)
        length_dist = analysis['length_distribution']['categories']
        for category, count in length_dist.items():
            percentage = (count / stats['total_passwords'] * 100) if stats['total_passwords'] > 0 else 0
            report.append(f"{category.replace('_', ' ').title()}: {count:,} ({percentage:.1f}%)")
        
        # Pattern Analysis
        report.append("\nPATTERN ANALYSIS:")
        report.append("-" * 20)
        patterns = analysis['pattern_analysis']['pattern_matches']
        for pattern, data in patterns.items():
            report.append(f"{pattern.replace('_', ' ').title()}: {data['count']:,} ({data['percentage']:.1f}%)")
        
        # Strength Analysis
        report.append("\nSTRENGTH ANALYSIS:")
        report.append("-" * 20)
        strength = analysis['strength_analysis']
        report.append(f"Average Strength Score: {strength['average_strength']:.1f}/100")
        
        strength_dist = strength['strength_distribution']
        for category, count in strength_dist.items():
            percentage = (count / stats['total_passwords'] * 100) if stats['total_passwords'] > 0 else 0
            report.append(f"{category.replace('_', ' ').title()}: {count:,} ({percentage:.1f}%)")
        
        # Recommendations
        report.append("\nRECOMMENDATIONS:")
        report.append("-" * 20)
        for i, rec in enumerate(analysis['recommendations'], 1):
            report.append(f"{i}. {rec}")
        
        report_text = "\n".join(report)
        
        # Save to file if specified
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f"Report saved to: {output_file}")
            except Exception as e:
                print(f"Error saving report: {e}")
        
        return report_text
