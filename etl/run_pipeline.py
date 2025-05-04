import os
import subprocess

# List of ETL scripts to run (in order)
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

print("🔁 Running full ETL pipeline...\n")

for script in etl_scripts:
    print(f"🚀 Running {script}...")
    result = subprocess.run(["python", os.path.join("etl", script)], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {script} executed successfully!\n")
    else:
        print(f"❌ Error running {script}:\n{result.stderr}\n")

print("🏁 All scripts attempted.")
