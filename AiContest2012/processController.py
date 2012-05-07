import subprocess
import re

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
                         shell = True,
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
if __name__ == "__main__":
  pc = ProcessController("hoge.py")
  while True:
    pc.write("hoge\n".encode())
    print("wrote")
    pc.flush()
#  pc.p.stdin.write(b"hoge\n")
#  pc.p.stdin.flush()
  for j in pc:
    if j == b"\n":
      continue
    print("step")
    print("stdout = ", j.decode('cp932'))
    print(pc)
    print(pc._subprocess)
    print(pc._subprocess.stdin)
    pc.write("foo".encode())
    
    
