# RestrictedPythonSandbox
An implementation of RestrictedPython focused on file system isolation and nested sandboxing.

# Features
- Execute untrusted or unsafe code in a sandboxed environment using RestrictedPython.
- Enforce permission-based file system isolation.
- Support for nested sandboxing, including inherited and restrictive nested permissions.

# Key Details
Default Folder Permissions: If not specified, access is denied.
Default File Permissions: If not specified, files follow the permissions of their parent folder.
No File System Access: To completely remove file system access, omit the open function when calling the sandbox.
Nested Sandboxes: Inherit permission restrictions from all parent sandboxes and cannot elevate their privileges.

# Disclaimer
While this project provides a Python sandboxing implementation with file system isolation and nested sandboxing, it’s important to note the following:

1. No Sandbox is Completely Secure:
Python was not originally designed with secure sandboxing in mind. Despite leveraging RestrictedPython and carefully implemented permission checks, determined attackers may still find ways to bypass restrictions.

2. Not Suitable for High-Security Scenarios:
This sandbox is designed for educational purposes, experimentation, and non-critical environments. It should not be used for scenarios requiring guaranteed isolation or high security, such as running untrusted code from unknown sources.

3. Understand the Risks:
Running code in any sandbox environment may still expose vulnerabilities in the interpreter or the sandbox implementation. Always evaluate the risks carefully before deploying this project in production environments.

4. Use Additional Security Layers:
For higher security, consider combining this sandbox with other isolation mechanisms such as Docker containers, virtual machines, or restricted OS-level user permissions.
By using this sandbox, you acknowledge these limitations and accept the risks associated with executing untrusted code.
