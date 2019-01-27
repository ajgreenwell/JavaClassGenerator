# JavaClassGenerator

This is a code generator inteded to accept Java interfaces as input and produce compilable, type-correct skeletons of their implementing classes. All relevant code is contained within the `/src` directory, while the `/examples` directory contains some sample Java interfaces and their auto-generated class files. The main logic of this generator is contained within the generate.py module, while syntax.py contains all the necessary details regarding regex matching and class file generation. Lastly, returntypes.py contains a dictionary that maps Java data types to their corresponding, default return values. 

## How To

In order to use the JavaClassGenerator (JCG), you must run the generate.py file with python3 and pass the desired interface file as a command line argument, like so:

```
python3 generate.py interface.java
```

You will then be prompted to enter the name of your new class file...

```
Please enter the name of your class file:
classfile.java
```

Afterwards, your new class file will be generated and stored in the current directory.

### Optional Argument -- Indentation Level

The generate.py module accepts up to 2 arguments via the command line. The first argument is mandatory, and should be a relative path to the desired interface, as shown above. The second is optional, and allows the user to specify a desired indentation level for the class file by passing an integer that represents the number of spaces for each indent, like so:

```
python3 generate.py interface.java 4
```

This command would generate the proper class file from interface.java and use 4 spaces per indentation. However, this second argument is optional, and the default value is 2 spaces.

### Customization

After downloading the JavaClassGenerator, you may find there are some settings you'd like to tweak. For example, you may want to adjust the auto-generated comments at the top of your class file, or the default number of spaces used for indentation levels. This can be done by opening up generate.py and changing the values of the appropriate global variables at the top of the file. Each is prepended by an underscore and marked clearly under the heading 'customizable settings'. Note that modifying the auto-generated comments could neccesitate modifying one line of code in the main() function.

Lastly, for the frequent users of this code generator, you may wish to reduce the amount of typing required to run the generate.py module. You can always do so either by adding an alias to your system profile or by writing a simple shell script. For example, by creating an alias `jcg` for the command `python3 ~/absolute/path/to/generate.py`, you can then invoke the JavaClassGenerator from any directory, like so:

```
jcg interface.java
```
