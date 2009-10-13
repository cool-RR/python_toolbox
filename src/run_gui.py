import garlicsim
import garlicsim_wx

try:
    import psyco
    psyco_installed = True
except ImportError:
    psyco_installed = False

if __name__ == '__main__':
    
    if psyco_installed:
        pass # psyco.full()
        
    garlicsim_wx.main()