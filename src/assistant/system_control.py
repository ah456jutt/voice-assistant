import subprocess
import webbrowser
import os
import pyautogui
import psutil
import random
from datetime import datetime
import time
from youtubesearchpython import VideosSearch
import urllib.parse
import requests
import json
from pytube import YouTube
from pytube import Search
from .system_monitor import SystemMonitor
from .health_monitor import HealthMonitor
import platform

class SystemController:
    def __init__(self):
        # Common websites dictionary
        self.websites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'gmail': 'https://mail.google.com',
            'netflix': 'https://www.netflix.com',
            'github': 'https://github.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://twitter.com',
            'linkedin': 'https://www.linkedin.com'
        }
        
        # Expand allowed CMD commands with descriptions
        self.cmd_commands = {
            # System information
            'systeminfo': 'Get detailed system information',
            'ver': 'Display Windows version',
            'hostname': 'Show computer name',
            'whoami': 'Show current user',
            
            # Network commands
            'ipconfig': 'Show network configuration',
            'netstat': 'Display network statistics',
            'ping': 'Test network connection',
            'tracert': 'Trace route to host',
            'nslookup': 'Query DNS records',
            
            # System utilities
            'tasklist': 'List running processes',
            'taskkill': 'Terminate a process',
            'dir': 'List directory contents',
            'tree': 'Display folder structure',
            'type': 'Display file contents',
            'findstr': 'Search text in files',
            
            # Power management
            'powercfg': 'Power configuration',
            'shutdown': 'Shutdown options',
            'logoff': 'Log off current user',
            
            # Network services
            'net': 'Network commands',
            'netsh': 'Network shell',
            'route': 'Show/manipulate network routing',
            
            # System management
            'sfc': 'System file checker',
            'chkdsk': 'Check disk',
            'diskpart': 'Disk partitioning',
            'defrag': 'Defragment drives',
            
            # User management
            'net user': 'User account management',
            'net group': 'Group management',
            
            # File operations
            'copy': 'Copy files',
            'move': 'Move files',
            'del': 'Delete files',
            'rd': 'Remove directory',
            'md': 'Make directory',
            'rename': 'Rename files'
        }

        # Add search engines
        self.search_engines = {
            'google': 'https://www.google.com/search?q={}',
            'bing': 'https://www.bing.com/search?q={}',
            'amazon': 'https://www.amazon.com/s?k={}',
            'shopping': 'https://shopping.google.com/search?q={}'
        }

        self.music_keywords = ['play', 'song', 'music', 'youtube']
        self.system_monitor = SystemMonitor()
        self.health_monitor = HealthMonitor()

        self.health_tips = [
            "Remember to maintain good posture, boss!",
            "Stay hydrated - drink some water!",
            "Take a 20-second eye break every 20 minutes.",
            "Stand up and stretch for a minute.",
            "Take deep breaths and relax your shoulders."
        ]

        self.system_info = platform.uname()

        # Add allowed CMD commands set
        self.allowed_commands = {
            'echo', 'dir', 'systeminfo', 'ipconfig', 'tasklist', 
            'ver', 'date', 'time', 'hostname', 'whoami',
            'type', 'path', 'ping', 'netstat', 'wmic',
            'net', 'powercfg'
        }

    def execute_basic_command(self, command):
        """Execute basic system commands"""
        try:
            # Create process with proper configurations
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # Get output with timeout
            stdout, stderr = process.communicate(timeout=10)
            
            # Combine output if available
            output = stdout or stderr
            if output:
                return f"Command output:\n{output.strip()}"
            return "Command executed successfully."
            
        except subprocess.TimeoutExpired:
            return "Command timed out after 10 seconds."
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def handle_command(self, command):
        command = command.lower().strip()
        
        # Handle direct system commands first
        base_command = command.split()[0]
        if base_command in self.cmd_commands or base_command in self.allowed_commands:
            return self.execute_basic_command(command)
        
        # Handle other commands
        elif "open" in command:
            return self.handle_website(command)
        elif any(word in command for word in ["date", "time", "today"]):
            if "time" in command:
                return self.get_time()
            return self.get_date()
        elif any(word in command for word in ["status", "info", "cpu", "memory"]):
            return self.handle_status_command(command)
        elif command in ["help", "commands", "show commands"]:
            return self.show_available_commands()
    
        return "Command not recognized. Type 'help' to see available commands."

    def handle_status_command(self, command):
        if "system" in command or "info" in command:
            return self.get_system_info()
        elif "cpu" in command:
            return self.get_cpu_info()
        elif "memory" in command or "ram" in command:
            return self.get_memory_info()
        elif "disk" in command or "storage" in command:
            return self.get_disk_info()
        return "Status command not recognized"

    def handle_website(self, command):
        site_name = command.replace('open', '').strip()
        if site_name in self.websites:
            webbrowser.open_new_tab(self.websites[site_name])
            return f"Opening {site_name}"
        return f"Website {site_name} not found in my list"

    def show_available_commands(self):
        """Show all available commands with descriptions"""
        output = "Available Commands:\n\n"
        for cmd, desc in self.cmd_commands.items():
            output += f"{cmd:<15} - {desc}\n"
        return output