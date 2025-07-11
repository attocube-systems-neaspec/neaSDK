"""
Access neaSCOPE database for searching specified keyword.
1. Find all projects with keyword in its name - identical to search function in Project Browser in project panel
2. Iterate through found projects to find  
  a. all Locations with keyword and 
  b. all Scans with keyword
   which are included in the project
"""
from neaspec import context
keyword = "FAT"
maxcount = 100
projects = context.Database.SelectProjects(fullTextSearch=keyword, maxProjectsCount = maxcount).Result
 
for project in projects:
    locations = context.Database.SelectLocations(project.Id).Result
    for location in locations:
        print(f"Location {location.Id} has keyword: {keyword in locations.Name}")
        location_scans = context.Database.SelectScans(location=location)
    scans = context.Database.SelectScans(projectId = project.Id, fullTextSearch = keyword, maxScansCount = maxcount, skipScansCount=0).Result
    for scan in scans:
        print(scan.Name)
