import subprocess
import platform

def check_user_accounts():
    user_accounts = []

    if platform.system() == "Linux":
        try:
            passwd_file = open("/etc/passwd", "r")
            user_accounts = passwd_file.read()
            passwd_file.close()
        except FileNotFoundError:
            pass

    return f"\nUser Accounts:\n{user_accounts}"

def check_system_configuration():
    system_configuration = []

    if platform.system() == "Linux":
        try:
            sysctl_info = subprocess.check_output(["sysctl", "-a"], universal_newlines=True)
            system_configuration.append(f"\nSystem Configuration:\n{sysctl_info}")
        except FileNotFoundError:
            pass

    return system_configuration

def check_vulnerabilities():
    vulnerabilities = []

    system_info = f"Operating System: {platform.system()} {platform.release()}"
    vulnerabilities.append(system_info)

    # Check open ports
    if platform.system() == "Windows":
        open_ports = subprocess.check_output(["netstat", "-ano"], universal_newlines=True)
    else:
        open_ports = subprocess.check_output(["netstat", "-an"], universal_newlines=True)
    vulnerabilities.append(f"\nOpen Ports:\n{open_ports}")

    # Check installed software (Linux and Windows)
    if platform.system() == "Linux":
        try:
            installed_packages = subprocess.check_output(["dpkg", "-l"], universal_newlines=True)
            vulnerabilities.append(f"\nInstalled Packages:\n{installed_packages}")
        except FileNotFoundError:
            pass
    elif platform.system() == "Windows":
        try:
            installed_programs = subprocess.check_output(["wmic", "product", "get", "name"], universal_newlines=True)
            vulnerabilities.append(f"\nInstalled Programs:\n{installed_programs}")
        except FileNotFoundError:
            pass

    # Check system updates (Linux and Windows)
    if platform.system() == "Linux":
        try:
            updates_available = subprocess.check_output(["apt", "list", "--upgradable"], universal_newlines=True)
            vulnerabilities.append(f"\nAvailable Updates:\n{updates_available}")
        except FileNotFoundError:
            pass
    elif platform.system() == "Windows":
        try:
            windows_updates = subprocess.check_output(["wmic", "qfe", "list", "full"], universal_newlines=True)
            vulnerabilities.append(f"\nWindows Updates:\n{windows_updates}")
        except FileNotFoundError:
            pass

    # Check running processes (Linux and Windows)
    if platform.system() == "Linux":
        running_processes = subprocess.check_output(["ps", "aux"], universal_newlines=True)
    elif platform.system() == "Windows":
        running_processes = subprocess.check_output(["tasklist"], universal_newlines=True)
    vulnerabilities.append(f"\nRunning Processes:\n{running_processes}")

    return vulnerabilities

if __name__ == "__main__":
    vulnerabilities = check_vulnerabilities()

    print("System Vulnerability Report")
    print("=" * 60)

    for vulnerability_info in vulnerabilities:
        if isinstance(vulnerability_info, list):
            print("\n".join(vulnerability_info))
        else:
            print(vulnerability_info)
        print("=" * 60)

    print("Vulnerability scan completed.")

