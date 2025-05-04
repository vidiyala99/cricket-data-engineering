import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of ETL script names to execute
etl_scripts = [
    "Create_Top_Batters_350runs_130sr_View.py",
    "Create_Top_Powerplay_Batters_View.py",
    "Create_Top_Death_Batters_View.py",
    "Create_Top_Bowlers_10wickets_Economy_View.py",
    "Create_Top_Powerplay_Bowlers_View.py",
    "Create_Top_Death_Bowlers_View.py",
    "Create_Impactful_Death_Bowlers_View.py",
    "Create_Best_All_Rounders_View.py",
    "Create_Impact_of_Toss_Home_Games_View.py",
    "Create_Team_Home_Away_Win_Percentage_View.py",
    "Create_Team_Win_Percentage_By_Venue_View.py"
]

def run_script(script_name):
    path = os.path.join("etl", script_name)
    result = subprocess.run(["python", path], capture_output=True, text=True)
    return (script_name, result.returncode, result.stdout, result.stderr)

print("🔁 Running ETL scripts in parallel...\n")

# Launch scripts in parallel threads
with ThreadPoolExecutor(max_workers=min(6, len(etl_scripts))) as executor:
    futures = [executor.submit(run_script, script) for script in etl_scripts]

    for future in as_completed(futures):
        script_name, returncode, stdout, stderr = future.result()
        if returncode == 0:
            print(f"✅ {script_name} completed successfully.")
        else:
            print(f"❌ {script_name} failed.\nError:\n{stderr}")

print("\n🏁 All scripts attempted in parallel.")
