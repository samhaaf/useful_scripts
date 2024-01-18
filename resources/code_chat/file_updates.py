import os
import time

def find_nearest_parent_timestamp(path, timestamps):
    """Find the timestamp of the nearest parent directory in the timestamps dictionary."""
    while path != os.path.dirname(path):  # Check until the root directory is reached
        if path in timestamps:
            return timestamps[path]
        path = os.path.dirname(path)
    return timestamps.get(path, 0)  # Default to 0 if no parent timestamp is found

def has_file_been_updated_since(file_path, timestamp):
    """Check if the file has been modified since the timestamp in the timestamps dict."""
    if not os.path.isfile(file_path):
        return False

    file_mod_time = os.path.getmtime(file_path)
    return file_mod_time > timestamp

def get_updated_files_in(paths, timestamps, default_timestamp=0):
    """Get a list of files or directories in the given paths that have been updated since their respective timestamps."""
    updated_items = []
    for path in paths:
        timestamp = timestamps.get(path, default_timestamp)
        if os.path.isdir(path):
            child_paths = [
                (path + '/' + child).replace('//', '/')
                for child in os.listdir(path)
            ]
            child_paths.sort()
            child_updates = get_updated_files_in(
                child_paths, timestamps, default_timestamp=timestamp
            )
            if child_paths == child_updates:
                updated_items.append(path)
            else:
                updated_items.extend(child_updates)
        elif os.path.isfile(path) and has_file_been_updated_since(path, timestamp):
            updated_items.append(path)

    return updated_items

if __name__ == "__main__":
    # Example usage
    timestamps = {
        '/path/to/directory': time.time() - 86400,  # 24 hours ago
        '/path/to/file.txt': time.time() - 3600     # 1 hour ago
    }
    paths = ['/path/to/directory', '/path/to/file.txt']
    updated_items = get_updated_files_in(paths, timestamps)
    print(updated_items)
