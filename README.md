# JavaClassGenerator

This is a code generator inteded to accept java interfaces as input and produce compilable, type-correct skeletons of their implementing classes. The main logic of this generator is contained within the generate.py module, while various dictionaries have been allocated to the syntax.py and returntypes.py modules in order to improve extensibility.

## How To

In order to use the JavaClassGenerator (JCG), you must run the generate.py file with python3 and pass the desired interface file as a command line argument, like so:

```
python3 generate.py interface.java
```

You will then be prompted to enter the name of your new class file...

```
Please enter the name of your class file:
interfaceC.java
```

Afterwards, your new class file will be generated and stored in the current directory. Any 'import' statements found in the interface will be automatically transferred over to the class file as well.

### Optional Argument -- Indentation Level

As of right now, generate.py accepts up to 2 arguments via the command line. The first argument is mandatory, and should be a relative path to the desired interface, as shown above. The second is optional, and allows the user to specify a desired indentation level for the class file by passing an integer that represents the number of spaces for each indent, like so:

```
python3 generate.py interface.java 4
```

This command would generate the proper class file from interface.java and use 4 spaces per indentation. However, this second argument is optional, and the default value is 2 spaces.

### Customization

After downloading the JavaClassGenerator, you may find there are some settings you'd like to tweak. For example, you may want to modify the default comments that get written at the top of every class file, or you might want to adjust the name of the file's author, or you may want to modify the default number of spaces used for indentation levels. All of this can be done by simply opening up generate.py and changing the values of the global variables at the top of the file. Each is prepended by an underscore.

Lastly, for the frequent users of this code generator, you may wish to reduce the amount of typing required to run the generate.py module. You can always do so either by adding an alias to your system profile or by writing a simple shell script. For example, by creating an alias `jcg` for the command `python3 /absolute/path/to/generate.py`, you can then invoke the JavaClassGenerator from any directory, like so:

```
jcg interface.java
```

