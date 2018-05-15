# -*- encoding: utf-8 -*-
from ctypes import *
import os,time

class MEMORYSTATUS (Structure):  
    """定义内存用率的结构体
    """
    _fields_ = [('dwLength', c_ulong),#sizeof(MEMORYSTATUS)
                ('dwMemoryLoad',c_ulong), # percent of memory in use
                ('dwTotalPhys', c_ulong),#;     // bytes of physical memory
                ('dwAvailPhys', c_ulong),#;     // free physical memory bytes
                ('dwTotalPageFile',c_ulong),#; // bytes of paging file
                ('dwAvailPageFile', c_ulong),#; // free bytes of paging file
                ('dwTotalVirtual', c_ulong),#;  // user bytes of address space
                ('dwAvailVirtual',c_ulong),#;  // free user bytes
    ]

if os.name == 'nt':
    mem = MEMORYSTATUS()
    memptr = pointer(mem)
    windll.kernel32.GlobalMemoryStatus(memptr)

    print u"在用的内存",mem.dwMemoryLoad,"%"
    print u"物理内存",mem.dwTotalPhys
else:
    file = open('/proc/meminfo')
    conf = {}
    line = file.readline()
    while line:
        title, num, kb = line.split()
        conf[title[:-1]] = int(num)
        line = file.readline()
    file.close()
    print 'memtotal:', conf['MemTotal']
    print 'MemFree:', conf['MemFree']
    print 'Cached:', conf['Cached']
    print 'Buffers:', conf['Buffers']
    print 'SwapTotal:', conf['SwapTotal']
    print 'SwapFree:', conf['SwapFree']
    print u'物理内存用率:',(1-(conf['MemFree']*1.0/conf['MemTotal']))*100, '%'
    print u'交换分区:',(1-(conf['SwapFree']*1.0/conf['SwapTotal']))*100, '%'

#################   CPU   #########################

SystemBasicInformation = 0
SystemPerformanceInformation = 2
SystemTimeInformation = 3

class LARGEINT(Union):
    class struct_1(Structure):
        _fields_ = [('lowpart', c_long),
                    ('highpart',c_long)
                    ]
    _fields_ = [("u", struct_1),
                ("QuadPart", c_longlong)]
    

class SYSTEM_BASIC_INFORMATION(Structure):
    _fields_ = [('dwOemId', c_ulong),
                  ('dwPageSize', c_ulong),
                  ('lpMinimumApplicationAddress', c_void_p),
                  ('lpMaximumApplicationAddress', c_void_p),
                  ('dwActiveProcessorMask', c_void_p),
                  ('dwNumberOfProcessors', c_ulong),
                  ('dwProcessorType', c_ulong),
                  ('dwAllocationGranularity', c_ulong),
                  ('wProcessorLevel', c_ushort),
                  ('wProcessorRevision', c_ushort),
                ]

class SYSTEM_PERFORMANCE_INFORMATION(Structure):
    _fields_ = [('liIdleTime', LARGEINT),
                ('dwSpare', c_ulong*76),
                ]

class SYSTEM_TIME_INFORMATION(Structure):
    _fields_ = [('liKeBootTime', LARGEINT),
                ('liKeSystemTime', LARGEINT),
                ('liExpTimeZoneBias', LARGEINT),
                ('uCurrentTimeZoneId', c_ulong),
                ('dwReserved', c_ulong),
            ]

if os.name=='nt':
    SysPerfInfo = SYSTEM_PERFORMANCE_INFORMATION ();
    SysTimeInfo = SYSTEM_TIME_INFORMATION ();
    SysBaseInfo = SYSTEM_BASIC_INFORMATION ();
    #get number of processors in the system
    windll.kernel32.GetSystemInfo(pointer(SysBaseInfo))
    windll.ntdll.NtQuerySystemInformation(SystemTimeInformation,
            pointer(SysTimeInfo),
            sizeof(SYSTEM_TIME_INFORMATION),
            0);
    windll.ntdll.NtQuerySystemInformation(SystemPerformanceInformation,
            pointer(SysPerfInfo),
            sizeof(SYSTEM_PERFORMANCE_INFORMATION),
            0);


    def Li2Double(x):
        return (((x).u.highpart) * 4.294967296E9 + ((x).u.lowpart))
        #return x.QuadPart

    liOldIdleTime = Li2Double(SysPerfInfo.liIdleTime);
    liOldSystemTime = Li2Double(SysTimeInfo.liKeSystemTime);
    begt = time.time()
    time.sleep(1)
    if SysPerfInfo.liIdleTime.QuadPart != 0:
        windll.kernel32.GetSystemInfo(pointer(SysBaseInfo))
        windll.ntdll.NtQuerySystemInformation(SystemTimeInformation,
                pointer(SysTimeInfo),
                sizeof(SYSTEM_TIME_INFORMATION),
                0);
        windll.ntdll.NtQuerySystemInformation(SystemPerformanceInformation,
                pointer(SysPerfInfo),
                sizeof(SYSTEM_PERFORMANCE_INFORMATION),
                0);
        # CurrentValue = NewValue - OldValue
        dbIdleTime = Li2Double(SysPerfInfo.liIdleTime) - liOldIdleTime;
        dbSystemTime = Li2Double(SysTimeInfo.liKeSystemTime) - liOldSystemTime;
        #print SysBaseInfo.dwNumberOfProcessors

        # CurrentCpuIdle = IdleTime / SystemTime
        dbIdleTime = dbIdleTime / dbSystemTime;

        # CurrentCpuUsage% = 100 - (CurrentCpuIdle * 100) / NumberOfProcessors
        dbIdleTime = 100.0 - dbIdleTime*100.0/SysBaseInfo.dwNumberOfProcessors ;

        print u'cpu用率:',dbIdleTime,'%'

        liOldIdleTime = Li2Double(SysPerfInfo.liIdleTime);
        liOldSystemTime = Li2Double(SysTimeInfo.liKeSystemTime);
        time.sleep(1)
else:
    file = open('/proc/stat')
    line = file.readline()
    while not line.startswith('cpu'):
        line = file.readline()
    cpus = line.split()
    Totle1 = sum([int(i) for i in cpus[1:5]])
    use1 = sum([int(cpus[1]),int(cpus[2])])
    file.close()
    time.sleep(0.3)
    file = open('/proc/stat')
    line = file.readline()
    while not line.startswith('cpu'):
        line = file.readline()
    cpus = line.split()
    Totle2 = sum([int(i) for i in cpus[1:5]])
    use2 = sum([int(cpus[1]),int(cpus[2])])
    file.close()
    print u'cpu:用率:', (use2-use1)*1.0/(Totle2-Totle1)*100, '%'

######################## 磁盘使用率 ############################

if os.name=='nt':
    L = 256
    divs = c_buffer("\0"*L)
    l = c_int32(L)
    windll.kernel32.GetLogicalDriveStringsA(l,divs)
    dlist = divs.raw.strip("\0").split("\0")
    print dlist
    try:
        free = c_ulonglong(0)
        totle = c_ulonglong(0)
        freecall = c_ulonglong(0)
        for d in dlist:
            if not (d.startswith('A') or d.startswith('B')):
                print u"磁盘：", d
                result = windll.kernel32.GetDiskFreeSpaceExA(d,
                        pointer(freecall),pointer(totle),pointer(free))
                print u"\t磁盘使用",totle.value-free.value
                print u"\t磁盘剩余",free.value
                print u"\t磁盘总量",totle.value
    except:
        secp = c_ulong(0)
        byteper= c_ulong(0)
        freecl = c_ulong(0)
        totlecl = c_ulong(0)
        for d in dlist:
            if not (d.startswith('A') or d.startswith('B')):
                print u"磁盘：", d
                result = windll.kernel32.GetDiskFreeSpaceA(d,
                        pointer(secp),pointer(byteper),pointer(freecl),pointer(totlecl))
                print u"\t磁盘剩余",secp.value * byteper.value * freecl.value#/ 1073741824.0
                print u"\t磁盘总量",secp.value * byteper.value * totlecl.value#/ 1073741824.0
        #print secp,byteper,freecl,noclu

else:
    dlinfo = os.popen("df")
    line = dlinfo.readline()
    while line:
        if line.startswith('/dev/'):
            #filesys, blocks, used, avaliable, use pre, mount
            fs,t,u,a,p,m = line.split()
            print u"磁盘：",m
            print u"\t磁盘使用(k)", int(u)
            print u"\t磁盘剩余(k)", int(a)
            print u"\t磁盘总量(k)", int(t)
            print u"\t使用率(%)", p[:-1], "%"
        line = dlinfo.readline()
    dlinfo.close()


