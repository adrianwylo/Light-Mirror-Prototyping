import multiprocessing
import os
import time

def run_script(script_name):
    while True:
        try:
            print(f"Running {script_name}")
            exit_code = os.system(f"sudo python3 {script_name}")  # Replace with the appropriate command to run your scripts
            
            if exit_code == 0:
                print(f"{script_name} completed successfully.")
            else:
                print(f"{script_name} encountered an error. Restarting...")
            
            time.sleep(5)  # Wait for a while before restarting the script
        except Exception as e:
            print(f"An exception occurred while running {script_name}: {e}. Restarting...")
            time.sleep(5)  # Wait for a while before restarting the script

if __name__ == "__main__":
    scripts_to_run = ["script1.py", "script2.py", "script3.py"]  # List of scripts you want to run
    
    processes = []
    for script in scripts_to_run:
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
