import logging
import sys
sys.path.insert(0, "../..")

import ply.lex as lex
import ply.yacc as yacc
import os

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ParserUtil:
    """
    Base class for a lexer/parser that has the rules defined as methods.
    """
    tokens = ()
    keywords = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = []
        self._input_lines = None
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                          1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"

        # build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self, debug=self.debug, debugfile=self.debugfile)

    @property
    def input_lines(self):
        return self._input_lines

    @input_lines.setter
    def input_lines(self, lines: str):
        self._input_lines = lines

    def run(self):
        if not self.input_lines:
            # Read from the terminal.
            while True:
                try:
                    s = input('parse > ')
                except EOFError:
                    break
                if not s:
                    continue
        newline_count = self.input_lines.count('\n')
        logger.debug(f'About to parse {newline_count + 1} lines.')
        yacc.parse(self.input_lines)


class SasParser(ParserUtil):
    keywords = (
        'PROC',
        'MEANS',
        'DATA',
        'EOL',
        'RUN',
    )
    tokens = keywords + (
        'NUMBER',
        'PLUS', 'MINUS', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN',
        'DATASETNAME',
    )

    # Token rules need to be implemented in each class.
    t_EOL = ';'
    t_PLUS = r'\+'
    t_EXP = r'\*\*'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        # print "parsed number %s" % repr(t.value)
        return t

    def t_DATASETNAME(self, t):
        r'[A-Za-z][A-Za-z0-9\.]*'
        tupper = str(t.value).upper()
        if tupper in self.keywords:
            t.type = tupper
            logger.debug(f'interpreting as keyword: {t.value}')
        else:
            logger.debug(f'encountering datasetname: {t.value}')
        return t

    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        logger.error(f'Illegal character {t.value[0]}')
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EXP'),
        ('right', 'UMINUS'),
    )

    def p_statement_proc(self, p):
        '''
        statement : procdecl
        '''

    def p_procdecl(self, p):
        '''
        procdecl : procmeans
        '''
        logger.debug('encountered proc declaration')

    def p_procmeans(self, p):
        '''
        procmeans : procmeansdecl procend
        '''
        logger.debug('encountered proc means')

    def p_proc_means_decl(self, p):
        '''
        procmeansdecl : PROC MEANS EOL
                      | PROC MEANS procoptions EOL
        '''
        logger.debug('encountered proc means declaration')

    def p_proc_options(self, p):
        '''
        procoptions : procoptions procoption
                    | procoption
        '''

    def p_proc_option(self, p):
        '''
        procoption : dataoption
        '''

    def p_data_option(self, p):
        '''
        dataoption : DATA EQUALS DATASETNAME
        '''

    def p_procend(self, p):
        '''
        procend : RUN EOL
        '''
        logger.debug('encountered RUN statement')

    def p_statement_expr(self, p):
        '''
        statement : expression
        '''
        logger.debug(f'encountering expression: {p[1]}')

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXP expression
        """
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '**':
            p[0] = p[1] ** p[3]

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_error(self, p):
        if p:
            logger.error(f'Syntax error at {p.value}')
        else:
            logger.error('Syntax error at EOF')
