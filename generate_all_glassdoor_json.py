import subprocess

# Run department data export
subprocess.run(['python', 'glassdoor_department_charts.py'])

# Run positive sunburst data export
subprocess.run(['python', 'generate_glassdoor_sunburst.py'])

# Run negative sunburst data export
subprocess.run(['python', 'generate_glassdoor_negative_sunburst.py'])

print("All Glassdoor JSON data refreshed!") 