import os
import subprocess

# Path to the lock file
lock_file = 'C:/Users/samco/.git/index.lock'

# Check if the file exists
if os.path.exists(lock_file):
    try:
        # Remove the lock file
        os.remove(lock_file)
        print(f"Successfully removed {lock_file}")
        
        # Try the git commit again
        result = subprocess.run(['git', 'commit'], 
                               capture_output=True, 
                               text=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
    except Exception as e:
        print(f"Error removing the file: {e}")
else:
    print(f"Lock file {lock_file} does not exist")