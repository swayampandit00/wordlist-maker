import psutil
import sys
import time
import click
import os
from perm_classes import *
from utils import *
from multilang import MultiLanguageSupport
from patterns import PatternTemplates
from config_manager import ConfigManager
from multithread import MultiThreadGenerator
from analyzer import WordlistAnalyzer


class main_ganerator:
	def __init__(self, level=0, pwd_min=8, pwd_max=12, num_range=0,
				 leeter=False, years=0, chars=True, verbose=True, export='passwords.txt',
				 languages=None, templates=None, threads=4):
		# Complication levels:
		# 0 = default
		# 1 = 0 + allowing more permutations in perm_classes
		# 2 = 1 + allowing more permutations in old passwords perm class
		# 3 = 2 + Using the whole special chars set allowed in passwords
		# 4 = 3 + Use more permutations in the main function
		# 5 = 4 + Don't use ordered pairs for perm function
		# if you want more, enable the leeter it's level 666 lol!
		self.shit_level   = level
		self.verbose_mode = verbose
		# Initialize new features
		self.multilang = MultiLanguageSupport()
		self.patterns = PatternTemplates()
		self.config_manager = ConfigManager()
		self.multithread = MultiThreadGenerator(threads)
		self.analyzer = WordlistAnalyzer()
		
		# Set language support
		if languages:
			self.multilang.add_language_support(languages)
		
		# Okay lesgooo!
		self.names = names_perm
		self.dates = dates_perm
		self.phones = phones_perm
		self.old_passwords = oldpwds
		self.total_result = []
		# Password length variables
		self.minimum_length = pwd_min
		self.maximum_length = pwd_max
		# Deepness level
		# For banner and checking
		self.number_range = f"{B}{num_range}{reset + W}" if num_range != 0 else f"{R}False{reset + W}"
		self.years_range = f"{B}{years}-{time.localtime().tm_year + 1}{reset + W}" if years != 0 else f"{R}False{reset + W}"
		if chars:
			self.special_chars = f"{B}All chars{reset + W}" if self.shit_level >= 3 else f"{B}Common chars{reset + W}"
		else:
			self.special_chars = f"{R}False{reset + W}"
		self.leeting = f"{B}Enabled{reset + W}" if leeter else f"{R}Disabled{reset + W}"
		# For looping
		self.recipes = [[]]
		if num_range != 0:
			self.recipes.append(data_plus.nums_range(num_range))
		if years != 0:
			self.recipes.append(data_plus.years(years))
		if chars:
			if self.shit_level >= 3:
				self.recipes.append(data_plus.chars)
			else:
				self.recipes.append(("_", ".", "-", "!", "@", "*", "$", "?", "&",
									 "%"))  # Common special chars according to this thread (https://www.reddit.com/r/dataisbeautiful/comments/2vfgvh/most_frequentlyused_special_characters_in_10/)
		self.add_leet_perms = leeter
		self.export_file = export
		self.templates = templates or []
		self.threads = threads

	def __input(self, prompt):
		result = []
		while True:
			# A workaround because colorama for some reason not print colored texts with input() !!
			print(f"{G}[{reset + B}>{reset + G}] {prompt}{reset}", end="")
			data = input()
			print(f"{reset}", end="")
			if data:
				if " " in data.strip():
					data = data.split(" ")
				else:
					data = [data]
				for part in data:
					for smaller_part in part.split(","):
						if smaller_part:
							result.append(smaller_part)
			return result

	def __pwd_check(self, pwd):
		if (len(pwd) >= self.minimum_length) and (len(pwd) <= self.maximum_length) and (pwd not in self.total_result):
			return True
		return False

	def __simple_perm(self, target, *groups):
		for pair in zip(*groups, fillvalue=""):
			for targeted in target:
				pair = (targeted,) + pair
				for addition in self.recipes:
					yield ("".join(pair + (added,)) for added in addition)

	def __commonPerms(self):
		# Just to make sure common perms are in permutations
		for name in self.names.words:
			if self.__pwd_check(name):
				self.total_result.append(name)
		for date in self.dates.joined_dates:
			if self.__pwd_check(date):
				self.total_result.append(date)
			for thing in [self.names.words, self.names.one, self.names.two]:
				for justone in thing:
					if self.__pwd_check(justone + date):
						self.total_result.append(justone + date)
		for national_number in self.phones.national:
			if self.__pwd_check(national_number):
				self.total_result.append(national_number)
			for thing in [self.names.words, self.names.one, self.names.two]:
				for justone in thing:
					if self.__pwd_check(justone + national_number):
						self.total_result.append(justone + national_number)

	def __perm(self, target, *groups, perm_length=None):
		# Return all the permutations of a combined iterators/generators
		if groups:
			perm_length = perm_length if perm_length else len(groups) + 1
			if self.shit_level >= 5:
				# You want more results,
				#      don't wanna skip any possible permutation,
				#          and you don't mind more unrealistic results?
				#              Then you came for the right place :laughing:
				for pair in ((target, pair2) for pair2 in groups):
					for addition in self.recipes:
						iterator = chain.from_iterable(pair + (addition,))
						yield ("".join(p) for p in perm(iterator, perm_length) if
							   (self.__pwd_check("".join(p)) and not ("".join(p)).isdecimal()))
			else:
				# If you want things not complicated for more realistic results, use ordered pairs like this
				# Maybe I'm wrong? PR with what you think is best realistic result without chaos :)
				for targeted in target:
					for pair in (((targeted,) + pairs) for pairs in zip(*groups, fillvalue="")):
						for addition in self.recipes:
							if not addition:
								yield ("".join(p) for p in perm(pair, perm_length) if
									   (self.__pwd_check("".join(p)) and not ("".join(p)).isdecimal()))
							else:
								for added in addition:
									# iterator = chain.from_iterable(pair+(added,))
									iterator = pair + (added,)
									yield ("".join(p) for p in perm(iterator, perm_length) if
										   (self.__pwd_check("".join(p)) and not ("".join(p)).isdecimal()))

	def __perms(self, *main_group, others, perm_length=None):
		# Return the combined permutations of (main_group, other_group)
		# Written this one to make the code cleaner instead of writting self.__perm many times
		iters = []
		for other_group in others:
			iters.append(self.__perm(*main_group, other_group, perm_length=perm_length))
		iters.append(self.__perm(*main_group, *others, perm_length=perm_length))
		return chain.from_iterable(iters)

	def __export(self):
		# Line by line is slower but memeory efficient (very large results could not fit in your ram)
		if self.total_result:
			sys.stdout.write(f"[~] Exporting results to {self.export_file}...\r")
			sys.stdout.flush()
			with open(self.export_file, 'w') as f:
				for pwd in self.total_result:
					f.write(f"{pwd}\n")
			print(f"[+] Results exported to {self.export_file}!")

	def perms_generator(self):
		# Common passwords before starting the permutations
		self.__commonPerms()
		
		# Add pattern-based passwords if templates are specified
		if self.templates:
			print("[~] Generating pattern-based passwords...")
			data_dict = {
				'names': self.names.words,
				'dates': self.dates.joined_dates,
				'numbers': [str(i) for i in range(1000)],
				'keywords': getattr(self.names, 'keywords', [])
			}
			
			for template in self.templates:
				pattern_passwords = self.patterns.generate_from_template(template, data_dict)
				for pwd in pattern_passwords:
					if self.__pwd_check(pwd):
						self.total_result.append(pwd)
						if self.verbose_mode:
							sys.stdout.write(f"[~] Pattern generation: {pwd : <25} [N:{len(self.total_result) :_<10}]\r")
							sys.stdout.flush()
		
		# Now let's start the permutations
		mixes = [
			# names only
			self.__simple_perm(self.names.words, ),
			# names and dates mixes
			self.__perms(self.names.words, others=(self.dates.days, self.dates.months, self.dates.years), ),
			# names and phones mixes
			self.__perm(self.names.one, self.dates.joined_dates, ),
			self.__perm(self.names.two, self.dates.joined_dates, ),
			self.__perms(self.names.words,
						 others=(self.phones.national, self.phones.first_four, self.phones.last_four), ),
			self.__perm(self.names.one, self.phones.national, ),
			self.__perm(self.names.two, self.phones.national, ),
			self.__perms(self.names.one, others=(self.phones.first_four, self.phones.last_four), ),
			self.__perms(self.names.two, others=(self.phones.first_four, self.phones.last_four), ),
			# names, dates and phones
			self.__perm(self.names.words, self.dates.years, self.phones.first_four, ),
			self.__perm(self.names.words, self.dates.years, self.phones.last_four, ),
			self.__perm(self.names.words, self.dates.years, self.phones.national, )]
		# Now for the mixes based on old passwords
		if self.old_passwords.passwords:
			for pwd in self.old_passwords.passwords:
				# Here we will not get all permutations because people tend to just append new things to old passwords without changing a lot!
				for iterator in (data_plus.nums_range(100), data_plus.years(1900), data_plus.chars,):
					mixes.append(
						("".join(p) for one in iterator for p in perm((pwd, one), 2) if self.__pwd_check("".join(p))))
			mixes.append(self.__perm(self.old_passwords.passwords, self.names.words, ))
			mixes.append(self.__perms(self.old_passwords.passwords,
									  others=(self.dates.days, self.dates.months, self.dates.years), ))
			mixes.append(self.__perms(self.old_passwords.passwords,
									  others=(self.phones.national, self.phones.first_four, self.phones.last_four), ))
		#######################################################################
		# More complicated not very common or realistic
		if self.shit_level >= 4:
			# names and dates
			mixes.append(self.__perm(self.names.words, self.dates.days, self.dates.months, self.dates.years))
			mixes.append(self.__perm(self.names.one, self.names.two, self.dates.joined_dates))
			# names and phones
			mixes.append(self.__perm(self.names.words, self.phones.first_four, self.phones.last_four))
			mixes.append(self.__perm(self.names.one, self.names.two, self.phones.national))
			mixes.append(self.__perm(self.names.one, self.names.two, self.phones.first_four, self.phones.last_four, ))
			# names, dates and phones
			mixes.append(
				self.__perm(self.names.words, self.dates.years, self.phones.first_four, self.phones.last_four, ))
			mixes.append(self.__perm(self.names.words, self.dates.days, self.dates.months, self.phones.national, ))
			# phones, dates...etc numbers only different variations
			mixes.append(self.__perm(self.dates.days, self.dates.months, self.dates.years, ))
			mixes.append(self.__perm(self.phones.national, self.dates.years, ))
			mixes.append(self.__perm(self.phones.first_four, self.phones.last_four, self.dates.years, ))
		######################
		sys.stdout.write("[~] Generating passwords...\r")
		sys.stdout.flush()
		for generator in chain.from_iterable(mixes):
			for pwd in generator:
				if self.__pwd_check(pwd):
					# Apply multi-language filtering if enabled
					pwd = self.multilang.filter_text(pwd)
					if pwd:  # Only add if not filtered out
						self.total_result.append(pwd)
						if self.verbose_mode:
							sys.stdout.write(f"[~] Generating passwords: {pwd : <25} [N:{len(self.total_result) :_<10}]\r")
							sys.stdout.flush()

		print(f"[+] Total number: {str(len(self.total_result))+' password(s)': <40}")
		self.__export()
		if self.add_leet_perms:
			print("[~] Now making new file with leet permutations for each generated password...")
			del self.total_result[:]
			self.total_result = []
			with open(self.export_file, 'r') as data:
				for pwd in data:
					self.total_result.extend(data_plus.leet_perm(pwd.strip()))
			self.export_file = "Leeted-"+self.export_file
			print(f"[+] Total number of leeted passwords: {len(self.total_result)} password(s)")
			self.__export()
	
	def generate_with_multithreading(self, data_sources):
		"""Generate passwords using multi-threading"""
		print(f"[~] Using {self.threads} threads for parallel generation...")
		
		special_chars = []
		if self.recipes:
			for recipe in self.recipes:
				special_chars.extend(recipe)
		
		result = self.multithread.generate_passwords_parallel(
			data_sources=data_sources,
			min_length=self.minimum_length,
			max_length=self.maximum_length,
			special_chars=special_chars,
			export_file=self.export_file,
			verbose=self.verbose_mode
		)
		
		print(f"[+] Multi-threaded generation completed!")
		print(f"[+] Total passwords: {result['total_passwords']:,}")
		print(f"[+] Time elapsed: {result['elapsed_time']:.2f}s")
		print(f"[+] Threads used: {result['threads_used']}")
		
		return result
	
	def analyze_wordlist(self, wordlist_file=None):
		"""Analyze generated wordlist"""
		if not wordlist_file:
			wordlist_file = self.export_file
		
		if not os.path.exists(wordlist_file):
			print(f"[!] Wordlist file not found: {wordlist_file}")
			return
		
		print(f"[~] Analyzing wordlist: {wordlist_file}")
		report = self.analyzer.generate_report(wordlist_file)
		print(report)
		
		# Save analysis report
		report_file = wordlist_file.replace('.txt', '_analysis.txt')
		try:
			with open(report_file, 'w', encoding='utf-8') as f:
				f.write(report)
			print(f"[+] Analysis report saved to: {report_file}")
		except Exception as e:
			print(f"[!] Error saving analysis report: {e}")
	
	def save_config(self, filename):
		"""Save current configuration"""
		config = {
			'level': self.shit_level,
			'min_length': self.minimum_length,
			'max_length': self.maximum_length,
			'num_range': int(self.number_range.replace(f"{B}", "").replace(f"{reset + W}", "")) if self.number_range != f"{R}False{reset + W}" else 0,
			'years': int(self.years_range.split('-')[0]) if self.years_range != f"{R}False{reset + W}" else 0,
			'chars': self.special_chars != f"{R}False{reset + W}",
			'leet': self.leeting != f"{R}Disabled{reset + W}",
			'verbose': self.verbose_mode,
			'export_file': self.export_file,
			'templates': self.templates,
			'threads': self.threads
		}
		
		if self.config_manager.export_config(config, filename):
			print(f"[+] Configuration saved to: {filename}")
		else:
			print(f"[!] Error saving configuration")
	
	def load_config(self, filename):
		"""Load configuration from file"""
		config = self.config_manager.import_config(filename)
		
		if config:
			self.shit_level = config.get('level', 0)
			self.minimum_length = config.get('min_length', 8)
			self.maximum_length = config.get('max_length', 12)
			self.verbose_mode = config.get('verbose', False)
			self.export_file = config.get('export_file', 'passwords.txt')
			self.templates = config.get('templates', [])
			self.threads = config.get('threads', 4)
			
			print(f"[+] Configuration loaded from: {filename}")
			return True
		else:
			print(f"[!] Error loading configuration")
			return False

	def __print_banner(self):
		with open("banner.txt", encoding='utf-8') as f:
			banner_text = f.read()
			print(W + banner_text.format(
				ver=f"{reset}{B}2.0{reset}{W}",
				num=self.number_range, year=self.years_range,
				chars=self.special_chars,
				leet=self.leeting,
				min=f"{reset}{B}{self.minimum_length}{reset}{G}", max=f"{reset}{B}{self.maximum_length}{reset}{G}",
				verbose={
					True: f"{B}Enabled{reset + W}",
					False: f"{R}Disabled{reset + W}"
				}[self.verbose_mode], export=f"{B}{self.export_file}{reset + W}",
				# 0 = default
				# 1 = 0 + allowing more permutations in perm_classes
				# 2 = 1 + allowing more permutations in old passwords perm class
				# 3 = 2 + Using the whole special chars set allowed in passwords
				# 4 = 3 + Don't use ordered pairs for perm function
				# 5 = 4 + Use more permutations in the main function
				level=reset+C+{
					0: "Simple person",
					1: "Average person",
					2: "Cyber awareness ",
					3: "Paranoid person",
					4: "Nerd person",
					5: "Nuclear!",
				}[self.shit_level]+reset+G,
				G=G, end=reset + W
			) + reset)
		print(f"\n{G}Generation Recipes:{W}")
		print(f"{G}Number range  : {W}{self.number_range}, {G}Years range: {W}{self.years_range}")
		print(f"{G}Special chars : {W}{self.special_chars}, {G}Leet permutations: {W}{self.leeting}")
		print(f"{G}Verbose mode : {W}{'Enabled' if self.verbose_mode else 'Disabled'}, {G}Export file : {W}{self.export_file}")
		print(f"{G}Password stats: Min={self.minimum_length} Max={self.maximum_length} Complication level set for: {['Simple person', 'Average person', 'Cyber awareness', 'Paranoid person', 'Nerd person', 'Nuclear!'][self.shit_level]}{reset}")

	def interface(self):
		self.__print_banner()
		self.names = self.names(self.__input("Any names (No spaces, comma seperated): "),
								complicated=self.shit_level)
		self.names.add_keywords(
			self.__input("Any keywords like nicknames, job, movies, series... (No spaces, comma seperated): "))
		self.dates = self.dates(
			self.__input("Any birthdays or dates you know (Format: [dd-mm-yyyy], comma seperated): "),
			complicated=self.shit_level)
		self.phones = self.phones(
			self.__input("Any phone numbers you know (Format: [+Countrycodexxx...], comma seperated): "))
		self.old_passwords = self.old_passwords(
			self.__input("Old passwords or words you think new passwords will be made out of it (comma seperated): "),
			complicated=self.shit_level)
		start_time = time.time()
		try:
			self.perms_generator()
		except KeyboardInterrupt:
			print('[!] Detected Keyboard interruption(Ctrl+C)! Exiting...')
			self.__export()
		finally:
			process = psutil.Process(os.getpid())
			elapsed = round(time.time()-start_time, 2)
			if elapsed >= 60:
				elapsed /= 60
				elapsed = str(round(elapsed, 2))+"m"
			else:
				elapsed = str(elapsed)+"s"
			# usage in megabytes
			print(f"[+] Elapsed time {elapsed} - Memory usage (rss:{round(process.memory_info().rss / 1024 ** 2, 2)}MB vms:{round(process.memory_info().vms / 1024 ** 2, 2)}MB)")
			sys.exit(0)


@click.command()
@click.option('-l', '--level', metavar='', type=click.Choice(['0', '1', '2', '3', '4', '5']), default='0', 
              help='🔧 Complexity level (0=Simple, 1=Average, 2=Cyber Aware, 3=Paranoid, 4=Nerd, 5=Nuclear!)')
@click.option('--min', 'pmin', metavar='', type=int, default=8, help='📏 Minimum password length (Default:8)')
@click.option('--max', 'pmax', metavar='', type=int, default=12, help='📏 Maximum password length (Default:12)')
@click.option('-r', '--num-range', metavar='', type=int, default=0, help='🔢 Number range (0 to N, Default:0)')
@click.option('--leet', metavar='', is_flag=True, default=False, help='🔄 Generate leet permutations')
@click.option('-y', '--years', metavar='', type=int, default=0, help='📅 Include years from N to current (Default:0)')
@click.option('-c', '--chars', metavar='', is_flag=True, default=False, help='!@# Add special characters')
@click.option('-v', '--verbose', metavar='', is_flag=True, default=False, help='📢 Show generation progress (slower)')
@click.option('-x', '--export', metavar='', type=str, default='passwords.txt', help='💾 Output filename (Default:passwords.txt)')
@click.option('--languages', metavar='', type=str, help='🌍 Multi-language support (hindi,arabic,chinese,japanese,russian,european)')
@click.option('--templates', metavar='', type=str, help='📋 Pattern templates (common,corporate,personal,gaming,social)')
@click.option('--threads', metavar='', type=int, default=4, help='⚡ Thread count for multi-threading (Default:4)')
@click.option('--multithread', is_flag=True, default=False, help='🚀 Enable multi-threaded generation')
@click.option('--analyze', is_flag=True, default=False, help='📊 Analyze wordlist after generation')
@click.option('--save-config', metavar='', type=str, help='💾 Save configuration to JSON file')
@click.option('--load-config', metavar='', type=str, help='📂 Load configuration from JSON file')
@click.option('--help-advanced', is_flag=True, default=False, help='📖 Show advanced usage examples')
def main(level, pmin, pmax, num_range, leet, years, chars, verbose, export, languages, templates, threads, multithread, analyze, save_config, load_config, help_advanced):
	# Show advanced help if requested
	if help_advanced:
		print_advanced_help()
		return
	
	# Parse languages and templates
	languages_list = languages.split(',') if languages else None
	templates_list = templates.split(',') if templates else None
	
	gen = main_ganerator(int(level), pmin, pmax, num_range, leet, years, chars, verbose, export, languages_list, templates_list, threads)
	
	# Load config if specified
	if load_config:
		if gen.load_config(load_config):
			# Update parameters from loaded config
			level = str(gen.shit_level)
			pmin = gen.minimum_length
			pmax = gen.maximum_length
			num_range = int(gen.number_range.replace(f"{B}", "").replace(f"{reset + W}", "")) if gen.number_range != f"{R}False{reset + W}" else 0
			years = int(gen.years_range.split('-')[0]) if gen.years_range != f"{R}False{reset + W}" else 0
			chars = gen.special_chars != f"{R}False{reset + W}"
			leet = gen.leeting != f"{R}Disabled{reset + W}"
			verbose = gen.verbose_mode
			export = gen.export_file
			templates_list = gen.templates
			threads = gen.threads
	
	# Save config if specified
	if save_config:
		gen.save_config(save_config)
		return
	
	# Run interface or direct generation
	if multithread:
		# Prepare data sources for multi-threading
		data_sources = {
			'names': [],
			'dates': [],
			'numbers': [],
			'keywords': []
		}
		
		# Get input data
		names_input = gen.__input("Any names (No spaces, comma seperated): ")
		data_sources['names'] = names_input
		
		keywords_input = gen.__input("Any keywords like nicknames, job, movies, series... (No spaces, comma seperated): ")
		data_sources['keywords'] = keywords_input
		
		dates_input = gen.__input("Any birthdays or dates you know (Format: [dd-mm-yyyy], comma seperated): ")
		data_sources['dates'] = dates_input
		
		phones_input = gen.__input("Any phone numbers you know (Format: [+Countrycodexxx...], comma seperated): ")
		data_sources['numbers'] = phones_input
		
		oldpwds_input = gen.__input("Old passwords or words you think new passwords will be made out of it (comma seperated): ")
		data_sources['old_passwords'] = oldpwds_input
		
		# Generate with multi-threading
		start_time = time.time()
		try:
			result = gen.generate_with_multithreading(data_sources)
		except KeyboardInterrupt:
			print('[!] Detected Keyboard interruption(Ctrl+C)! Exiting...')
			return
		finally:
			elapsed = round(time.time() - start_time, 2)
			process = psutil.Process(os.getpid())
			if elapsed >= 60:
				elapsed /= 60
				elapsed = str(round(elapsed, 2))+"m"
			else:
				elapsed = str(elapsed)+"s"
			print(f"[+] Elapsed time {elapsed} - Memory usage (rss:{round(process.memory_info().rss / 1024 ** 2, 2)}MB vms:{round(process.memory_info().vms / 1024 ** 2, 2)}MB)")
	else:
		# Use original interface
		gen.interface()
	
	# Analyze wordlist if requested
	if analyze:
		gen.analyze_wordlist()

def print_advanced_help():
	"""Print advanced usage examples"""
	print(f"""
{G}╔══════════════════════════════════════════════════════════════╗
{G}║                    🔥 WORDLIST-MAKER 🔥                      ║
{G}║                 Advanced Usage Examples                        ║
{G}╚══════════════════════════════════════════════════════════════╝{W}

{B}📚 BEGINNER EXAMPLES:{W}
{G}1. Basic wordlist:{W}
   python wordlist.py

{G}2. Simple with custom length:{W}
   python wordlist.py --min 6 --max 10

{G}3. With numbers and years:{W}
   python wordlist.py -r 999 -y 2000

{B}🚀 INTERMEDIATE EXAMPLES:{W}
{G}4. Special characters and leet:{W}
   python wordlist.py -c --leet --export advanced_passwords.txt

{G}5. Higher complexity level:{W}
   python wordlist.py -l 3 -c --leet

{G}6. Multi-language support:{W}
   python wordlist.py --languages hindi,arabic

{B}⚡ ADVANCED EXAMPLES:{W}
{G}7. Pattern templates:{W}
   python wordlist.py --templates common,corporate,personal

{G}8. Multi-threaded generation:{W}
   python wordlist.py --multithread --threads 8

{G}9. Full advanced setup:{W}
   python wordlist.py -l 5 --min 8 --max 16 -r 9999 -y 1990 -c --leet \\
   --templates common,corporate,gaming --languages hindi,chinese \\
   --multithread --threads 8 --analyze

{G}10. Configuration management:{W}
   # Save config
   python wordlist.py --save-config my_setup.json
   
   # Load config
   python wordlist.py --load-config my_setup.json

{B}🎯 SPECIFIC USE CASES:{W}
{G}Corporate Environment:{W}
   python wordlist.py --templates corporate -l 3 -c --years 2010

{G}Gaming Accounts:{W}
   python wordlist.py --templates gaming --multithread --threads 6

{G}Personal Passwords:{W}
   python wordlist.py --templates personal -l 2 --years 1995

{G}Multi-language Target:{W}
   python wordlist.py --languages european,russian,chinese -l 4

{B}📊 ANALYSIS EXAMPLES:{W}
{G}Generate and analyze:{W}
   python wordlist.py --analyze --templates common

{G}Analyze existing wordlist:{W}
   python -c "from wordlist import main_ganerator; gen=main_ganerator(); gen.analyze_wordlist('passwords.txt')"

{B}💡 PRO TIPS:{W}
{G}• Use --multithread for faster generation with large datasets
{G}• Combine templates for better coverage
{G}• Higher levels (-l 4,5) generate more but take longer
{G}• Use --analyze to understand wordlist quality
{G}• Save configurations for repeated use cases
{G}• GUI available: python gui.py{W}

{B}🔧 CONFIGURATION PRESETS:{W}
{G}• Quick: -l 1 --min 6 --max 10
{G}• Standard: -l 2 --min 8 --max 12 -c
{G}• Advanced: -l 3 --min 10 --max 16 -c --leet
{G}• Maximum: -l 5 --min 12 --max 20 -c --leet --multithread{W}

{G}For more help, run: python wordlist.py --help{W}
""")


if __name__ == '__main__':
	main()
