#!/usr/bin/python
from shutil import copyfile
import os
import base64
import smtplib


# path to folder containing the .eml files (recurcive search)
path = '/path/to/eml/files'

# path to folder containing the extracted binary attachment files
attachmentPath = '/path/to/extracted/attachment'

# empty dir for writing the new .eml files containing the attachment encoded in base64
outputDir = '/path/to/merged/eml'

def find_all(name):
    result = []
    #print "name :" + name + ":"
    for root, dirs, files in os.walk(attachmentPath):
        #print "root : " + str(root)
        #print "dirs : " + str(dirs)
        #print "files : " + str(files)
        if name in files:
          for file in files:
            if name == file:
              print "filename : " + str(filename)
              print "file : " + str(root) + "/" + str(file)
              fullAttachmentPath = os.path.join(root, name)
              print fullAttachmentPath
              return fullAttachmentPath
    return False

def copyEmailFile(file):
  try:
   print('try to open : ' + os.path.join(outputDir,file[1]))
   destFile = open(os.path.join(outputDir,file[1]))
  except IOError:
    print("File not found, copy")
    print("copying " + os.path.join(file[0], file[1]))
    copyfile(os.path.join(file[0], file[1]),os.path.join(outputDir, file[1]))
  return os.path.join(outputDir, file[1])

def convertToBase64(attachmentBinary):
  data = open(attachmentBinary, "r").read()
  encoded = base64.b64encode(data)
  return encoded

def insertAttachment(destEmailFile,filename,attachmentBase64):
  lines = []
  filenameFound = False

  with open(destEmailFile) as f:
        lines = f.readlines()

  for i, line in enumerate(lines):
    if 'filename=' + filename in line: 
      print ("line found : " + line + ", tying to iter until the next empty line")
      filenameFound=True
    if filenameFound and line == '\n':
      print ("found an empty line : " + line + " at position " + str(i) + ", inserting here")
      lines.insert(i,'\n')
      lines.insert(i,attachmentBase64)
      lines.insert(i,'\n')
      break

  with open(destEmailFile, 'w') as f:
    f.writelines(lines)

def setMaxColums(attachmentBase64):
  chars = []
  count = 0
  chars = [char for char in attachmentBase64] 
  output = ''

  for  char in chars:
    if count == 75:
      output += '\n' 
      count = 0
    else:
      count = count + 1
    output += char

  return output

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.eml' in file:
          #files.append(os.path.join(r, file))
          files.append([r,file])
	  print file

print files


for file in files:
  f = open(os.path.join(file[0],file[1]))
  for line in f.readlines():
    if 'filename=' in line:
      filename = line.split("=")[1].replace('"', '').replace(';','').replace("\n", " ").rstrip()
      print "email file : " + str(file) + "filename : " + filename
      attachmentBinary = find_all(filename)
      if attachmentBinary:
        print "attachment found"
        print "email file : " + str(file[0] + "/" + str(file[1]))
        destEmailFile = copyEmailFile(file)
        attachmentBase64 = convertToBase64(attachmentBinary) 
        attachmentBase64cols = setMaxColums(attachmentBase64)
        insertAttachment(destEmailFile,filename,attachmentBase64cols)
        
      else:
        print "attachement not found"
      print " "
      print " "
      print " "


