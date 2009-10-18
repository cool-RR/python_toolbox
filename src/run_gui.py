import sys
import garlicsim
import garlicsim_wx

arguments = sys.argv[1:]
debug = '-debug' in arguments

use_psyco = False
if not debug:
    try:
        import psyco
        use_psyco = True
    except ImportError:
        pass
    
if __name__ == '__main__':
    
    if use_psyco:
        psyco.full()
        
    garlicsim_wx.main()