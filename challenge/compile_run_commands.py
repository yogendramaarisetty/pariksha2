import platform,enum
os_env = platform.system()

CompileCommands = {
    'c' : "gcc {}",
    'cpp' : "g++ {}",
    'java' : "javac {}",
    'python' : "py {}" if os_env == "Windows" else "python3 {}"
}

RunCommands = {
    'c' : "a" if os_env == "Windows" else "./a.out",
    'cpp' : "a" if os_env == "Windows" else "./a.out",
    'java' : "java {}" ,
    'python' : "py {}" if os_env == "Windows" else "python3 {}"
}