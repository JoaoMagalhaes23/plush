
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftMULTIPLYDIVIDEMODrightPOWERnonassocLESSGREATERLESS_EQUALGREATER_EQUALEQUALSDIFFERENTleftANDleftORrightNOTrightUMINUSAND BOOLEAN BOOLEAN_LITERAL CHAR CHAR_LITERAL COLON COLON_EQUALS COMMA DIFFERENT DIVIDE DOUBLE DOUBLE_LITERAL ELSE EQUALS FLOAT FLOAT_LITERAL FUNCTION GREATER GREATER_EQUAL ID IF IMMUTABLE_VARIABLE INT INT_LITERAL LESS LESS_EQUAL L_BRACKET L_PAREN L_S_BRACKET MINUS MOD MULTIPLY MUTABLE_VARIABLE NOT OR PLUS POWER R_BRACKET R_PAREN R_S_BRACKET SEMICOLON STRING STRING_LITERAL VOID WHILE\n    start : top_level_declarations\n    \n    top_level_declarations  : top_level_declaration top_level_declarations\n                            | top_level_declaration\n    \n    top_level_declaration   : create_variable SEMICOLON\n                            | assign SEMICOLON\n                            | function\n    \n    create_variable : MUTABLE_VARIABLE ID COLON type t\n                    | IMMUTABLE_VARIABLE ID COLON type t   \n    \n    t   : COLON_EQUALS expression\n        | \n    \n    assign : ID COLON_EQUALS expression\n    \n    function : FUNCTION ID L_PAREN parameter_list R_PAREN COLON type L_BRACKET block R_BRACKET\n    \n    parameter_list  : create_variable COMMA parameter_list\n                    | create_variable\n     \n    block   : statement block \n            | statement\n    \n    statement   : if_statement\n                | while_statement\n                | assign SEMICOLON\n                | create_variable SEMICOLON\n                | function_call SEMICOLON\n    \n    if_statement    : IF expression L_BRACKET block R_BRACKET else_if_statements\n    \n    else_if_statements  : ELSE IF expression L_BRACKET block R_BRACKET else_if_statements\n                        | ELSE IF expression L_BRACKET block R_BRACKET\n                        | ELSE L_BRACKET block R_BRACKET\n    \n    while_statement : WHILE expression L_BRACKET block R_BRACKET\n    \n    expression  : expression MULTIPLY expression\n                | expression DIVIDE expression\n                | expression MOD expression\n                | expression POWER expression\n                | expression PLUS expression\n                | expression MINUS expression\n                | expression LESS expression\n                | expression GREATER expression\n                | expression GREATER_EQUAL expression\n                | expression LESS_EQUAL expression\n                | expression EQUALS expression\n                | expression DIFFERENT expression\n                | expression AND expression\n                | expression OR expression\n                | L_PAREN expression R_PAREN\n                | value\n    expression : MINUS expression %prec UMINUSexpression : NOT expression\n    type    : type_int\n            | type_double\n            | type_string\n            | type_boolean\n            | type_char\n            | type_float\n            | type_void\n            | type_array\n    \n    type_int : INT\n    \n    type_double : DOUBLE\n    \n    type_string : STRING\n    \n    type_boolean : BOOLEAN\n    \n    type_char : CHAR\n    \n    type_float : FLOAT\n    \n    type_void : VOID\n    \n    type_array : L_S_BRACKET type R_S_BRACKET\n    \n    value   : literal_int\n            | literal_double\n            | literal_string\n            | literal_boolean\n            | literal_char\n            | literal_float\n            | identifier\n            | function_call\n            | array\n    \n    literal_int : INT_LITERAL\n    \n    literal_double : DOUBLE_LITERAL\n    \n    literal_string : STRING_LITERAL\n    \n    literal_boolean : BOOLEAN_LITERAL\n    \n    literal_char : CHAR_LITERAL\n    \n    literal_float : FLOAT_LITERAL\n    \n    identifier  : ID\n                | ID L_S_BRACKET expression R_S_BRACKET\n    \n    array   : L_S_BRACKET values_list R_S_BRACKET\n            | L_BRACKET R_BRACKET\n    \n    values_list : value COMMA values_list\n                | value\n                |\n    \n    function_call : ID L_PAREN arguments_list R_PAREN\n    \n    arguments_list  : expression COMMA arguments_list\n                    | expression\n                    |\n    '
    
_lr_action_items = {'MUTABLE_VARIABLE':([0,3,6,12,13,43,111,122,125,126,127,133,135,136,137,140,141,145,146,149,152,153,155,156,],[7,7,-6,-4,-5,7,7,7,7,-17,-18,-12,-19,-20,-21,7,7,-26,-22,7,7,-25,-24,-23,]),'IMMUTABLE_VARIABLE':([0,3,6,12,13,43,111,122,125,126,127,133,135,136,137,140,141,145,146,149,152,153,155,156,],[9,9,-6,-4,-5,9,9,9,9,-17,-18,-12,-19,-20,-21,9,9,-26,-22,9,9,-25,-24,-23,]),'ID':([0,3,6,7,9,10,12,13,15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,122,125,126,127,131,132,133,135,136,137,140,141,145,146,148,149,152,153,155,156,],[8,8,-6,14,16,17,-4,-5,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,123,123,-17,-18,19,19,-12,-19,-20,-21,123,123,-26,-22,19,123,123,-25,-24,-23,]),'FUNCTION':([0,3,6,12,13,133,],[10,10,-6,-4,-5,-12,]),'$end':([1,2,3,6,11,12,13,133,],[0,-1,-3,-6,-2,-4,-5,-12,]),'SEMICOLON':([4,5,19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,77,79,82,83,86,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,109,112,113,114,115,128,129,130,],[12,13,-76,-11,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-10,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-43,-44,-79,-10,-7,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,-8,-9,-60,-77,-83,135,136,137,]),'COLON_EQUALS':([8,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,83,113,123,],[15,87,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,87,-60,15,]),'COLON':([14,16,110,],[18,42,118,]),'L_PAREN':([15,17,19,21,22,24,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,116,123,131,132,148,],[22,43,62,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,62,22,22,22,]),'MINUS':([15,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,82,87,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,116,131,132,138,139,148,150,],[21,-76,68,21,21,-42,21,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,-43,68,-44,-79,21,68,68,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,68,-77,-83,21,21,21,68,68,21,68,]),'NOT':([15,21,22,24,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,116,131,132,148,],[24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'INT_LITERAL':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'DOUBLE_LITERAL':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'STRING_LITERAL':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'BOOLEAN_LITERAL':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'CHAR_LITERAL':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'FLOAT_LITERAL':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'L_S_BRACKET':([15,18,19,21,22,24,40,42,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,118,131,132,148,],[40,60,61,40,40,40,40,60,60,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,60,40,40,40,]),'L_BRACKET':([15,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,79,82,87,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,113,114,115,116,121,131,132,138,139,147,148,150,],[41,-76,41,41,-42,41,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,41,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,-43,-44,-79,41,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,41,-60,-77,-83,41,122,41,41,140,141,149,41,152,]),'INT':([18,42,60,118,],[53,53,53,53,]),'DOUBLE':([18,42,60,118,],[54,54,54,54,]),'STRING':([18,42,60,118,],[55,55,55,55,]),'BOOLEAN':([18,42,60,118,],[56,56,56,56,]),'CHAR':([18,42,60,118,],[57,57,57,57,]),'FLOAT':([18,42,60,118,],[58,58,58,58,]),'VOID':([18,42,60,118,],[59,59,59,59,]),'MULTIPLY':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,63,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,63,-44,-79,63,63,-27,-28,-29,-30,63,63,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,63,-77,-83,63,63,63,]),'DIVIDE':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,64,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,64,-44,-79,64,64,-27,-28,-29,-30,64,64,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,64,-77,-83,64,64,64,]),'MOD':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,65,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,65,-44,-79,65,65,-27,-28,-29,-30,65,65,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,65,-77,-83,65,65,65,]),'POWER':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,66,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,66,-44,-79,66,66,66,66,66,66,66,66,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,66,-77,-83,66,66,66,]),'PLUS':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,67,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,67,-44,-79,67,67,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,67,-77,-83,67,67,67,]),'LESS':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,69,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,69,-44,-79,69,69,69,69,69,69,69,69,None,None,None,None,None,None,-39,-40,-41,-78,69,-77,-83,69,69,69,]),'GREATER':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,70,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,70,-44,-79,70,70,70,70,70,70,70,70,None,None,None,None,None,None,-39,-40,-41,-78,70,-77,-83,70,70,70,]),'GREATER_EQUAL':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,71,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,71,-44,-79,71,71,71,71,71,71,71,71,None,None,None,None,None,None,-39,-40,-41,-78,71,-77,-83,71,71,71,]),'LESS_EQUAL':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,72,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,72,-44,-79,72,72,72,72,72,72,72,72,None,None,None,None,None,None,-39,-40,-41,-78,72,-77,-83,72,72,72,]),'EQUALS':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,73,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,73,-44,-79,73,73,73,73,73,73,73,73,None,None,None,None,None,None,-39,-40,-41,-78,73,-77,-83,73,73,73,]),'DIFFERENT':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,74,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,74,-44,-79,74,74,74,74,74,74,74,74,None,None,None,None,None,None,-39,-40,-41,-78,74,-77,-83,74,74,74,]),'AND':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,75,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,75,-44,-79,75,75,75,75,75,75,75,75,75,75,75,75,75,75,-39,-40,-41,-78,75,-77,-83,75,75,75,]),'OR':([19,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,77,78,79,82,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,112,114,115,138,139,150,],[-76,76,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-43,76,-44,-79,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,-40,-41,-78,76,-77,-83,76,76,76,]),'R_PAREN':([19,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,62,77,78,79,82,83,84,85,86,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,109,112,113,114,115,116,119,120,],[-76,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-10,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-86,-43,106,-44,-79,-10,110,-14,-7,115,-85,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,-8,-9,-60,-77,-83,-86,-13,-84,]),'R_S_BRACKET':([19,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,77,79,80,81,82,88,89,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,113,114,115,117,],[-76,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-82,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-43,-44,107,-81,-79,113,114,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,-82,-60,-77,-83,-80,]),'COMMA':([19,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,77,79,81,82,83,85,86,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,109,112,113,114,115,],[-76,-42,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-10,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-43,-44,108,-79,-10,111,-7,116,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-78,-8,-9,-60,-77,-83,]),'R_BRACKET':([41,124,125,126,127,134,135,136,137,142,143,145,146,151,153,154,155,156,],[82,133,-16,-17,-18,-15,-19,-20,-21,144,145,-26,-22,153,-25,155,-24,-23,]),'IF':([122,125,126,127,135,136,137,140,141,145,146,147,149,152,153,155,156,],[131,131,-17,-18,-19,-20,-21,131,131,-26,-22,148,131,131,-25,-24,-23,]),'WHILE':([122,125,126,127,135,136,137,140,141,145,146,149,152,153,155,156,],[132,132,-17,-18,-19,-20,-21,132,132,-26,-22,132,132,-25,-24,-23,]),'ELSE':([144,155,],[147,147,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'top_level_declarations':([0,3,],[2,11,]),'top_level_declaration':([0,3,],[3,3,]),'create_variable':([0,3,43,111,122,125,140,141,149,152,],[4,4,85,85,129,129,129,129,129,129,]),'assign':([0,3,122,125,140,141,149,152,],[5,5,128,128,128,128,128,128,]),'function':([0,3,],[6,6,]),'expression':([15,21,22,24,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,116,131,132,148,],[20,77,78,79,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,112,91,138,139,150,]),'value':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[23,23,23,23,81,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,81,23,23,23,23,]),'literal_int':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'literal_double':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'literal_string':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'literal_boolean':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'literal_char':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,]),'literal_float':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,]),'identifier':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'function_call':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,122,125,131,132,140,141,148,149,152,],[32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,130,130,32,32,130,130,32,130,130,]),'array':([15,21,22,24,40,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,87,108,116,131,132,148,],[33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,]),'type':([18,42,60,118,],[44,83,88,121,]),'type_int':([18,42,60,118,],[45,45,45,45,]),'type_double':([18,42,60,118,],[46,46,46,46,]),'type_string':([18,42,60,118,],[47,47,47,47,]),'type_boolean':([18,42,60,118,],[48,48,48,48,]),'type_char':([18,42,60,118,],[49,49,49,49,]),'type_float':([18,42,60,118,],[50,50,50,50,]),'type_void':([18,42,60,118,],[51,51,51,51,]),'type_array':([18,42,60,118,],[52,52,52,52,]),'values_list':([40,108,],[80,117,]),'parameter_list':([43,111,],[84,119,]),'t':([44,83,],[86,109,]),'arguments_list':([62,116,],[90,120,]),'block':([122,125,140,141,149,152,],[124,134,142,143,151,154,]),'statement':([122,125,140,141,149,152,],[125,125,125,125,125,125,]),'if_statement':([122,125,140,141,149,152,],[126,126,126,126,126,126,]),'while_statement':([122,125,140,141,149,152,],[127,127,127,127,127,127,]),'else_if_statements':([144,155,],[146,156,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> top_level_declarations','start',1,'p_start','mparser.py',17),
  ('top_level_declarations -> top_level_declaration top_level_declarations','top_level_declarations',2,'p_top_level_declarations','mparser.py',23),
  ('top_level_declarations -> top_level_declaration','top_level_declarations',1,'p_top_level_declarations','mparser.py',24),
  ('top_level_declaration -> create_variable SEMICOLON','top_level_declaration',2,'p_top_level_declaration','mparser.py',34),
  ('top_level_declaration -> assign SEMICOLON','top_level_declaration',2,'p_top_level_declaration','mparser.py',35),
  ('top_level_declaration -> function','top_level_declaration',1,'p_top_level_declaration','mparser.py',36),
  ('create_variable -> MUTABLE_VARIABLE ID COLON type t','create_variable',5,'p_create_variable','mparser.py',42),
  ('create_variable -> IMMUTABLE_VARIABLE ID COLON type t','create_variable',5,'p_create_variable','mparser.py',43),
  ('t -> COLON_EQUALS expression','t',2,'p_t','mparser.py',58),
  ('t -> <empty>','t',0,'p_t','mparser.py',59),
  ('assign -> ID COLON_EQUALS expression','assign',3,'p_assign','mparser.py',68),
  ('function -> FUNCTION ID L_PAREN parameter_list R_PAREN COLON type L_BRACKET block R_BRACKET','function',10,'p_function','mparser.py',74),
  ('parameter_list -> create_variable COMMA parameter_list','parameter_list',3,'p_parameter_list','mparser.py',80),
  ('parameter_list -> create_variable','parameter_list',1,'p_parameter_list','mparser.py',81),
  ('block -> statement block','block',2,'p_block','mparser.py',90),
  ('block -> statement','block',1,'p_block','mparser.py',91),
  ('statement -> if_statement','statement',1,'p_statement','mparser.py',100),
  ('statement -> while_statement','statement',1,'p_statement','mparser.py',101),
  ('statement -> assign SEMICOLON','statement',2,'p_statement','mparser.py',102),
  ('statement -> create_variable SEMICOLON','statement',2,'p_statement','mparser.py',103),
  ('statement -> function_call SEMICOLON','statement',2,'p_statement','mparser.py',104),
  ('if_statement -> IF expression L_BRACKET block R_BRACKET else_if_statements','if_statement',6,'p_if_statement','mparser.py',110),
  ('else_if_statements -> ELSE IF expression L_BRACKET block R_BRACKET else_if_statements','else_if_statements',7,'p_else_if_statements','mparser.py',119),
  ('else_if_statements -> ELSE IF expression L_BRACKET block R_BRACKET','else_if_statements',6,'p_else_if_statements','mparser.py',120),
  ('else_if_statements -> ELSE L_BRACKET block R_BRACKET','else_if_statements',4,'p_else_if_statements','mparser.py',121),
  ('while_statement -> WHILE expression L_BRACKET block R_BRACKET','while_statement',5,'p_while_statement','mparser.py',132),
  ('expression -> expression MULTIPLY expression','expression',3,'p_expression','mparser.py',138),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','mparser.py',139),
  ('expression -> expression MOD expression','expression',3,'p_expression','mparser.py',140),
  ('expression -> expression POWER expression','expression',3,'p_expression','mparser.py',141),
  ('expression -> expression PLUS expression','expression',3,'p_expression','mparser.py',142),
  ('expression -> expression MINUS expression','expression',3,'p_expression','mparser.py',143),
  ('expression -> expression LESS expression','expression',3,'p_expression','mparser.py',144),
  ('expression -> expression GREATER expression','expression',3,'p_expression','mparser.py',145),
  ('expression -> expression GREATER_EQUAL expression','expression',3,'p_expression','mparser.py',146),
  ('expression -> expression LESS_EQUAL expression','expression',3,'p_expression','mparser.py',147),
  ('expression -> expression EQUALS expression','expression',3,'p_expression','mparser.py',148),
  ('expression -> expression DIFFERENT expression','expression',3,'p_expression','mparser.py',149),
  ('expression -> expression AND expression','expression',3,'p_expression','mparser.py',150),
  ('expression -> expression OR expression','expression',3,'p_expression','mparser.py',151),
  ('expression -> L_PAREN expression R_PAREN','expression',3,'p_expression','mparser.py',152),
  ('expression -> value','expression',1,'p_expression','mparser.py',153),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','mparser.py',163),
  ('expression -> NOT expression','expression',2,'p_expression_not','mparser.py',167),
  ('type -> type_int','type',1,'p_type','mparser.py',172),
  ('type -> type_double','type',1,'p_type','mparser.py',173),
  ('type -> type_string','type',1,'p_type','mparser.py',174),
  ('type -> type_boolean','type',1,'p_type','mparser.py',175),
  ('type -> type_char','type',1,'p_type','mparser.py',176),
  ('type -> type_float','type',1,'p_type','mparser.py',177),
  ('type -> type_void','type',1,'p_type','mparser.py',178),
  ('type -> type_array','type',1,'p_type','mparser.py',179),
  ('type_int -> INT','type_int',1,'p_type_int','mparser.py',185),
  ('type_double -> DOUBLE','type_double',1,'p_type_double','mparser.py',191),
  ('type_string -> STRING','type_string',1,'p_type_string','mparser.py',197),
  ('type_boolean -> BOOLEAN','type_boolean',1,'p_type_boolean','mparser.py',203),
  ('type_char -> CHAR','type_char',1,'p_type_char','mparser.py',209),
  ('type_float -> FLOAT','type_float',1,'p_type_float','mparser.py',215),
  ('type_void -> VOID','type_void',1,'p_type_void','mparser.py',221),
  ('type_array -> L_S_BRACKET type R_S_BRACKET','type_array',3,'p_type_array','mparser.py',227),
  ('value -> literal_int','value',1,'p_value','mparser.py',233),
  ('value -> literal_double','value',1,'p_value','mparser.py',234),
  ('value -> literal_string','value',1,'p_value','mparser.py',235),
  ('value -> literal_boolean','value',1,'p_value','mparser.py',236),
  ('value -> literal_char','value',1,'p_value','mparser.py',237),
  ('value -> literal_float','value',1,'p_value','mparser.py',238),
  ('value -> identifier','value',1,'p_value','mparser.py',239),
  ('value -> function_call','value',1,'p_value','mparser.py',240),
  ('value -> array','value',1,'p_value','mparser.py',241),
  ('literal_int -> INT_LITERAL','literal_int',1,'p_literal_int','mparser.py',247),
  ('literal_double -> DOUBLE_LITERAL','literal_double',1,'p_literal_double','mparser.py',253),
  ('literal_string -> STRING_LITERAL','literal_string',1,'p_literal_string','mparser.py',259),
  ('literal_boolean -> BOOLEAN_LITERAL','literal_boolean',1,'p_literal_boolean','mparser.py',265),
  ('literal_char -> CHAR_LITERAL','literal_char',1,'p_literal_char','mparser.py',271),
  ('literal_float -> FLOAT_LITERAL','literal_float',1,'p_literal_float','mparser.py',277),
  ('identifier -> ID','identifier',1,'p_identifier','mparser.py',283),
  ('identifier -> ID L_S_BRACKET expression R_S_BRACKET','identifier',4,'p_identifier','mparser.py',284),
  ('array -> L_S_BRACKET values_list R_S_BRACKET','array',3,'p_array','mparser.py',293),
  ('array -> L_BRACKET R_BRACKET','array',2,'p_array','mparser.py',294),
  ('values_list -> value COMMA values_list','values_list',3,'p_values_list','mparser.py',300),
  ('values_list -> value','values_list',1,'p_values_list','mparser.py',301),
  ('values_list -> <empty>','values_list',0,'p_values_list','mparser.py',302),
  ('function_call -> ID L_PAREN arguments_list R_PAREN','function_call',4,'p_function_call','mparser.py',313),
  ('arguments_list -> expression COMMA arguments_list','arguments_list',3,'p_arguments_list','mparser.py',319),
  ('arguments_list -> expression','arguments_list',1,'p_arguments_list','mparser.py',320),
  ('arguments_list -> <empty>','arguments_list',0,'p_arguments_list','mparser.py',321),
]
