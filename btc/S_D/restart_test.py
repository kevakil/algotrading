import os
import sys

print 'test'
# os.fsync()
# sys.stdout.flush()
os.execv(sys.executable, ['python'] + sys.argv)
