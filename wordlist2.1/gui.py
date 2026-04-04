import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
import os
from wordlist import main_ganerator
import time
from datetime import datetime

class ModernWordlistGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordlist Generator Pro v2.0")
        
        # Set window size and position
        window_width = 1400
        window_height = 768
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1200, 800)
        
        # Modern color palette
        self.colors = {
            'bg_dark': '#0a0e27',
            'bg_medium': '#141b33',
            'bg_light': '#1e2a4a',
            'accent_primary': '#6c63ff',
            'accent_secondary': '#ff6584',
            'accent_success': '#00d26a',
            'accent_warning': '#ffaa00',
            'accent_error': '#ff4444',
            'text_primary': '#ffffff',
            'text_secondary': '#a0b3d9',
            'text_muted': '#5a6e8a',
            'border': '#2a3a5a'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Variables
        self.setup_variables()
        
        # Create GUI
        self.create_gui()
        
        # Animation variables
        self.loading = False
        
    def setup_variables(self):
        """Initialize all variables"""
        # Complexity
        self.complexity = tk.IntVar(value=2)
        
        # Length
        self.min_length = tk.IntVar(value=6)
        self.max_length = tk.IntVar(value=16)
        
        # Options
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=False)
        self.include_leet = tk.BooleanVar(value=False)
        self.include_dates = tk.BooleanVar(value=True)
        self.include_years = tk.BooleanVar(value=True)
        self.case_sensitive = tk.BooleanVar(value=True)
        
        # Advanced
        self.use_multithreading = tk.BooleanVar(value=True)
        self.thread_count = tk.IntVar(value=4)
        self.use_compression = tk.BooleanVar(value=False)
        self.estimate_size = tk.BooleanVar(value=True)
        
        # Export
        self.export_path = tk.StringVar(value="wordlist.txt")
        self.export_format = tk.StringVar(value="txt")
        
        # Year range
        self.year_start = tk.IntVar(value=1980)
        self.year_end = tk.IntVar(value=2024)
        
        # Number range
        self.number_start = tk.IntVar(value=0)
        self.number_end = tk.IntVar(value=9999)
        
        # Input data
        self.input_data = {
            'names': [],
            'keywords': [],
            'dates': [],
            'phones': [],
            'old_passwords': []
        }
        
    def create_gui(self):
        """Create the main GUI structure"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Content area (split into two columns)
        content_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Left panel - Input Section
        left_panel = self.create_left_panel(content_frame)
        
        # Right panel - Configuration & Output
        right_panel = self.create_right_panel(content_frame)
        
        # Footer
        self.create_footer(main_container)
        
    def create_header(self, parent):
        """Create modern header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_medium'])
        title_frame.pack(side=tk.LEFT, padx=30)
        
        # Icon (using text emoji for now)
        icon_label = tk.Label(title_frame, text="🔐", font=('Segoe UI', 36), 
                             bg=self.colors['bg_medium'], fg=self.colors['accent_primary'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        title_label = tk.Label(title_frame, text="WORDLIST GENERATOR PRO", 
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['bg_medium'], fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(title_frame, text="Advanced Password Intelligence Tool", 
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_medium'], fg=self.colors['text_secondary'])
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Stats panel
        stats_frame = tk.Frame(header_frame, bg=self.colors['bg_medium'])
        stats_frame.pack(side=tk.RIGHT, padx=30)
        
        self.stats_label = tk.Label(stats_frame, text="Ready to generate", 
                                   font=('Segoe UI', 11),
                                   bg=self.colors['bg_medium'], fg=self.colors['accent_success'])
        self.stats_label.pack()
        
    def create_left_panel(self, parent):
        """Create left panel with input sections"""
        left_frame = tk.Frame(parent, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=0)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas for scrolling
        canvas = tk.Canvas(left_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel binding
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        canvas.bind('<MouseWheel>', on_mousewheel)
        
        # Input sections
        self.create_input_section(scrollable_frame, "📝 Names", "names", 
                                 "Enter names (comma or line separated)")
        self.create_input_section(scrollable_frame, "🔑 Keywords", "keywords", 
                                 "Enter keywords (comma or line separated)")
        self.create_input_section(scrollable_frame, "📅 Dates", "dates", 
                                 "Enter dates (DD-MM-YYYY format)")
        self.create_input_section(scrollable_frame, "📞 Phone Numbers", "phones", 
                                 "Enter phone numbers")
        self.create_input_section(scrollable_frame, "🔐 Old Passwords", "old_passwords", 
                                 "Enter old passwords")
        
        return left_frame
    
    def create_input_section(self, parent, title, attr_name, placeholder):
        """Create a styled input section"""
        section_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        section_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Section header
        header_frame = tk.Frame(section_frame, bg=self.colors['bg_light'], height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text=title, font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['bg_light'], fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, padx=15)
        
        # Count label
        count_label = tk.Label(header_frame, text="0 items", font=('Segoe UI', 9),
                              bg=self.colors['bg_light'], fg=self.colors['text_secondary'])
        count_label.pack(side=tk.RIGHT, padx=15)
        
        # Text input area
        text_widget = tk.Text(section_frame, height=4, bg=self.colors['bg_dark'],
                             fg=self.colors['text_primary'], insertbackground=self.colors['accent_primary'],
                             font=('Consolas', 10), relief=tk.FLAT, bd=1,
                             highlightcolor=self.colors['accent_primary'],
                             highlightbackground=self.colors['border'])
        text_widget.pack(fill=tk.X, padx=1, pady=(0, 1))
        
        # Insert placeholder
        text_widget.insert('1.0', placeholder)
        text_widget.config(fg=self.colors['text_muted'])
        
        # Bind events
        def on_focus_in(event):
            if text_widget.get('1.0', 'end-1c') == placeholder:
                text_widget.delete('1.0', tk.END)
                text_widget.config(fg=self.colors['text_primary'])
        
        def on_focus_out(event):
            if not text_widget.get('1.0', 'end-1c').strip():
                text_widget.insert('1.0', placeholder)
                text_widget.config(fg=self.colors['text_muted'])
            else:
                # Update count
                content = text_widget.get('1.0', 'end-1c')
                items = [item.strip() for item in content.replace('\n', ',').split(',') if item.strip() and item.strip() != placeholder]
                count_label.config(text=f"{len(items)} items")
                self.input_data[attr_name] = items
        
        text_widget.bind('<FocusIn>', on_focus_in)
        text_widget.bind('<FocusOut>', on_focus_out)
        
        setattr(self, f"{attr_name}_text", text_widget)
        
    def create_right_panel(self, parent):
        """Create right panel with configuration and output"""
        right_frame = tk.Frame(parent, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=0)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Tab control
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure notebook style
        style = ttk.Style()
        style.configure('TNotebook', background=self.colors['bg_medium'])
        style.configure('TNotebook.Tab', background=self.colors['bg_light'], 
                       foreground=self.colors['text_primary'], padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', self.colors['accent_primary'])])
        
        # Configuration tab
        config_tab = tk.Frame(notebook, bg=self.colors['bg_medium'])
        notebook.add(config_tab, text="⚙️ Configuration")
        
        # Output tab
        output_tab = tk.Frame(notebook, bg=self.colors['bg_medium'])
        notebook.add(output_tab, text="📊 Output")
        
        # Populate tabs
        self.create_config_tab(config_tab)
        self.create_output_tab(output_tab)
        
        return right_frame
    
    def create_config_tab(self, parent):
        """Create configuration tab content"""
        # Canvas for scrolling
        canvas = tk.Canvas(parent, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Complexity section
        self.create_complexity_section(scrollable_frame)
        
        # Length section
        self.create_length_section(scrollable_frame)
        
        # Options section
        self.create_options_section(scrollable_frame)
        
        # Advanced section
        self.create_advanced_section(scrollable_frame)
        
        # Export section
        self.create_export_section(scrollable_frame)
        
        # Action buttons
        self.create_action_buttons(scrollable_frame)
        
    def create_complexity_section(self, parent):
        """Create complexity selection with modern cards"""
        section_frame = self.create_section_card(parent, "🎯 Complexity Level", 
                                                 "Higher complexity = More passwords but longer generation time")
        
        complexities = [
            (0, "Simple", "Basic patterns only", "🟢", "#00d26a"),
            (1, "Standard", "Common variations", "🔵", "#2196f3"),
            (2, "Advanced", "Complex patterns", "🟠", "#ff9800"),
            (3, "Expert", "Leet + mutations", "🔴", "#f44336"),
            (4, "Nuclear", "Everything possible", "💀", "#9c27b0")
        ]
        
        for i, (value, name, desc, emoji, color) in enumerate(complexities):
            card = tk.Frame(section_frame, bg=self.colors['bg_dark'], relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, padx=10, pady=5)
            
            rb = tk.Radiobutton(card, text=f"{emoji} {name}", variable=self.complexity, value=value,
                               bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_dark'], font=('Segoe UI', 10, 'bold'),
                               activebackground=self.colors['bg_dark'])
            rb.pack(side=tk.LEFT, padx=10, pady=10)
            
            desc_label = tk.Label(card, text=desc, bg=self.colors['bg_dark'], 
                                 fg=self.colors['text_secondary'], font=('Segoe UI', 8))
            desc_label.pack(side=tk.LEFT, padx=10)
            
            # Preview indicator
            preview = tk.Label(card, text=emoji, bg=self.colors['bg_dark'], fg=color, font=('Segoe UI', 16))
            preview.pack(side=tk.RIGHT, padx=10)
    
    def create_length_section(self, parent):
        """Create password length controls"""
        section_frame = self.create_section_card(parent, "📏 Password Length", 
                                                 "Set minimum and maximum password length")
        
        # Min length
        min_frame = tk.Frame(section_frame, bg=self.colors['bg_medium'])
        min_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(min_frame, text="Minimum:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        
        min_spinbox = tk.Spinbox(min_frame, from_=4, to=32, textvariable=self.min_length,
                                bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 10), width=10, relief=tk.FLAT)
        min_spinbox.pack(side=tk.LEFT, padx=10)
        
        # Max length
        max_frame = tk.Frame(section_frame, bg=self.colors['bg_medium'])
        max_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(max_frame, text="Maximum:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        
        max_spinbox = tk.Spinbox(max_frame, from_=4, to=64, textvariable=self.max_length,
                                bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 10), width=10, relief=tk.FLAT)
        max_spinbox.pack(side=tk.LEFT, padx=10)
        
        # Length warning
        self.length_warning = tk.Label(section_frame, text="", bg=self.colors['bg_medium'],
                                       fg=self.colors['accent_warning'], font=('Segoe UI', 8))
        self.length_warning.pack(pady=5)
        
        def update_warning(*args):
            if self.min_length.get() > self.max_length.get():
                self.length_warning.config(text="⚠️ Minimum length cannot exceed maximum length!")
                self.max_length.set(self.min_length.get())
            else:
                self.length_warning.config(text="")
        
        self.min_length.trace('w', update_warning)
        self.max_length.trace('w', update_warning)
    
    def create_options_section(self, parent):
        """Create options with toggle switches"""
        section_frame = self.create_section_card(parent, "🔧 Generation Options", 
                                                 "Toggle various password generation features")
        
        options = [
            ("Include Numbers (0-9)", self.include_numbers, "🔢"),
            ("Include Special Characters (!@#$%)", self.include_special, "✨"),
            ("Leet Speak Permutations", self.include_leet, "🔄"),
            ("Include Dates", self.include_dates, "📅"),
            ("Include Years (1980-2024)", self.include_years, "📆"),
            ("Case Sensitivity", self.case_sensitive, "🔠")
        ]
        
        for text, var, emoji in options:
            frame = tk.Frame(section_frame, bg=self.colors['bg_medium'])
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            cb = tk.Checkbutton(frame, text=f"{emoji} {text}", variable=var,
                               bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_medium'], font=('Segoe UI', 10),
                               activebackground=self.colors['bg_medium'])
            cb.pack(side=tk.LEFT)
    
    def create_advanced_section(self, parent):
        """Create advanced configuration section"""
        section_frame = self.create_section_card(parent, "⚡ Advanced Settings", 
                                                 "Performance optimization options")
        
        # Multi-threading
        thread_frame = tk.Frame(section_frame, bg=self.colors['bg_medium'])
        thread_frame.pack(fill=tk.X, padx=10, pady=5)
        
        mt_cb = tk.Checkbutton(thread_frame, text="🚀 Enable Multi-threading", variable=self.use_multithreading,
                              bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                              selectcolor=self.colors['bg_medium'], font=('Segoe UI', 10),
                              activebackground=self.colors['bg_medium'])
        mt_cb.pack(side=tk.LEFT)
        
        # Thread count
        thread_count_frame = tk.Frame(section_frame, bg=self.colors['bg_medium'])
        thread_count_frame.pack(fill=tk.X, padx=30, pady=5)
        
        tk.Label(thread_count_frame, text="Threads:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=5)
        
        thread_spinbox = tk.Spinbox(thread_count_frame, from_=1, to=16, textvariable=self.thread_count,
                                   bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                                   width=8, relief=tk.FLAT)
        thread_spinbox.pack(side=tk.LEFT, padx=10)
        
        # Additional options
        extra_frame = tk.Frame(section_frame, bg=self.colors['bg_medium'])
        extra_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Checkbutton(extra_frame, text="📊 Estimate Output Size", variable=self.estimate_size,
                      bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['bg_medium']).pack(anchor=tk.W)
        
        tk.Checkbutton(extra_frame, text="🗜️ Enable Compression (Save space)", variable=self.use_compression,
                      bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['bg_medium']).pack(anchor=tk.W)
    
    def create_export_section(self, parent):
        """Create export configuration"""
        section_frame = self.create_section_card(parent, "💾 Export Settings", 
                                                 "Configure output file format and location")
        
        # File path
        path_frame = tk.Frame(section_frame, bg=self.colors['bg_medium'])
        path_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(path_frame, text="File:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=5)
        
        path_entry = tk.Entry(path_frame, textvariable=self.export_path, 
                             bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                             font=('Consolas', 9), relief=tk.FLAT)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        browse_btn = tk.Button(path_frame, text="📂 Browse", command=self.browse_export_path,
                              bg=self.colors['accent_primary'], fg='white',
                              font=('Segoe UI', 9), relief=tk.FLAT, cursor='hand2')
        browse_btn.pack(side=tk.RIGHT)
        
        # Format selection
        format_frame = tk.Frame(section_frame, bg=self.colors['bg_medium'])
        format_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(format_frame, text="Format:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=5)
        
        formats = ['txt', 'csv', 'json', 'gz']
        for fmt in formats:
            rb = tk.Radiobutton(format_frame, text=fmt.upper(), variable=self.export_format, value=fmt,
                               bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_medium'])
            rb.pack(side=tk.LEFT, padx=10)
    
    def create_action_buttons(self, parent):
        """Create main action buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Generate button
        generate_btn = tk.Button(button_frame, text="🚀 GENERATE WORDLIST", 
                                command=self.generate_wordlist,
                                bg=self.colors['accent_primary'], fg='white',
                                font=('Segoe UI', 12, 'bold'), relief=tk.FLAT,
                                cursor='hand2', height=2)
        generate_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Save config button
        save_btn = tk.Button(button_frame, text="💾 Save Config", 
                            command=self.save_config,
                            bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                            font=('Segoe UI', 10), relief=tk.FLAT, cursor='hand2')
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Load config button
        load_btn = tk.Button(button_frame, text="📂 Load Config", 
                            command=self.load_config,
                            bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                            font=('Segoe UI', 10), relief=tk.FLAT, cursor='hand2')
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear all button
        clear_btn = tk.Button(button_frame, text="🗑️ Clear All", 
                             command=self.clear_all,
                             bg=self.colors['bg_light'], fg=self.colors['accent_error'],
                             font=('Segoe UI', 10), relief=tk.FLAT, cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def create_output_tab(self, parent):
        """Create output console tab"""
        # Console output
        self.console = tk.Text(parent, bg=self.colors['bg_dark'], fg='#00ff41',
                              font=('Consolas', 10), relief=tk.FLAT,
                              wrap=tk.WORD, padx=10, pady=10)
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.console, orient='vertical', command=self.console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.configure(yscrollcommand=scrollbar.set)
        
        # Progress bar
        self.progress_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        self.progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate',
                                           style='Accent.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X)
        
        # Configure progressbar style
        style = ttk.Style()
        style.configure('Accent.Horizontal.TProgressbar', 
                       background=self.colors['accent_primary'],
                       troughcolor=self.colors['bg_dark'])
    
    def create_footer(self, parent):
        """Create footer with status and info"""
        footer_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        # Status
        self.status_label = tk.Label(footer_frame, text="● Ready", 
                                    font=('Segoe UI', 9),
                                    bg=self.colors['bg_medium'], 
                                    fg=self.colors['accent_success'])
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Info
        info_label = tk.Label(footer_frame, text="© 2024 Wordlist Generator Pro | Advanced Password Intelligence Tool",
                             font=('Segoe UI', 8),
                             bg=self.colors['bg_medium'], 
                             fg=self.colors['text_muted'])
        info_label.pack(side=tk.RIGHT, padx=20)
    
    def create_section_card(self, parent, title, subtitle):
        """Create a styled section card"""
        card = tk.Frame(parent, bg=self.colors['bg_light'], relief=tk.FLAT, bd=1)
        card.pack(fill=tk.X, padx=10, pady=10)
        
        # Header
        header = tk.Frame(card, bg=self.colors['accent_primary'], height=35)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text=title, font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['accent_primary'], fg='white')
        title_label.pack(side=tk.LEFT, padx=15)
        
        # Subtitle
        if subtitle:
            sub_label = tk.Label(card, text=subtitle, font=('Segoe UI', 8),
                                bg=self.colors['bg_light'], fg=self.colors['text_muted'])
            sub_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Content frame
        content = tk.Frame(card, bg=self.colors['bg_light'])
        content.pack(fill=tk.X, padx=10, pady=10)
        
        return content
    
    def browse_export_path(self):
        """Browse for export file path"""
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{self.export_format.get()}",
            filetypes=[(f"{self.export_format.get().upper()} files", f"*.{self.export_format.get()}"),
                      ("All files", "*.*")]
        )
        if filename:
            self.export_path.set(filename)
    
    def generate_wordlist(self):
        """Generate wordlist based on configuration"""
        if self.loading:
            messagebox.showwarning("Warning", "Generation already in progress!")
            return
        
        # Collect input data
        for key in self.input_data:
            text_widget = getattr(self, f"{key}_text")
            content = text_widget.get('1.0', 'end-1c')
            if content and not content.startswith('Enter '):
                items = [item.strip() for item in content.replace('\n', ',').split(',') if item.strip()]
                self.input_data[key] = items
            else:
                self.input_data[key] = []
        
        # Start generation in thread
        self.loading = True
        thread = threading.Thread(target=self._generate_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_thread(self):
        """Background thread for wordlist generation"""
        try:
            self.update_ui_status("Generating...", 'warning', True)
            
            # Prepare generator parameters
            params = {
                'level': self.complexity.get(),
                'pwd_min': self.min_length.get(),
                'pwd_max': self.max_length.get(),
                'leeter': self.include_leet.get(),
                'chars': self.include_special.get(),
                'verbose': True,
                'export': self.export_path.get(),
                'threads': self.thread_count.get() if self.use_multithreading.get() else 1
            }
            
            # Create generator
            gen = main_ganerator(**params)
            
            # Set input data
            if self.input_data['names']:
                gen.names = gen.names(self.input_data['names'], complicated=gen.shit_level)
            if self.input_data['keywords']:
                gen.names.add_keywords(self.input_data['keywords'])
            if self.input_data['dates'] and self.include_dates.get():
                gen.dates = gen.dates(self.input_data['dates'], complicated=gen.shit_level)
            if self.input_data['phones']:
                gen.phones = gen.phones(self.input_data['phones'])
            if self.input_data['old_passwords']:
                gen.old_passwords = gen.old_passwords(self.input_data['old_passwords'], complicated=gen.shit_level)
            
            # Generate years if enabled
            if self.include_years.get():
                years = list(range(self.year_start.get(), self.year_end.get() + 1))
                gen.names.add_keywords([str(year) for year in years])
            
            # Generate numbers if enabled
            if self.include_numbers.get():
                numbers = list(range(self.number_start.get(), self.number_end.get() + 1))
                gen.names.add_keywords([str(num) for num in numbers])
            
            # Start generation
            start_time = time.time()
            gen.perms_generator()
            elapsed_time = time.time() - start_time
            
            # Display results
            self.log_message(f"\n{'='*60}")
            self.log_message(f"✅ GENERATION COMPLETED SUCCESSFULLY!")
            self.log_message(f"{'='*60}")
            self.log_message(f"📊 Total Passwords: {len(gen.total_result):,}")
            self.log_message(f"⏱️ Time Taken: {elapsed_time:.2f} seconds")
            self.log_message(f"💾 File Saved: {gen.export_file}")
            self.log_message(f"📏 File Size: {os.path.getsize(gen.export_file) / 1024 / 1024:.2f} MB")
            self.log_message(f"{'='*60}")
            
            self.update_ui_status("Completed", 'success', False)
            
        except Exception as e:
            self.log_message(f"❌ ERROR: {str(e)}", 'error')
            self.update_ui_status("Error", 'error', False)
        finally:
            self.loading = False
    
    def update_ui_status(self, message, status_type, show_progress):
        """Update UI status from background thread"""
        def _update():
            if status_type == 'warning':
                self.status_label.config(text=f"⚠️ {message}", fg=self.colors['accent_warning'])
                if show_progress:
                    self.progress_bar.start()
            elif status_type == 'success':
                self.status_label.config(text=f"✅ {message}", fg=self.colors['accent_success'])
                self.progress_bar.stop()
            elif status_type == 'error':
                self.status_label.config(text=f"❌ {message}", fg=self.colors['accent_error'])
                self.progress_bar.stop()
            else:
                self.status_label.config(text=f"● {message}", fg=self.colors['accent_success'])
                self.progress_bar.stop()
        
        self.root.after(0, _update)
    
    def log_message(self, message, msg_type='info'):
        """Log message to console"""
        def _log():
            timestamp = datetime.now().strftime("%H:%M:%S")
            if msg_type == 'error':
                self.console.insert(tk.END, f"[{timestamp}] ❌ {message}\n", 'error')
            elif msg_type == 'warning':
                self.console.insert(tk.END, f"[{timestamp}] ⚠️ {message}\n", 'warning')
            else:
                self.console.insert(tk.END, f"[{timestamp}] {message}\n", 'info')
            
            self.console.see(tk.END)
            
            # Configure tags for colors
            self.console.tag_config('error', foreground=self.colors['accent_error'])
            self.console.tag_config('warning', foreground=self.colors['accent_warning'])
            self.console.tag_config('info', foreground='#00ff41')
        
        self.root.after(0, _log)
    
    def save_config(self):
        """Save current configuration to file"""
        config = {
            'complexity': self.complexity.get(),
            'min_length': self.min_length.get(),
            'max_length': self.max_length.get(),
            'include_numbers': self.include_numbers.get(),
            'include_special': self.include_special.get(),
            'include_leet': self.include_leet.get(),
            'include_dates': self.include_dates.get(),
            'include_years': self.include_years.get(),
            'case_sensitive': self.case_sensitive.get(),
            'use_multithreading': self.use_multithreading.get(),
            'thread_count': self.thread_count.get(),
            'export_path': self.export_path.get(),
            'export_format': self.export_format.get(),
            'input_data': self.input_data
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.log_message(f"Configuration saved to {filename}")
    
    def load_config(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                
                # Load settings
                self.complexity.set(config.get('complexity', 2))
                self.min_length.set(config.get('min_length', 6))
                self.max_length.set(config.get('max_length', 16))
                self.include_numbers.set(config.get('include_numbers', True))
                self.include_special.set(config.get('include_special', False))
                self.include_leet.set(config.get('include_leet', False))
                self.include_dates.set(config.get('include_dates', True))
                self.include_years.set(config.get('include_years', True))
                self.case_sensitive.set(config.get('case_sensitive', True))
                self.use_multithreading.set(config.get('use_multithreading', True))
                self.thread_count.set(config.get('thread_count', 4))
                self.export_path.set(config.get('export_path', 'wordlist.txt'))
                self.export_format.set(config.get('export_format', 'txt'))
                
                # Load input data
                saved_data = config.get('input_data', {})
                for key, items in saved_data.items():
                    text_widget = getattr(self, f"{key}_text")
                    text_widget.delete('1.0', tk.END)
                    if items:
                        text_widget.insert('1.0', ', '.join(items))
                        text_widget.config(fg=self.colors['text_primary'])
                        self.input_data[key] = items
                
                messagebox.showinfo("Success", "Configuration loaded successfully!")
                self.log_message(f"Configuration loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
                self.log_message(f"Error loading configuration: {str(e)}", 'error')
    
    def clear_all(self):
        """Clear all input fields and reset settings"""
        if messagebox.askyesno("Confirm", "Clear all input data and reset settings?"):
            # Clear input fields
            for key in self.input_data:
                text_widget = getattr(self, f"{key}_text")
                text_widget.delete('1.0', tk.END)
                text_widget.insert('1.0', f"Enter {key.replace('_', ' ')}")
                text_widget.config(fg=self.colors['text_muted'])
                self.input_data[key] = []
            
            # Reset settings to default
            self.complexity.set(2)
            self.min_length.set(6)
            self.max_length.set(16)
            self.include_numbers.set(True)
            self.include_special.set(False)
            self.include_leet.set(False)
            self.include_dates.set(True)
            self.include_years.set(True)
            self.use_multithreading.set(True)
            self.thread_count.set(4)
            
            self.log_message("All settings cleared and reset to defaults")
            self.update_ui_status("Ready", 'success', False)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    # Create and run application
    app = ModernWordlistGUI(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit Wordlist Generator Pro?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()