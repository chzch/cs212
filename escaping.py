# User Instructions
# 
# Implement the function escape_html(s), which replaces:
# > with &gt;
# < with &lt;
# " with &quot;
# & with &amp;
# and returns the escaped string
# Note that your browser will probably automatically 
# render your escaped text as the corresponding symbols, 
# but the grading script will still correctly evaluate it.
# 
import cgi


#uryyb &quot;&gt; jbeyq

def rotify(s):
    for char in s:
        print int(char) 
    return 

def escape_html(s):
    return cgi.escape(s, quote=True)

text = rotify(escape_html('hello "> world'))
print text
print rotify(escape_html(text))
