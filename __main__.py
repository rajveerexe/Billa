import zipfile
import os
import shutil
import tempfile
import sys
import platform
import subprocess

def main():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Get the path to the current script
        zip_file_path = os.path.abspath(sys.argv[0])

        # Extract the ZIP file to the temporary directory
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Determine the system and architecture
        system = platform.system()
        architecture = platform.machine()

        # Set the executable name based on platform and architecture
        if system == 'Linux':
            if architecture in ['aarch64', 'arm64']:
                executable_name = 'Executepy_arm64'
            else:
                raise RuntimeError(f"Unsupported architecture: {architecture}")
        else:
            raise RuntimeError(f"Unsupported platform: {system}")

        # Construct the full path to the executable
        executable_path = os.path.join(temp_dir, executable_name)

        # Make the executable file writable
        os.chmod(executable_path, 0o755)

        # Change the working directory to the temporary directory
        os.chdir(temp_dir)

        # Run the executable
        result = subprocess.run([executable_path], check=True)

        # Check if the execution was successful
        if result.returncode != 0:
            print(f"Execution failed with code {result.returncode}")

    finally:
        # Clean up the temporary directory
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
