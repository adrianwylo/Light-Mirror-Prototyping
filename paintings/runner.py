import multiprocessing
import os

def run_script(script_name):
    os.system(f"sudo python3 {script_name}")  # Replace with the appropriate command to run your scripts

if __name__ == "__main__":
    scripts_to_run = ["script1.py", "script2.py", "script3.py"]  # List of scripts you want to run
    
    processes = []
    for script in scripts_to_run:
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("All scripts have finished.")
