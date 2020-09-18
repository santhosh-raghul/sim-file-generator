# sim-file-generator
This is a python program that generates sim file for the given boolean expression. 

#

## To run
```
python3 sim_creator.py
```

The program asks for a boolean expression.

Use ```+``` for logical or, ```.``` for logical and, ```!``` for logical not and ```()``` for braces and single charcter variables only

Now, the program asks for a file name. Enter your preferred file name with ```.sim``` extension.

Now the sim file would have been generated.
#
## To test
```
irsim filename.sim
```
You can test the output in the irsim console by watching the nodes with the variable names you entered in the program and the node ```out``` for the output.
#