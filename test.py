from playsound import playsound
import os
cwd = os.getcwd()
print (cwd)
os.chdir(cwd+"\sounds\Père")
print(os.getcwd())
playsound("temp.flac")
os.chdir(cwd)
print (cwd)