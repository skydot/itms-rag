"""
Report Cleanup Service

Cleans up expired report files based on TTL metadata.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Set

# Base reports directory
DEFAULT_REPORTS_DIR = Path("app/static/reports")
DEFAULT_TTL_SECONDS = int(os.getenv("REPORT_TTL_SECONDS", "3600"))


def _is_safe_path(base_dir: Path, target_path: Path) -> bool:
    """
    Verify that target_path is within base_dir (prevent path traversal).
    """
    try:
        # Resolve both paths to absolute paths
        base_resolved = base_dir.resolve()
        target_resolved = target_path.resolve()
        
        # Check if target starts with base
        return str(target_resolved).startswith(str(base_resolved))
    except (OSError, ValueError):
        return False


def cleanup_expired_reports(
    reports_dir: str = "app/static/reports"
) -> int:
    """
    Clean up expired report files based on their metadata JSON files.
    
    Args:
        reports_dir: Base directory for reports (relative or absolute)
        
    Returns:
        Number of files deleted (HTML + JSON)
    """
    base_path = Path(reports_dir)
    
    # Security check - ensure path exists and is within expected directory
    if not base_path.exists():
        print(f"[Report Cleanup] Reports directory does not exist: {reports_dir}")
        return 0
    
    # Resolve to absolute path for safety checks
    base_path = base_path.resolve()
    
    # Verify we're only operating within the reports directory
    expected_base = DEFAULT_REPORTS_DIR.resolve()
    if not str(base_path).startswith(str(expected_base)):
        print(f"[Report Cleanup] ERROR: Path {base_path} is outside allowed directory {expected_base}")
        return 0
    
    deleted_count = 0
    now = datetime.now()
    ttl_threshold = now.timestamp() - DEFAULT_TTL_SECONDS
    
    # Track orphaned HTML files
    html_files_found: Set[Path] = set()
    json_files_found: Set[Path] = set()
    
    # Walk through the reports directory
    for root, dirs, files in os.walk(base_path):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in files:
            file_path = Path(root) / filename
            
            # Security check - ensure file is within reports directory
            if not _is_safe_path(base_path, file_path):
                print(f"[Report Cleanup] Skipping unsafe path: {file_path}")
                continue
            
            if filename.endswith('.json'):
                json_files_found.add(file_path)
                
                # Try to read metadata and check expiry
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    expires_at_str = metadata.get('expires_at')
                    if expires_at_str:
                        expires_at = datetime.fromisoformat(expires_at_str)
                        
                        if now > expires_at:
                            # Delete the associated HTML file
                            html_filename = metadata.get('file', filename.replace('.json', '.html'))
                            html_path = file_path.parent / html_filename
                            
                            # Delete HTML file
                            if html_path.exists() and _is_safe_path(base_path, html_path):
                                try:
                                    html_path.unlink()
                                    deleted_count += 1
                                    print(f"[Report Cleanup] Deleted expired report: {html_path.name}")
                                except OSError as e:
                                    print(f"[Report Cleanup] Error deleting {html_path}: {e}")
                            
                            # Delete JSON file
                            try:
                                file_path.unlink()
                                deleted_count += 1
                                print(f"[Report Cleanup] Deleted metadata: {file_path.name}")
                            except OSError as e:
                                print(f"[Report Cleanup] Error deleting {file_path}: {e}")
                                
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    print(f"[Report Cleanup] Error reading metadata {file_path}: {e}")
                    # If JSON is corrupted, treat as expired
                    try:
                        file_path.unlink()
                        deleted_count += 1
                        print(f"[Report Cleanup] Deleted corrupted metadata: {file_path.name}")
                    except OSError:
                        pass
                        
            elif filename.endswith('.html'):
                html_files_found.add(file_path)
    
    # Handle orphaned HTML files (no corresponding JSON or JSON was corrupted)
    for html_path in html_files_found:
        json_path = html_path.with_suffix('.json')
        
        # Check if JSON metadata exists
        if json_path not in json_files_found:
            # No metadata - check file age
            try:
                stat = html_path.stat()
                file_age = stat.st_mtime
                
                if file_age < ttl_threshold:
                    # File is older than TTL, safe to delete
                    if _is_safe_path(base_path, html_path):
                        try:
                            html_path.unlink()
                            deleted_count += 1
                            print(f"[Report Cleanup] Deleted orphaned report: {html_path.name}")
                        except OSError as e:
                            print(f"[Report Cleanup] Error deleting {html_path}: {e}")
            except OSError as e:
                print(f"[Report Cleanup] Error checking {html_path}: {e}")
    
    # Remove empty directories (except the root reports directory itself)
    for root, dirs, files in os.walk(base_path, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            
            # Security check
            if not _is_safe_path(base_path, dir_path):
                continue
            
            # Don't delete the base directory itself
            if dir_path.resolve() == base_path.resolve():
                continue
                
            try:
                # Check if directory is empty
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"[Report Cleanup] Removed empty directory: {dir_path.name}")
            except OSError:
                pass  # Directory not empty or permission issue
    
    if deleted_count > 0:
        print(f"[Report Cleanup] Total files deleted: {deleted_count}")
    else:
        print(f"[Report Cleanup] No expired reports found")
    
    return deleted_count


def get_report_stats(reports_dir: str = "app/static/reports") -> dict:
    """
    Get statistics about current reports.
    
    Returns:
        Dict with total_reports, expired_count, active_count, total_size
    """
    base_path = Path(reports_dir).resolve()
    
    if not base_path.exists():
        return {"total_reports": 0, "expired_count": 0, "active_count": 0, "total_size_bytes": 0}
    
    now = datetime.now()
    total_reports = 0
    expired_count = 0
    total_size = 0
    
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            if filename.endswith('.html'):
                total_reports += 1
                file_path = Path(root) / filename
                
                try:
                    stat = file_path.stat()
                    total_size += stat.st_size
                    
                    # Check if expired via JSON metadata
                    json_path = file_path.with_suffix('.json')
                    if json_path.exists():
                        with open(json_path, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        expires_at = datetime.fromisoformat(metadata.get('expires_at', '2000-01-01'))
                        if now > expires_at:
                            expired_count += 1
                except (OSError, json.JSONDecodeError, ValueError):
                    pass
    
    return {
        "total_reports": total_reports,
        "expired_count": expired_count,
        "active_count": total_reports - expired_count,
        "total_size_bytes": total_size
    }
