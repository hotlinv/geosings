
runstr ="""
import wx
class MyApp(wx.App):
    def OnInit(self):
        from geosings.ui.PyMainFrame import MainFrame
        from geosings.core.DefConf import GSSHOME,DOCHOME,BINHOME
        print "$HOME =",GSSHOME,'; $DOCHOME =',DOCHOME,
        print "; $BINHOME =", BINHOME
        mainframe = MainFrame(None, -1, "")
        mainframe.Show()

        return True


app = MyApp(False)
app.MainLoop()
"""

if __name__ == "__main__":
    import profile
    profile.run(runstr, "prof.plog")

