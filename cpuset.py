#! coding=utf8

import subprocess


class CPUSet(object):
    """CPUSet Represents a structure for manipulating
    the CPUSet(http://man7.org/linux/man-pages/man7/cpuset.7.html#FORMATS)"""

    def __init__(self, initset=None):
        self._items = set()
        if isinstance(initset, set):
            self._items = initset

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            other = CPUSet.Parse(other)
        return CPUSet(self._items.union(other._items))

    def __eq__(self, other):
        pass

    def __contains__(self, item):
        return item in self._items

    def __isub__(self, other):
        pass

    def __len__(self):
        return len(self._items)

    def union(self, other):
        if not isinstance(other, self.__class__):
            other = CPUSet.Parse(other)
        return CPUSet(self._items.union(other._items))

    def add(self, item):
        if isinstance(item, int):
            self._items.add(item)
        else:
            self._items.add(int(item))

    def clear(self):
        self._items = set()

    def copy(self):
        copied = self._items.copy()
        return CPUSet(copied)

    def difference_update(self, items):
        pass

    @staticmethod
    def merge_cpuset(one, two):
        """Merges 2 cpuset into one.
        the format can be string or CPUSet representative
        """
        if not isinstance(one, CPUSet):
            one = CPUSet.Parse(one)
        if not isinstance(two, CPUSet):
            two = CPUSet.Parse(two)
        return one.union(two)

    @classmethod
    def Parse(cls, cpuset_str):
        """Parse CPUSet constructs a new CPU set from a Linux CPU list formatted string.
        See: http://man7.org/linux/man-pages/man7/cpuset.7.html#FORMATS
        """
        if cpuset_str == "":
            return CPUSet(set())
        cpuset = set()
        for x in cpuset_str.split(","):
            if "-" in x:
                start_end = x.split("-")
                for z in range(int(start_end[0]), int(start_end[1]) + 1):
                    cpuset.add(z)
            else:
                cpuset.add(int(x))
        return cls(cpuset)

    @staticmethod
    def GetCPUCount():
        r = 0
        try:
            r = int(subprocess.run(
                ["nproc"], stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout)
        except:
            r = int(subprocess.check_output(['nproc']))
        return r

    @staticmethod
    def GetCGroupCPUCount():
        r = 0
        try:
            r = int(subprocess.run(
                ["cat", "/sys/fs/cgroup/cpuset/cpuset.cpus"], stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout)
        except:
            r = int(subprocess.check_output(['cat', "/sys/fs/cgroup/cpuset/cpuset.cpus"]))
        return r

    @classmethod
    def HostCPUSet(cls, from_cgroup=False):
        """Returns the CPUSet from running host.
        By default, it parses from `nproc` command
        it can also read cpuset from cgroup data from
        /sys/fs/cgroup/cpuset/cpuset.cpus
        """
        if from_cgroup:
            ncpu = CPUSet.GetCGroupCPUCount()
        else:
            ncpu = CPUSet.GetCPUCount()

        cpuset = [i for i in range(ncpu)]
        return CPUSet(set(cpuset))
