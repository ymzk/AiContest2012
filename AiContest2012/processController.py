import subprocess
import re
import sys

class ProcessController():
  def __init__(self, executableName):
    cmdline = ""

    match = re.match(r"(.*).py",executableName)
    if match is not None:
      cmdline = ["C:\Python32\python.exe",executableName]
    match = re.match(r"(.*).exe",executableName)
    if match is not None:
      cmdline = ["./" + executableName]
    
    assert cmdline != "","processController can't run this program"
    self._subprocess = subprocess.Popen(cmdline,
                         shell = False,
                         stdin = subprocess.PIPE,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE,
                         close_fds = False)
  def write(self, *arg):
    return self._subprocess.stdin.write(*arg)
  def flush(self, *arg):
    return self._subprocess.stdin.flush(*arg)
  def __iter__(self, *arg):
    return self._subprocess.stdout.__iter__(*arg)
  def __next__(self, *arg):
    return self._subprocess.stdout.__next__(*arg)
  def getchar(self, *arg):
    return self._subprocess.stdout.getchar(*arg)
  def readline(self, *arg):
    return self._subprocess.stdout.readline(*arg)
  def end(self):
    self._subprocess.kill()

  
if __name__ == "__main__":
  pc = ProcessController("echo.py")
  pc.end()
  while True:
    pass
  '''
  pc.write("end\n".encode())
  pc.flush()
  print("wrote end")
  sys.stdout.flush()
#  pc.p.stdin.write(b"hoge\n")
#  pc.p.stdin.flush()
  for j in pc:
    print("stdout = ", j.decode())
    sys.stdout.flush()
    if j == b"\n":
      print("only return")
      sys.stdout.flush()
      continue
    print("write foo")
    pc.write("foo\n".encode())
    pc.flush()
    sys.stdout.flush()
  print("end pc\n")
  sys.stdout.flush()
    '''
