#
# This is a special configuration of the Linux kernel, aimed exclusively
# for running inside a Hyper-V virtual machine
# This specialization allows us to optimize memory footprint and boot time.
#

Name:           linux-hyperv-mini
Version:        4.11.0
Release:        3
License:        GPL-2.0
Summary:        The Linux kernel optimized for running inside Hyper-V
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.11-rc2.tar.xz
Source1:        config
Source2:        cmdline

%define kversion 4.11.0-%{release}.hyperv-mini

BuildRequires:  bash >= 2.03
BuildRequires:  bc
BuildRequires:  binutils-dev
BuildRequires:  elfutils-dev
BuildRequires:  make >= 3.78
BuildRequires:  openssl-dev
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  kmod

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#    000X: cve, bugfixes patches

#    00XY: Mainline patches, upstream backports
Patch0011: 0011-Patch-for-Intel-Clear-Container-building-purpose.patch

# Serie    01XX: Clear Linux patches
Patch0101: 0101-init-don-t-wait-for-PS-2-at-boot.patch
Patch0102: 0102-i8042-decrease-debug-message-level-to-info.patch
Patch0103: 0103-init-do_mounts-recreate-dev-root.patch
Patch0104: 0104-Increase-the-ext4-default-commit-age.patch
Patch0105: 0105-silence-rapl.patch
Patch0106: 0106-pci-pme-wakeups.patch
Patch0107: 0107-ksm-wakeups.patch
Patch0108: 0108-intel_idle-tweak-cpuidle-cstates.patch
Patch0109: 0109-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0110: 0110-init_task-faster-timerslack.patch
Patch0111: 0111-KVM-x86-Add-hypercall-KVM_HC_RETURN_MEM.patch
Patch0112: 0112-fs-ext4-fsync-optimize-double-fsync-a-bunch.patch
Patch0113: 0113-overload-on-wakeup.patch
Patch0114: 0114-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0115: 0115-fix-initcall-timestamps.patch
Patch0116: 0116-smpboot-reuse-timer-calibration.patch
Patch0117: 0117-raid6-add-Kconfig-option-to-skip-raid6-benchmarking.patch
Patch0118: 0118-Initialize-ata-before-graphics.patch
Patch0119: 0119-reduce-e1000e-boot-time-by-tightening-sleep-ranges.patch
Patch0120: 0120-Skip-synchronize_rcu-on-single-CPU-systems.patch
Patch0121: 0121-Make-a-few-key-drivers-probe-asynchronous.patch
Patch0122: 0122-use-the-new-async-probing-feature-for-the-hyperv-dri.patch
Patch0123: 0123-sysrq-Skip-synchronize_rcu-if-there-is-no-old-op.patch
Patch0124: 0124-printk-end-of-boot.patch
Patch0125: 0125-Boot-with-rcu-expedite-on.patch
Patch0126: 0126-give-rdrand-some-credit.patch
Patch0127: 0127-print-starve.patch
Patch0128: 0128-increase-readahead-amounts.patch
Patch0129: 0129-free-initmem-asynchronously.patch
Patch0130: 0130-remove-clear-ioapic.patch

# Serie    XYYY: Extra features modules
# AUFS
Patch1001: 1001-aufs4.x-rcN-kbuild-patch.patch
Patch1002: 1002-aufs4.x-rcN-base-patch.patch
Patch1003: 1003-aufs4.x-rcN-mmap-patch.patch
Patch1004: 1004-aufs4.x-rcN-standalone-patch.patch
Patch1005: 1005-aufs4.x-rcN-docs-fs-includes.patch

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel Hyper-V extra files
Group:          kernel

%description extra
Linux kernel extra files

%prep
%setup -q -n linux-4.11-rc2

#     000X  cve, bugfixes patches

#     00XY  Mainline patches, upstream backports
%patch0011 -p1

#     01XX  Clear Linux patches
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1

# AUFS
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1

cp %{SOURCE1} .

%build
BuildKernel() {
    MakeTarget=$1

    Arch=x86_64
    ExtraVer="-%{release}.hyperv-mini"

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make -s mrproper
    cp config .config

    make -s ARCH=$Arch oldconfig > /dev/null
    make -s CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} ARCH=$Arch %{?sparse_mflags}
}

BuildKernel bzImage

%install

InstallKernel() {
    KernelImage=$1

    Arch=x86_64
    KernelVer=%{kversion}
    KernelDir=%{buildroot}/usr/lib/kernel

    mkdir   -p ${KernelDir}
    install -m 644 .config    ${KernelDir}/config-${KernelVer}
    install -m 644 System.map ${KernelDir}/System.map-${KernelVer}
    install -m 644 %{SOURCE2} ${KernelDir}/cmdline-${KernelVer}
    cp  $KernelImage ${KernelDir}/org.clearlinux.hyperv-mini.%{version}-%{release}
    chmod 755 ${KernelDir}/org.clearlinux.hyperv-mini.%{version}-%{release}

    mkdir -p %{buildroot}/usr/lib/modules/$KernelVer
    make -s ARCH=$Arch INSTALL_MOD_PATH=%{buildroot}/usr modules_install KERNELRELEASE=$KernelVer

    rm -f %{buildroot}/usr/lib/modules/$KernelVer/build
    rm -f %{buildroot}/usr/lib/modules/$KernelVer/source

    # Erase some modules index
    for i in alias ccwmap dep ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols usbmap softdep devname
    do
        rm -f %{buildroot}/usr/lib/modules/${KernelVer}/modules.${i}*
    done
    rm -f %{buildroot}/usr/lib/modules/${KernelVer}/modules.*.bin
}

InstallKernel arch/x86/boot/bzImage

rm -rf %{buildroot}/usr/lib/firmware

# Recreate modules indices
depmod -a -b %{buildroot}/usr %{kversion}

ln -s org.clearlinux.hyperv-mini.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-hyperv-mini

%files
%dir /usr/lib/kernel
%dir /usr/lib/modules/%{kversion}
/usr/lib/kernel/config-%{kversion}
/usr/lib/kernel/cmdline-%{kversion}
/usr/lib/kernel/org.clearlinux.hyperv-mini.%{version}-%{release}
/usr/lib/kernel/default-hyperv-mini
/usr/lib/modules/%{kversion}/kernel
/usr/lib/modules/%{kversion}/modules.*

%files extra
%dir /usr/lib/kernel
/usr/lib/kernel/System.map-%{kversion}
