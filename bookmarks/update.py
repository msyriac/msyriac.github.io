import os,sys
import glob

files = sorted(glob.glob("*.csv"), key=str.casefold)

mstr = """<div class='grid-container'>$ITEM
</div>"""

istr = """
  <div class='grid-item'>
	<h3>$HEADING</h3>
	<ul>$LIST
	</ul>
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
                heading = line.strip()
                continue
            flist = line.split(',')
            litem = flist[0].strip()
            link = ','.join(flist[1:]).strip()
            clstr = clstr + str(lstr).replace('$LINK',link).replace('$LITEM',litem)
    
    cistr = cistr + str(istr).replace('$HEADING',heading).replace('$LIST',clstr)

        
mstr = mstr.replace('$ITEM',cistr)

with open('grid.html','w') as f:
    f.write(mstr)
