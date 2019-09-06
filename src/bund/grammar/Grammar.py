##
##
##

GRAMMAR="""
//
// Main theBund statements and configurations
//
Bund:
  env        *= EnvStatementDef[","]
  namespaces *=NamespaceDef
;
//
// theBund basic definitions
//
NameDef:
  ID | STRING
;
SimpleDataDef:
  ID | STRING
;
Arity:
  "|" arity += ArityDef[","] "|"
;
ArityDef:
  ID | "_" | "*" | NUMBER
;
DefTypes:
  "data" | "var"
;
DefClauses:
  "history" | "env" | "io"
;
KeyWords:
  DirectDataAssignmentOp | ReverseDataAssignmentOp | DefTypes | DefClauses
;
SpecialWords1:
  "<<" | ">>" | "*" | "-" | "**" | "***" | "--" | "---" | "><" | "<>"
;
SpecialWords2:
  "+" | "++" | "+++"
;
LogicalOp:
  "||" | "&&" | "^" | "and" | "or" | "not"
;
CompareOp:
  "=" | "<>" | ">" | "<" | ">=" | "<=" | "is"
;
SpecialWords:
  SpecialWords1 | SpecialWords2 | LogicalOp | CompareOp
;
//
// theBund operations definition
//
DirectDataAssignmentOp:
  "is" | "<-"
;
ReverseDataAssignmentOp:
  "->" | "as"
;
EnvStatementDef:
  DirectEnvironmentAssignmentDef | ReverseEnvironmentAssignmentDef
;
//
// Defining environment of the script or module
//
DirectEnvironmentAssignmentDef:
  NameDef DirectDataAssignmentOp SimpleDataDef
;
ReverseEnvironmentAssignmentDef:
  SimpleDataDef ReverseDataAssignmentOp NameDef
;
//
// Assignments
//
DirectAssignmentDef:
  name=NameDef DirectDataAssignmentOp  arity=Arity? data=DataDefinition
;
ReverseAssignmentDef:
  data=DataDefinition arity=Arity? ReverseDataAssignmentOp name=NameDef
;
AssignmentOp:
  DirectAssignmentDef | ReverseAssignmentDef
;
AssignmentDef:
  atype=DefTypes "is"
    data *= AssignmentOp[","]
  ";;"
;
//
// Clause
//
ClauseDataDef:
  SimpleDataDef | DictSimpleDataDef
;
DirectAssignClauseDef:
  name = NameDef DirectDataAssignmentOp? data *= ClauseDataDef[","]
;
ReverseAssignClauseDef:
  data *= ClauseDataDef[","] ReverseDataAssignmentOp name = NameDef
;
AssignClauseDef:
  DirectAssignClauseDef | ReverseAssignClauseDef
;
DirectAssignClauseKVDef:
  name = NameDef DirectDataAssignmentOp data = SimpleDataDef
;

ReverseAssignClauseKVDef:
  data = SimpleDataDef ReverseDataAssignmentOp name = NameDef
;
AssignClauseKVDef:
  DirectAssignClauseKVDef | ReverseAssignClauseKVDef
;

DictSimpleDataDef:
  "{" data *= AssignClauseKVDef[","] "}"
;
DictInstantDataDef:
  "-" data *=AssignClauseKVDef
;
ClausesDef:
  AssignClauseDef | DictInstantDataDef
;
ClauseDef:
  ctype=DefClauses "is"
    clauses *= ClausesDef[";"]
  ";;"
;
//
// Pipelines
//
PipelineDef:
  "pipeline" name=NameDef "is"
    steps *= PipelineStepsDef["|"]
  ";;"
;
PipelineStepsDef:
  NameDef | FQWord | ChannelDef | PipelineGroupDef
;
PipelineComponentsDef:
  NameDef | FQWord
;
ChannelDef:
  "[" name=PipelineComponentsDef "]"
;
PipelineGroupDef:
  "(" steps *= PipelineComponentsDef[","] ")"
;
//
// Data
//
FQWord:
  ":" path += NameDef[":"]
;
BundExecWordDef:
  NameDef | FQWord
;
CurryDef:
  name = "#[" BundExecWordDef "@" param=DataDefinition "]"
;
LazyEvalWordDef:
  ":[" name=BundExecWordDef "]"
;
LazyEvalWordOp:
  "!"
;
ListDef:
  "[" data *= DataDefinition[","] "]"
;
DictElementDef:
  DirectAssignmentDef | ReverseAssignmentDef
;
DictDef:
  "{" data *= DictElementDef[","] "}"
;
RecordDef:
  "?{" data *= NameDef[","] "}"
;
CodeBlockDef:
  "(" words *= ParametrizedCodeWords ")"
;
CodeBlockRefDef:
  "`(" words *= ParametrizedCodeWords ")"
;
RunCodeBlockOp:
  "."
;
CondCodeBlockDef:
  "?(" words *= CodeWords ")"
;
CodeWords:
  ! KeyWords | DataDefinition | SpecialWords | FQWord | LazyEvalWordDef | LazyEvalWordOp | CondCodeBlockDef | RunCodeBlockOp
;
ParametrizedCodeWords:
  data=CodeWords ("/" arity*=DataDefinition[","] "/")?
;
DataDefinition:
  BASETYPE | ListDef | DictDef | RecordDef | CodeBlockDef | CodeBlockRefDef | CurryDef
;
//
// Namespace definitions
//
NamespaceDef:
  "[" name=NameDef ">"
    elements *= ElementsDef
  ";;"
;
//
// Elements definition
//
ElementsDef:
  NamespaceDef | AssignmentDef | ClauseDef | PipelineDef
;
//
// Comments
//
Comment:
  /##.*$|\/\/.*$/|/\/\*(.|\n)*?\*\//
;

"""

def bund_grammar()
    return GRAMMAR
