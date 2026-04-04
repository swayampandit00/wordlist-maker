import threading
import queue
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import permutations, combinations, product
import psutil

class MultiThreadGenerator:
    def __init__(self, num_threads=None):
        self.num_threads = num_threads or min(4, psutil.cpu_count())
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.lock = threading.Lock()
        self.total_generated = 0
        self.stop_event = threading.Event()
    
    def generate_passwords_parallel(self, data_sources, min_length, max_length, 
                                  special_chars, export_file, verbose=False):
        """Generate passwords using multiple threads"""
        
        # Prepare data chunks for parallel processing
        data_chunks = self._prepare_data_chunks(data_sources, self.num_threads)
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            # Submit tasks to thread pool
            futures = []
            for i, chunk in enumerate(data_chunks):
                future = executor.submit(
                    self._generate_password_chunk,
                    chunk, min_length, max_length, special_chars, verbose, i
                )
                futures.append(future)
            
            # Collect results
            all_passwords = set()
            for future in as_completed(futures):
                try:
                    chunk_passwords = future.result()
                    with self.lock:
                        all_passwords.update(chunk_passwords)
                        self.total_generated += len(chunk_passwords)
                        
                        if verbose:
                            print(f"[Thread completed] Generated {len(chunk_passwords)} passwords")
                
                except Exception as e:
                    print(f"[!] Thread error: {e}")
        
        elapsed_time = time.time() - start_time
        
        # Export results
        self._export_passwords(all_passwords, export_file)
        
        return {
            'total_passwords': len(all_passwords),
            'elapsed_time': elapsed_time,
            'threads_used': self.num_threads
        }
    
    def _prepare_data_chunks(self, data_sources, num_chunks):
        """Divide data sources into chunks for parallel processing"""
        chunks = []
        
        # Split each data source into chunks
        for source_name, data_list in data_sources.items():
            if not data_list:
                continue
            
            chunk_size = max(1, len(data_list) // num_chunks)
            for i in range(num_chunks):
                start_idx = i * chunk_size
                end_idx = start_idx + chunk_size if i < num_chunks - 1 else len(data_list)
                chunk_data = data_list[start_idx:end_idx]
                
                if i >= len(chunks):
                    chunks.append({})
                
                chunks[i][source_name] = chunk_data
        
        return chunks
    
    def _generate_password_chunk(self, data_chunk, min_length, max_length, 
                                special_chars, verbose, thread_id):
        """Generate passwords for a specific data chunk"""
        passwords = set()
        
        # Extract data from chunk
        names = data_chunk.get('names', [])
        dates = data_chunk.get('dates', [])
        numbers = data_chunk.get('numbers', [])
        keywords = data_chunk.get('keywords', [])
        
        # Generate basic combinations
        passwords.update(self._generate_basic_combinations(names, dates, numbers, keywords, min_length, max_length))
        
        # Generate combinations with special characters
        if special_chars:
            passwords.update(self._generate_special_combinations(names, dates, numbers, keywords, special_chars, min_length, max_length))
        
        # Generate permutations
        passwords.update(self._generate_permutations(names, dates, numbers, keywords, min_length, max_length))
        
        if verbose:
            print(f"[Thread {thread_id}] Generated {len(passwords)} passwords")
        
        return passwords
    
    def _generate_basic_combinations(self, names, dates, numbers, keywords, min_length, max_length):
        """Generate basic password combinations"""
        passwords = set()
        
        # Single items
        for name in names:
            if min_length <= len(name) <= max_length:
                passwords.add(name)
        
        for date in dates:
            if min_length <= len(date) <= max_length:
                passwords.add(date)
        
        for number in numbers:
            if min_length <= len(str(number)) <= max_length:
                passwords.add(str(number))
        
        # Two-item combinations
        for name in names:
            for date in dates:
                pwd = name + date
                if min_length <= len(pwd) <= max_length:
                    passwords.add(pwd)
                
                pwd = date + name
                if min_length <= len(pwd) <= max_length:
                    passwords.add(pwd)
            
            for number in numbers:
                pwd = name + str(number)
                if min_length <= len(pwd) <= max_length:
                    passwords.add(pwd)
                
                pwd = str(number) + name
                if min_length <= len(pwd) <= max_length:
                    passwords.add(pwd)
            
            for keyword in keywords:
                pwd = name + keyword
                if min_length <= len(pwd) <= max_length:
                    passwords.add(pwd)
                
                pwd = keyword + name
                if min_length <= len(pwd) <= max_length:
                    passwords.add(pwd)
        
        return passwords
    
    def _generate_special_combinations(self, names, dates, numbers, keywords, special_chars, min_length, max_length):
        """Generate combinations with special characters"""
        passwords = set()
        
        # Add special characters to existing combinations
        base_passwords = self._generate_basic_combinations(names, dates, numbers, keywords, min_length - 1, max_length - 1)
        
        for pwd in base_passwords:
            for char in special_chars:
                # Prefix
                new_pwd = char + pwd
                if min_length <= len(new_pwd) <= max_length:
                    passwords.add(new_pwd)
                
                # Suffix
                new_pwd = pwd + char
                if min_length <= len(new_pwd) <= max_length:
                    passwords.add(new_pwd)
                
                # Middle
                if len(pwd) > 1:
                    mid = len(pwd) // 2
                    new_pwd = pwd[:mid] + char + pwd[mid:]
                    if min_length <= len(new_pwd) <= max_length:
                        passwords.add(new_pwd)
        
        return passwords
    
    def _generate_permutations(self, names, dates, numbers, keywords, min_length, max_length):
        """Generate permutations of data items"""
        passwords = set()
        
        # Permutations of 2 items
        all_items = names + dates + [str(n) for n in numbers] + keywords
        
        for perm in permutations(all_items, 2):
            pwd = ''.join(perm)
            if min_length <= len(pwd) <= max_length:
                passwords.add(pwd)
        
        # Permutations of 3 items (limited to avoid explosion)
        if len(all_items) <= 10:  # Limit to reasonable size
            for perm in permutations(all_items, 3):
                pwd = ''.join(perm)
                if min_length <= len(pwd) <= max_length:
                    passwords.add(pwd)
        
        return passwords
    
    def _export_passwords(self, passwords, export_file):
        """Export passwords to file"""
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                for pwd in sorted(passwords):
                    f.write(pwd + '\n')
        except Exception as e:
            print(f"[!] Error exporting passwords: {e}")
    
    def get_optimal_thread_count(self):
        """Get optimal thread count based on system resources"""
        cpu_count = psutil.cpu_count()
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # Adjust thread count based on available memory
        if memory_gb < 4:
            return min(2, cpu_count)
        elif memory_gb < 8:
            return min(4, cpu_count)
        else:
            return min(8, cpu_count)
    
    def stop_generation(self):
        """Stop password generation"""
        self.stop_event.set()
    
    def get_progress(self):
        """Get generation progress"""
        return {
            'total_generated': self.total_generated,
            'is_running': not self.stop_event.is_set()
        }
