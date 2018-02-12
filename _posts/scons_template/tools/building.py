import os,sys,string
from SCons.Script import *

RootDir = ''
Env = None
BuildOptions = {}
Projects = []



def GetCurrentDir():
    conscript = File('SConscript')
    fn = conscript.rfile()
    name = fn.name
    path = os.path.dirname(fn.abspath)
    return path
    
    
def GetDepend(depend):
    building = True
    if(type(depend)) == type('str'):
        if not BuildOptions.has_key(depend) or BuildOptions[depend] == 0:
            building = False
        elif BuildOptions[depend] != '':
            return BuildOptions[depend]
        return building
    for item in depend:
        if item != '':
            if not BuildOptions.has_key(item) or BuildOptions[item] == 0:
                building = False
    return building
    
def DefineGroup(name, src, depend, **parameters):
    global Env
    if not GetDepend(depend):
        return []
    group_path = ''
    
    for g in Projects:
        if g['name'] == name:
            group_path = g['path']
    if group_path == '':
        group_path = GetCurrentDir()
    group = parameters
    group['name'] = name
    group['path'] = group_path
    if type(src) == type(['src1']):
        group['src'] = File(src)
    else:
        group['src'] = src
        
    if group.has_key('CCFLAGS'):
        Env.AppendUnique(CCFLAGS=group['CCFLAGS'])
    if group.has_key('CPPPATH'):
        Env.AppendUnique(CPPPATH=group['CPPPATH'])
    if group.has_key('CPPDEFINES'):
        Env.AppendUnique(CPPDEFINES=group['CPPDEFINES'])
    if group.has_key('LINKFLAGS'):
        Env.AppendUnique(LINKFLAGS=group['LINKFLAGS'])
        
    if group.has_key('LIBRARY'):
        objs = Env.Library(name, group['src'])
    else:
        objs = group['src']
        
    Projects.append(group)
    return objs
    
def PrepareBuilding(env, rootdir):
    global BuildOptions
    global Env
    global Projects
    global RootDir
    
    RootDir = os.path.abspath(rootdir)
    Env = env
    vdir = 'build'
    objs = SConscript('SConscript', duplicate=0)
    #objs.extend(SConscript(RootDir+'/app/SConscript', variant_dir=vdir+'/app', duplicate=0))
    objs.extend(SConscript(RootDir+'/mod1/SConscript', variant_dir=vdir+'/mod1', duplicate=0))
    objs.extend(SConscript(RootDir+'/mod2/SConscript', variant_dir=vdir+'/mod2', duplicate=0))
    return objs
    
def DoBuilding(target, objs):
    program = None
    program = Env.Program(target, objs)
    print "compile ok"