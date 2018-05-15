
import sys
import pstats

if len(sys.argv)>1:
    pyname = sys.argv[1]+".py"
else:
    pyname = ""
p = pstats.Stats("prof.plog")
#"LayerCanvas.py"
p.strip_dirs().sort_stats("time").print_stats(pyname)

raw_input('press enter to exit...')
