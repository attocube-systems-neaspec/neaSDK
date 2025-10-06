"""
Access neaSCOPE database for searching specified keyword.
1. Find all projects with keyword in its name - identical to search function in Project Browser in project panel
2. Iterate through found projects to find  
  a. all Locations with keyword and 
  b. all Scans with keyword
   which are included in the project
3. Return the M1A channel for each found scan.
"""
from neaspec import context
import System.Threading as Threading
import Nea.Client.SharedDefinitions as nea
import System
keyword = "FAT"
maxcount = 100
channel_name = "M1A"
projects = context.Database.SelectProjects(fullTextSearch=keyword, maxProjectsCount = maxcount).Result
print(f"Num projects with keyword '{keyword}' = {len(projects)}")

def get_scan_data(scan_id, channel_name):
  progress = System.Progress[float]()
  NoCancellation = getattr(Threading.CancellationToken, 'None')
  channel = nea.Channel.FromString(channel_name)
  data = context.Database.SelectRawImage(scan_id,channel, 1, NoCancellation, progress).Result
  return data

for project in projects:
    locations = context.Database.SelectLocations(projectId = project.Id).Result
    print(f"Project '{project.Name}': {len(locations)} location(s)")

    for location in locations:
        location_scans = context.Database.SelectScans(location=location, projectId = project.Id).Result
        print(f"Location '{location.Name}' of project '{project.Name}' has {len(location_scans)} scan(s)")
    
    scans = context.Database.SelectScans(projectId = project.Id, fullTextSearch = keyword, maxScansCount = maxcount, skipScansCount=0).Result
    print(f"Project {project.Name}: {len(scans)} scan(s) with keyword '{keyword}'")

    for scan in scans:
        data = get_scan_data(scan.Uuid, channel_name)
        print(f"Scan '{scan.Name}' has length {len(data)}, first value is {data[0]}")
