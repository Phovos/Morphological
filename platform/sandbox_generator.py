#!/usr/bin/env python3
"""
Dynamic Windows Sandbox Configuration Generator
Generates sandbox_config.wsb based on the current system's runtime parameters.
"""

import os
import sys
import getpass
from pathlib import Path


def get_current_user_path():
    """Get the current user's path for the sandbox directory mapping."""
    username = getpass.getuser()
    # Get the user's Documents folder path
    user_profile = Path.home()
    documents_path = user_profile / "Documents"

    # Construct the sandbox path
    sandbox_host_path = documents_path / "sandbox"

    return str(sandbox_host_path)


def get_system_info():
    """Gather system information for configuration context."""
    info = {
        'platform': sys.platform,
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'python_executable': sys.executable,
        'current_user': getpass.getuser(),
        'working_directory': os.getcwd(),
    }
    return info


def generate_wsb_config(sandbox_host_path, output_path="sandbox_config.wsb"):
    """
    Generate the Windows Sandbox configuration file.

    Args:
        sandbox_host_path (str): Path to the sandbox directory on the host system
        output_path (str): Output file path for the WSB config
    """

    # Ensure the sandbox host path exists
    if not os.path.exists(sandbox_host_path):
        print(
            f"Warning: Sandbox directory does not exist at {sandbox_host_path}")
        print("You may need to create this directory or adjust the path.")

    # Define the sandbox target path (always the same in sandbox)
    sandbox_target_path = "C:\\Users\\WDAGUtilityAccount\\Desktop\\sandbox"

    # Define the provisioner path within the mapped folder
    provisioner_path = f"{sandbox_target_path}\\platform\\provisioner.bat"

    # Generate the WSB configuration XML
    wsb_config = f"""<Configuration>
    <vGPU>Enable</vGPU>
    <Networking>Default</Networking>
    <AudioInput>Enable</AudioInput>
    <VideoInput>Disable</VideoInput>
    <PrinterRedirection>Disable</PrinterRedirection>
    <ClipboardRedirection>Default</ClipboardRedirection>
    <ProtectedClient>Disable</ProtectedClient>
    <MemoryInMB>8192</MemoryInMB>
    <MappedFolders>
        <MappedFolder>
            <HostFolder>{sandbox_host_path}</HostFolder>
            <SandboxFolder>{sandbox_target_path}</SandboxFolder>
            <ReadOnly>false</ReadOnly>
        </MappedFolder>
    </MappedFolders>
    <LogonCommand>
        <Command>cmd.exe /c start /wait "" "{provisioner_path}"</Command>
    </LogonCommand>
</Configuration>"""

    # Write the configuration to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(wsb_config)

        print(f"✅ Successfully generated WSB config: {output_path}")
        print(f"📁 Host folder mapped: {sandbox_host_path}")
        print(f"Sandbox folder: {sandbox_target_path}")
        print(f"Provisioner: {provisioner_path}")

        return True

    except Exception as e:
        print(f"❌ Error writing WSB config: {e}")
        return False


def main():
    """Main function to generate the WSB configuration."""
    print("🔧 Dynamic Windows Sandbox Configuration Generator")
    print("=" * 50)

    # Get system information
    sys_info = get_system_info()
    print(f"Current user: {sys_info['current_user']}")
    print(f"Platform: {sys_info['platform']}")
    print(f"Python: {sys_info['python_version']}")
    print(f"Working directory: {sys_info['working_directory']}")
    print()

    # Determine the sandbox host path
    sandbox_host_path = get_current_user_path()

    # Allow user to override the path
    print(f"Default sandbox path: {sandbox_host_path}")
    user_input = input(
        "Press Enter to use default, or type a different path: ").strip()

    if user_input:
        sandbox_host_path = user_input

    # Normalize the path (convert forward slashes to backslashes for Windows)
    sandbox_host_path = os.path.normpath(sandbox_host_path)

    print(f"Using sandbox path: {sandbox_host_path}")
    print()

    # Generate the WSB configuration
    success = generate_wsb_config(sandbox_host_path)

    if success:
        print()
        print("🎉 Configuration generated successfully!")
        print("You can now run the sandbox with: sandbox_config.wsb")
        print()
        print("Next steps:")
        # Kept this line as is, assuming it refers to the *content* of the mapped folder,
        # not the folder name itself, based on the original request.
        print("1. Ensure your MORPHOLOGICAL-SOURCE-CODE/ directory exists at the specified path")
        print("2. Double-click sandbox_config.wsb to launch the sandbox")
    else:
        print("❌ Failed to generate configuration")
        sys.exit(1)


if __name__ == "__main__":
    main()
