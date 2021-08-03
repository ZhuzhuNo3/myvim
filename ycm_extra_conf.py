import os
import re
import json

# cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
# or
# bear -- make
compilation_database_file = ''

flags = [
'-Wall',
'-Wextra',
'-Wno-long-long',
'-Wno-variadic-macros',
'-fexceptions',
'-DNDEBUG',
'-std=c++11',
'-x',
'c++',
]

def AddCompilationDatabase( comp_database_file ):
  flags_set=set()
  with open(comp_database_file,'r') as f:
    comp_db = json.load(f)
    for cmd in comp_db:
      if "command" in cmd:
        for inc in re.findall(r" ((?:-I|-isystem)\s?(?:[^\s]*(?:\\ )?/?)+)",cmd["command"]):
          flags_set.add(inc)
      if "arguments" in cmd:
        incs = cmd["arguments"]
        for i in range(0, len(incs)-1):
          if re.match(r"^(-I|-isystem)$", incs[i]) and i + 1 != len(incs):
            flags_set.add(incs[i]+incs[i+1])
          elif re.match(r"^((-I|-isystem).+)$",incs[i]):
            flags_set.add(incs[i])
  return list(flags_set)

pwd = os.getcwd()
for dbPath in [
    compilation_database_file,
    pwd + '/build/compile_commands.json',
    pwd + '/compile_commands.json',
    ]:
  if os.path.exists( dbPath ):
    flags += AddCompilationDatabase( dbPath )
    break

flags += [
'-isystem',
'/usr/local/include',
# ...
]

def Settings( **kwargs ):
  return {
    'flags': flags,
  }
