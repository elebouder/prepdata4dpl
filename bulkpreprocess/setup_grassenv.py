import os
import sys
import subprocess
import preprocess_main as prep

###todo make sure projection when initiating this module isnt a problem
###todo figure out what to do if I need to initialize modules individually, or if
###if we need to run a particular GRASS environment after it's already been initialized

def initsetup(location, raw_data):

    #Define grass database
    gisdb = os.path.join(os.path.expanduser("~"), "grassdata")
    mapset = "PERMANENT"

    #path to GRASS GIS launch script
    grass7bin = 'grass74'

    #Query GRASS GIS for GISBASE
    startcmd = [grass7bin, '--config', 'path']
    try:
        p = subprocess.Popen(startcmd,
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True)
        out, err = p.communicate()

    except OSError as error:
        sys.exit("ERROR: Cannot find GRASS GIS start script"
                 "{cmd}: {error}"
                 .format(cmd=startcmd[0], error=error))
    if p.returncode != 0:
        sys.exit("ERROR: Issues running GRASS GIS start script")
    gisbase =out.strip(os.linesep)

    #set GISBASE environment variable
    os.environ['GISBASE'] = gisbase

    #define GRASS Python environment
    grass_pydir = os.path.join(gisbase, "etc", "python")
    sys.path.append(grass_pydir)

    #import some GRASS Python bindings
    import grass.script as grass
    import grass.script.setup as gsetup
    #import grass.script.core.create_location as cloc

    #create new location
    #cloc(gisdb, location, filename=raw_data)
    #launch session
    rcfile = gsetup.init(gisbase, gisdb, location, mapset)
    #gscript.setup.set_gui_path()

    grass.message("Current GRASS GIS environment:")
    
    print(grass.gisenv())
    return rcfile

def reproject(raw_dataset_path, scene):
    import subprocess, os
    lfile = os.listdir(raw_dataset_path)
    lfile = lfile[0]
    batpath = "grass74"
    input = raw_dataset_path + '/' + lfile
    cmd = batpath + " -c " + '"' + input + '" ' + '/home/elebouder/grassdata' \
                                                  '/%s' % scene + ' -e'
    print cmd
    subprocess.call(cmd, shell=True)


