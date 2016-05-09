
###################################SQL INJECTION ##################################
LOGIN_REGEX_PATTERNS = [
    "\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))", # Typical Form
    "((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))",  # meta-characters
    "((\%27)|(\'))union",
    "((\%27)|(\'))insert",
    "((\%27)|(\'))update",
    "((\%27)|(\'))delete",
    "((\%27)|(\'))drop",
    "((\%27)|(\'))alter",
    "((\%27)|(\'))create",
    "(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})",
    "((\%41\%4c\%54\%45\%52)|(\%43\%52\%45\%41\%54\%45)|(\%44\%45\%4c\%45\%54\%45)|(\%44\%52\%4f\%50)|(\%45\%58\%45\%43)((\%55\%54\%45)){0,1}|(\%49\%4e\%53\%45\%52\%54)( +(\%49\%4e\%54\%4f)){0,1}|(\%4d\%45\%52\%47\%45)|(\%53\%45\%4c\%45\%43\%54)|(\%55\%50\%44\%41\%54\%45)|(\%55\%4e\%49\%4f\%4e)( +(41 4c 4c)){0,1})"

]

###################################### XSS #######################################
#All the possible combinations of the character "<"
#in HTML and JavaScript. Most of these won't render out of the box,
#but many of them can get rendered in certain circumstances
#as seen above.

COMINATION_OWASP_XSS=[
"<",
"%3C",
"&lt",
"&lt;",
"&LT",
"&LT;",
"&#60",
"&#060",
"&#0060",
"&#00060",
"&#000060",
"&#0000060",
"&#60;",
"&#060;",
"&#0060;",
"&#00060;",
"&#000060;",
"&#0000060;",
"&#x3c",
"&#x03c",
"&#x003c",
"&#x0003c",
"&#x00003c",
"&#x000003c",
"&#x3c;",
"&#x03c;",
"&#x003c;",
"&#x0003c;",
"&#x00003c;",
"&#x000003c;",
"&#X3c",
"&#X03c",
"&#X003c",
"&#X0003c",
"&#X00003c",
"&#X000003c",
"&#X3c;",
"&#X03c;",
"&#X003c;",
"&#X0003c;",
"&#X00003c;",
"&#X000003c;",
"&#x3C",
"&#x03C",
"&#x003C",
"&#x0003C",
"&#x00003C",
"&#x000003C",
"&#x3C;",
"&#x03C;",
"&#x003C;",
"&#x0003C;",
"&#x00003C;",
"&#x000003C;",
"&#X3C",
"&#X03C",
"&#X003C",
"&#X0003C",
"&#X00003C",
"&#X000003C",
"&#X3C;",
"&#X03C;",
"&#X003C;",
"&#X0003C;",
"&#X00003C;",
"&#X000003C;",
"\x3c",
"\x3C",
"\u003c",
"\u003C"]

XSS_REGEX_LIST_PRIMARY=[
  "((\%3C)|<)[^\n]+((\%3E)|>)",  #paranoid matching method -->> catches everything have <
  "((\%3C)|<)((\%69)|i|(\%49))((\%6D)|m|(\%4D))((\%67)|g|(\%47))[^\n]+((\%3E)|>)", # img tag
   "((\%3C)|<)((\%2F)|\/)*[a-z0-9\%]+((\%3E)|>)" # typic xss form
]

XSS_COMPLETE_REGEX_LIST= XSS_REGEX_LIST_PRIMARY + COMINATION_OWASP_XSS

def Generate_Whole_Pattern(regex_list):
    pattern=""
    for i in range(len(regex_list)):
        if i==len(regex_list)-1:
            pattern+='('+regex_list[i]+')'
        else:
            pattern+='('+regex_list[i]+')'+"|"
    return pattern
