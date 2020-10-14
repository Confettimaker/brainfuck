# TODO  
## Optimize Transpilation to Python (Currently the transpilation is 1:1 and is not Pythonic)
## Clean up the code
## Document


Due to the code being transpiled to Python 1:1, certain errors can show up in the transpiled code.  One of these errors is caused by having a too deeply nested set of loops.  Python can handle nested loops that have a depth of up to 20 and no more.
