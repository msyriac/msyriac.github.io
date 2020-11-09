import os,sys
import glob

files = sorted(glob.glob("*.csv"), key=str.casefold)

mstr = """<div class='grid-container'>$ITEM
</div>"""

istr = """
  <div class='grid-item'>
	<h3>$HEADING</h3>
$PRIV_DIV
	<ul>$LIST
	</ul>
$END_PRIV_DIV
  </div>"""

lstr = """
	  <li>
	  \t<a href='$LINK' target='_blank'> $LITEM </a>
	  </li>"""

cistr = ""
for fname in files:
    with open(fname) as f:
        clstr = ""
        for i,line in enumerate(f):
            if i==0:
                heading,private = line.strip().split(',')
                continue
            if private=='true':
                pdiv1 = """
                <div class='private'>
                  <p style="color:#cc2222;">
                    HIDDEN
                    </p>
                  </div>
                <div class='private' style=\"display: none;\">
                """
                pdiv2 = "</div>"
            elif private=='false':
                pdiv1 = ""
                pdiv2 = ""
            else:
                raise ValueError
                    
            flist = line.split(',')
            litem = flist[0].strip()
            link = ','.join(flist[1:]).strip()
            clstr = clstr + str(lstr).replace('$LINK',link).replace('$LITEM',litem)
    
    cistr = cistr + str(istr).replace('$HEADING',heading).replace('$LIST',clstr).replace('$PRIV_DIV',pdiv1).replace('$END_PRIV_DIV',pdiv2)

        
mstr = mstr.replace('$ITEM',cistr)

with open('grid.html','w') as f:
    f.write(mstr)
