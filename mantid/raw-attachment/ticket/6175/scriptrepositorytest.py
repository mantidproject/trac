## Before testing make sure your Mantid.user.properties does not 
## have a wrong definition for these variables: 
##  - UploaderWebServer 
##  - ScriptLocalRepository 
##  - ScriptRepository

#creation of the ScriptRepository instance
from mantid.api import ScriptRepositoryFactory as srf
repo = srf.Instance().create("ScriptRepositoryImpl")

REPO_PATH = '/tmp/myrep/'

#double check what is available inside ScriptRepository
# I hope you can use the script repository with this example and the 
#information on help 
help(repo)



# In order to test the ScriptRepository we must check its requirements.


# Requirement 1 : Be able to install without network problems
# Requirement 2: Create a Local folder that will be the local repository
repo.install(REPO_PATH) 
# TEST: check that a folder was created in REPO_PATH, and two files are there .local.json .repository.json (hidden files)

# Requirement 3: List Files (remotelly and locally)
list = repo.listFiles()
print '\n'.join(list)
#TEST: check that inside this list you find any file available at https://github.com/mantidproject/scripts.git
#TEST: create a new file and folders inside the REPO_PATH, execute again repo.listFiles() and check
# that these new files are listed as well. 


# Requirement 4: Ability to ignore some file patterns 
# By default we set to ignore pyc files, but the pattern is available at ScriptRepositoryIgnore inside the properties file.
# You may override this property and check if it works well.
#  So, create a file pyc inside the REPO_PATH, execute repo.listFiles() and make sure it does not appear in the list
print  ('file.pyc' not in repo.listFiles() )  FAILED

# Requirement 5: Download files or folders recursively
repo.download('TofConv/TofConverter/Ui_MainWindow.py') 
# TEST: check REPO_PATH/TofConv/TofConverter/Ui_MainWindow.py was created
repo.download('other')
#TEST: check REPO_PATH/other/PyMcp/guassfit.py was created

# Requirement 6: Provide general information for files (Description, Author, Last Modified date, version id)
print repo.fileInfo('TofConv/TofConverter/Ui_MainWindow.py')
#TEST: check that it provides the description, last modified date, version id, author is not implemented yet

# Requirement 7: Manage the versions of a file instance: up-to-date, locally modified, new version available, new version available and locally modified, local only.
# Any file may have the following states: 
#   LOCAL_ONLY
#   REMOTE_ONLY
#   LOCAL_CHANGED
#   REMOTE_CHANGED
#   BOTH_UNCHANGED
#   BOTH_CHANGED
# NOTE: after changing a file locally, or remotely, it is necessary to execute listFiles again.
repo.listFiles() 
print repo.fileStatus('TofConv/TofConverter/Ui_MainWindow.py')
#TEST: should be BOTH_UNCHANGED -  we have just downloaded
print repo.fileStatus('TofConv/TofConverter/converter.ui')
#TEST: should be REMOTE_ONLY
#TEST: open TofConv/TofConverter/Ui_MainWindow.py, make some changes, close it, run listFiles, and than
# run print repo.fileInfo('TofConv/TofConverter/Ui_MainWindow.py'), should return LOCAL_CHANGED
#TEST: test if a file is LOCAL_ONLY, 
# TEST: update a file at the repository, (wait at least one minute - time for the mantidweb to update), run listFiles,
#    check the status is REMOTE_CHANGED

# Requirement 8: Allow files to be marked for automatically updates. (NOT IMPLEMENTED YET)

# Requirement 9: Never override local changes. If the user decides to download a new version of a file he has changed, a backup of his own copy must be produced.
# TEST: download one file repo.download('file')
#            change it locally (open it, and edit it)
#            change the same file remotelly (push your commit to the repository)
#            go, take one coffee  (wait some minutes to mantidweb to recognize the change)
#            run listFiles()
#            check that the file is marked as BOTH_CHANGED repo.fileStatus('file')
#            execute download file : repo.download('file')
#            check that the file is inside your REPO_PATH and a backup file is created as well. 
#example: 
repo.download('README.md')
f = open(REPO_PATH+ '/README.md','w')
f.write("local change")
f.close()
import time
time.sleep(1)
repo.listFiles() 
print repo.fileStatus('README.md') #MUST BE LOCAL_CHANGED
#chage the file and upload, wait , and check4update
repo.update()
print repo.fileStatus('README.md') #Wait till BOTH_CHANGED
repo.download('README.md')
#check taht README.md_bck was created.
