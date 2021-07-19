# Compiler
Main concept: read in one type of computer language (say SAS or Pandas Python) and emit another type of computer language (say Python or PySpark).

# Main Modules
## ParserUtil
Base class
### SasParser
A child class that implements ply (Python Lex Yacc) to read SAS modules (like Proc mean).

## CompilerUtil
Abstract Base Class (ABC) for a compiler.
One side of a Bridge design pattern.

### SasCompilerUtil
Concrete implementation of CompilerUtil. 
Other side of a Bridge design pattern.

## EmitterUtil
Abstract Base Class (ABC) for an emitter.
One side of a Bridge design pattern.

### SasSummerizeUtil
Concrete implementation of EmitterUtil.

### PandasEmitterUtil
Concrete implementation of EmitterUtil.

### PythonEmitterUtil
Concrete implementation of EmitterUtil.
