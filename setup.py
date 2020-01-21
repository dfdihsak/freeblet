from cx_Freeze import setup, Executable 

setup(name = "HelloWorld" , 
      version = "0.1" , 
      description = "" ,
      executables = [Executable("hello.py")])