import numpy as np
import os,sys
from datetime import date
today = date.today()
d2 = today.strftime("%B %d, %Y")

try:
    pfile = sys.argv[1].strip()
except:
    pfile = None

if (pfile is None) or pfile=='': pfile = "pubs.tsv"

combined = False
#ptype = 'significant'
ptype = 'student'


"""
Symbols from:
https://tug.ctan.org/info/symbols/comprehensive/symbols-a4.pdf
Colors from:
https://en.wikibooks.org/wiki/LaTeX/Colors

"""


a = np.genfromtxt(pfile,dtype=str,delimiter='\t',skip_header=1)
if ptype=='student':
    student_star_global = "{\\bf{\\faGraduationCap}}"
    sstr = "that I supervised or co-supervised the corresponding student-led publication"
elif ptype=='significant':
    student_star_global = "{\\bf {\\large *}}"
    sstr = "a significant publication"
    
peer_star_global = "\\textcolor{LimeGreen}{{\\Large \\bf{\\Checkedbox}}}~"
wait_star_global = "\\textcolor{Melon}{{\\faPause}}~"
hindex = 51
ncites = 12300

output = """
\\documentclass[11pt,usenames,dvipsnames]{article}

%\\usepackage{helvet}
%\\renewcommand{\\familydefault}{\\sfdefault}

%\\usepackage{librebaskerville}
%\\usepackage[T1]{fontenc}

%\\usepackage[T1]{fontenc}
%\\usepackage{ebgaramond}


%\\usepackage{fancyhdr}
\\usepackage{fontawesome}
\\usepackage{ccicons}
\\usepackage{marvosym}
\\usepackage{wrapfig}
\\usepackage[margin=2.5cm]{geometry}
\\usepackage{etaremune}

\\pagenumbering{gobble}

\\usepackage{amsthm}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage[colorlinks = true, linkcolor = blue, urlcolor = blue, citecolor = black, final]{hyperref}

\\usepackage{graphicx}
\\usepackage{multicol}
\\usepackage{ marvosym }
\\usepackage{wasysym}
\\usepackage{tikz}
\\usetikzlibrary{patterns}

\\newcommand{\\ds}{\\displaystyle}
\\DeclareMathOperator{\\sech}{sech}


\\setlength{\\parindent}{0in}

%\\lhead{Publications}
%\\chead{Mathew Madhavacheril}
%\\rhead{\\thepage}
%\\lfoot{}
%\\cfoot{}
%\\rfoot{}

\\begin{document}

%\\thispagestyle{fancy}
%\\pagestyle{fancy}

\\date{}

\\title{\\normalsize \\bf List of Publications -- Mathew Madhavacheril \\vspace{-3em}}

\\maketitle


h-index: """ + str(hindex) + """\\\\""" +str(ncites) + """+ citations\\\\
{\\bf Last updated: }
"""  + d2 + "\\\\" + \
"""
{\\bf Legend:} \\\\
""" + student_star_global + \
f""" indicates {sstr}.\\\\""" + peer_star_global + \
""" indicates that it has been accepted in a journal after peer-review.\\\\""" + wait_star_global + \
""" indicates that it is intended for peer-review but has not been accepted yet. \\\\
\\\\
Out of 129 articles, 109 are intended for peer-review and 100 of those have been accepted. \\\\
"""

if combined:
    headings = [""]
else:
    headings = [
    """
    \\textbf{Papers with major contributions}                                                                                                                                                            
    """,
    """
    \\textbf{Papers with some contribution}                                                                                                                                                            
    """]


encaps = """    
\\begin{enumerate} 
$COUNTER
$DATA
\\end{enumerate}  \\
"""

template = "\\item $TITLE\\\\ $AUTHORS, $MONTH/$YEAR$ARXIV\\emph{$JOURNAL} \n"
utemplate = template
#utemplate = "\\item $TITLE\\\\ $AUTHORS $ARXIV\\emph{$JOURNAL} \n"
count = 0
for i in range(len(headings)):
    if not(combined):
        idata = a[a[:,4]==str(i+1)]
    else:
        idata = a
    idata[:,1] = [x.zfill(2) for x in idata[:,1]]
    
    idata = idata[idata[:,1].argsort()] # First sort doesn't need to be stable.
    idata = idata[idata[:,0].argsort(kind='mergesort')]

    idata = idata[::-1]

    years = idata[:,0]
    months = idata[:,1]
    titles = idata[:,2]
    authors = idata[:,3]
    arxivs = idata[:,5]
    journals = idata[:,6]
    students = idata[:,7]
    peers = idata[:,8]
    subs = idata[:,9]

    output = output + headings[i]

    
    olist = ""
    ocount = count
    for year,month,title,author,arxiv,journal,student,peer,sub in zip(years,months,titles,authors,arxivs,journals,students,peers,subs):
        #title = '{\\it{%s}}' % title
        iarxiv = '' if arxiv=='' else ', \\href{https://arxiv.org/abs/'+arxiv+'}{arxiv:'+arxiv+'}'
        ijournal = '' if journal=='' else ', '+journal
        if i==0:
            temp = utemplate
        else:
            temp = template
        if int(student):
            student_star = student_star_global+"~"
        else:
            student_star = ""
        if int(peer):
            peer_star = peer_star_global
        else:
            peer_star = ""
        if int(sub) and not(int(peer)):
            wait_star = wait_star_global
        else:
            wait_star = ""
        olist = olist + temp.replace('$TITLE',student_star+peer_star+wait_star+title).replace('$AUTHORS',author).replace('$YEAR',year).replace('$ARXIV',iarxiv).replace('$JOURNAL',ijournal).replace('$MONTH',month)
        count = count + 1

    if i>0:
        cntr = "\\setcounter{enumi}{%d}" % ocount
    else:
        cntr = ""

    olist = olist.replace('M Madhavacheril','{\\bf{MS Madhavacheril}}').replace('MS Madhavacheril','{\\bf{MS Madhavacheril}}').replace('M. Madhavacheril','{\\bf{MS Madhavacheril}}').replace('M. S. Madhavacheril','{\\bf{MS Madhavacheril}}')
    output = output + encaps.replace("$COUNTER",cntr).replace("$DATA",olist)
    
output = output + """

\end{document}
"""

ostr = "_combined" if combined else ""
ofile = f"Publications{ostr}_{ptype}.tex"
with open(ofile, "w") as text_file:
    text_file.write(output)


os.system(f"pdflatex {ofile}")
