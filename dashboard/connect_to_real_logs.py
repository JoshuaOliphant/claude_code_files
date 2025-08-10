#!/usr/bin/env python3
"""
Connect Claude Code Analytics Dashboard to real log files.
Supports multiple connection methods and real-time monitoring.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Optional
import click
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogSyncHandler(FileSystemEventHandler):
    """Sync logs when source files change"""
    
    def __init__(self, source: Path, dest: Path):
        self.source = source
        self.dest = dest
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            # Copy modified file to dashboard
            src_file = Path(event.src_path)
            dest_file = self.dest / src_file.name
            shutil.copy2(src_file, dest_file)
            print(f"✅ Synced: {src_file.name}")

class DashboardConnector:
    """Manages connection between dashboard and real logs"""
    
    def __init__(self):
        self.dashboard_logs = Path("/workdir/dashboard/logs")
        self.config_file = Path("/workdir/dashboard/config.yaml")
    
    def connect_symlink(self, source_path: str) -> bool:
        """Create symlink to real logs (best for local)"""
        source = Path(source_path).expanduser().resolve()
        
        if not source.exists():
            print(f"❌ Source path doesn't exist: {source}")
            return False
        
        # Remove existing logs
        if self.dashboard_logs.exists():
            if self.dashboard_logs.is_symlink():
                self.dashboard_logs.unlink()
            else:
                shutil.rmtree(self.dashboard_logs)
        
        # Create symlink
        self.dashboard_logs.symlink_to(source)
        print(f"✅ Symlinked: {self.dashboard_logs} -> {source}")
        return True
    
    def connect_copy(self, source_path: str, watch: bool = False) -> bool:
        """Copy logs to dashboard (works everywhere)"""
        source = Path(source_path).expanduser().resolve()
        
        if not source.exists():
            print(f"❌ Source path doesn't exist: {source}")
            return False
        
        # Ensure destination exists
        self.dashboard_logs.mkdir(parents=True, exist_ok=True)
        
        # Copy all JSON files
        copied = 0
        for json_file in source.glob("*.json"):
            dest_file = self.dashboard_logs / json_file.name
            shutil.copy2(json_file, dest_file)
            copied += 1
        
        print(f"✅ Copied {copied} log files to dashboard")
        
        if watch:
            # Set up file watching
            print("👁️  Watching for changes...")
            event_handler = LogSyncHandler(source, self.dashboard_logs)
            observer = Observer()
            observer.schedule(event_handler, str(source), recursive=False)
            observer.start()
            
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
        
        return True
    
    def connect_mount(self, source_path: str) -> bool:
        """Generate Docker mount configuration"""
        source = Path(source_path).expanduser()
        
        docker_compose = {
            'version': '3.8',
            'services': {
                'dashboard': {
                    'build': '.',
                    'ports': ['8000:8000'],
                    'volumes': [f'{source}:/workdir/dashboard/logs:ro'],
                    'environment': ['LOGS_PATH=/workdir/dashboard/logs']
                }
            }
        }
        
        compose_file = Path("/workdir/dashboard/docker-compose.yml")
        with open(compose_file, 'w') as f:
            yaml.dump(docker_compose, f, default_flow_style=False)
        
        print(f"✅ Docker compose file created: {compose_file}")
        print(f"   Run: docker-compose up -d")
        return True
    
    def save_config(self, source_path: str, method: str):
        """Save configuration for persistence"""
        config = {
            'logs_source': str(Path(source_path).expanduser()),
            'connection_method': method,
            'auto_sync': True,
            'sync_interval': 60
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f)
        
        print(f"✅ Configuration saved to {self.config_file}")
    
    def load_config(self) -> Optional[dict]:
        """Load saved configuration"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return yaml.safe_load(f)
        return None

@click.command()
@click.option('--source', '-s', required=True, 
              help='Path to Claude Code logs (e.g., ~/.claude/logs)')
@click.option('--method', '-m', 
              type=click.Choice(['symlink', 'copy', 'watch', 'docker']),
              default='copy',
              help='Connection method to use')
@click.option('--watch', '-w', is_flag=True,
              help='Watch for changes and sync automatically')
def main(source: str, method: str, watch: bool):
    """Connect Claude Code Analytics Dashboard to real log files"""
    
    connector = DashboardConnector()
    
    print("Claude Code Analytics Dashboard - Log Connector")
    print("=" * 50)
    print(f"Source: {source}")
    print(f"Method: {method}")
    print()
    
    success = False
    
    if method == 'symlink':
        success = connector.connect_symlink(source)
    elif method == 'copy':
        success = connector.connect_copy(source, watch=False)
    elif method == 'watch':
        success = connector.connect_copy(source, watch=True)
    elif method == 'docker':
        success = connector.connect_mount(source)
    
    if success:
        connector.save_config(source, method)
        print()
        print("=" * 50)
        print("✅ Dashboard connected to real logs!")
        print("   Refresh your browser to see the data")
        
        if method != 'watch':
            print()
            print("To keep logs synced, run:")
            print(f"  python connect_to_real_logs.py -s {source} -m watch")

if __name__ == "__main__":
    # If no arguments provided, use default
    if len(sys.argv) == 1:
        # Default to your logs location
        sys.argv.extend(['-s', '~/.claude/logs', '-m', 'copy'])
    
    main()