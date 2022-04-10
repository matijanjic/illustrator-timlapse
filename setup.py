# setup script has to be put inside the plugins folder
# it should ask the user for output folder, interval and key used
# after that it should create the script that would have to be manually added in illustrator and set to the same key that was given to the setup script
# and it should also create another python script in charge of pressing the key

print('\n')
print('---------------ILLUSTRATOR TIMELAPSE SETUP------------------')
print('\n')
print('------------------------------------------------------------')
print('This script has to be inside the Illustrator scripts folder.')
print('Illustrator has to be closed.')
print('------------------------------------------------------------')
print('\n')
print('Images from the timelapse will be saved to an output folder next to the .ai file.')
print('\n')
print('When ran, script created by this setup will export a .png file in an interval (output every x seconds).')
interval = input('Preferred interval in seconds:\n')
print('\n')
print('Script will be simulating a keypress to call an Illustrator action that will export the artboard. \nYou will also have to bind that key to the action in the Illustrator manually.')
fkey = input('Which F key do you want to use? Enter a number: (1-12)?\n')
print('\n')

print('Writing export script...')

jsxOutput = f'''
var document = app.activeDocument;
var aFile = document.fullName;
var folder = new Folder(aFile.parent.fsName + '/output');
if (!folder.exists) {{
  folder.create();
}}
var files = folder.getFiles('*.png')
var iteration = []
for (var i = 0; i < files.length; i++) {{
  iteration.push(parseInt(files[i].toString().split('.')[1]))
}}
iteration.sort(function (a, b) {{ return a - b }})
var currNumber = iteration.slice(-1)[0] + 1
if (!currNumber) {{
  currNumber = 0;
}}
var file = new File(folder.fsName + '/' + 'frame.' + currNumber + '.png')
var options = new ExportOptionsPNG8
options.transparency = false
options.artBoardClipping = true
activeDocument.exportFile(file, ExportType.PNG8, options);
    '''

with open('Export.jsx', 'w') as f:
    f.write(jsxOutput)

print('Done.')

print('Writing timelapse script...')

timelapseScript = f'''
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()
i = 0
while i >= 0:
  keyboard.press(Key.f{fkey})
  keyboard.release(Key.f{fkey})
  time.sleep({interval})
  i += 1
  print(f'F{fkey} pressed {{i}} times.')
'''

with open('timelapse.py', 'w') as f:
    f.write(timelapseScript)

print('Done.')
print('''
What to do next?

1)  Open Illustrator.
2)  Check that the Export script exists under File > Scripts menu
3)  Open the Actions panel by going to Window > Actions
4)  Press the Create New Action button and call it whatever you like
5)  Select the Function key which you specified during this setup
6)  Press record
7)  Go to the top right menu of the Actions panel and select Insert Menu Item
8)  Type in Export and press OK and stop the recording.
9)  When you are ready to record, run the timelapse.py script the same way you ran this script.
10) Note that the key you chose to be pressed will be pressed as long as the script is running, 
    so take that into account with other applications.
11) You can always stop the recording by pressing CTRL + C. You can also resume the recording 
    when you want by running the script again. Note that the count will start from 0 again,
    but previous images won't be lost, that is just the count of how many times key was pressed since starting
    the script.
12) If you want to change anything, just run this setup script again.
''')
