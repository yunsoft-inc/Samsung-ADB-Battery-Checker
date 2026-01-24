import wx
import sys
import subprocess
import re
wx.SizerFlags.DisableConsistencyChecks() 

import gettext
_ = gettext.gettext

def adb(cmd):
    result = subprocess.run(
        ["adb", cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result

def adb_batt(serial):
    result = subprocess.run(
        ["adb", "-s", serial, "shell", "dumpsys", "battery"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result

def get_adb_devices():
    r = adb("devices")
    devices = []
    for line in r.stdout.splitlines():
        if "\tdevice" in line:
            serial = line.split()[0]
            devices.append(serial)
    return devices

def find(pattern, text, cast=int):
    m = re.search(pattern, text)
    if not m:
        return -1
    try:
        return cast(m.group(1))
    except:
        return -1

def find(pattern, text, cast=int):
    if not text: return -1
    
    m = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return -1
    try:
        res = m.group(1).strip()
        return cast(res)
    except:
        return -1

def parse_battery_log(text):
    return [
        find(r"technology:\s*(\S+)", text, str),
        find(r"level:\s*(\d+)", text),
        find(r"^\s{2}voltage:\s*(\d+)", text),
        find(r"temperature:\s*(\d+)", text),
        find(r"Charge\s+counter:\s*(\d+)", text),
        find(r"current\s+now:\s*(-?\d+)", text),
        find(r"FirstUseDate:\s*\[(\d+)\]", text),
        find(r"LLB\s+CAL:\s*(\d+)", text),
        find(r"LLB\s+MAN:\s*(\d+)", text),
        find(r"LLB\s+CURRENT:\s*(\w+)", text, str),
        find(r"LLB\s+DIFF:\s*(\d+)", text),
        find(r"mSavedBatteryAsoc:\s*\[(\d+)\]", text),
        find(r"mSavedBatteryBsoh:\s*(\d+)", text),
        find(r"mSavedBatteryUsage:\s*\[(\d+)\]", text)
    ]


class Samsung_Battery_Tool ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Samsung Battery Tool By Yunsoft V1.0"), pos = wx.DefaultPosition, size = wx.Size( 800,800 ), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX) | wx.TAB_TRAVERSAL )

        #self.SetIcon(wx.Icon('img.ico', wx.BITMAP_TYPE_ICO))
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_SCROLLBAR ) )

        base_box = wx.BoxSizer( wx.HORIZONTAL )

        bSizer79 = wx.BoxSizer( wx.VERTICAL )

        device_box = wx.BoxSizer( wx.HORIZONTAL )

        devices_choiceChoices = []
        self.devices_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,-1 ), devices_choiceChoices, 0 )
        self.devices_choice.SetSelection( 0 )
        device_box.Add( self.devices_choice, 0, wx.ALL, 5 )

        self.Device_Refresh = wx.Button( self, wx.ID_ANY, _(u"Refresh"), wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
        device_box.Add( self.Device_Refresh, 0, wx.ALL, 5 )


        bSizer79.Add( device_box, 0, wx.EXPAND, 5 )

        Data = wx.BoxSizer( wx.VERTICAL )

        D1 = wx.BoxSizer( wx.HORIZONTAL )

        self.name4 = wx.StaticText( self, wx.ID_ANY, _(u"Battery Technology : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name4.Wrap( -1 )

        self.name4.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D1.Add( self.name4, 0, wx.ALIGN_CENTER, 5 )

        self.batttech_text = wx.TextCtrl( self, wx.ID_ANY, _(u"None"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.batttech_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D1.Add( self.batttech_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit.Wrap( -1 )

        self.unit.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D1.Add( self.unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D1, 1, wx.EXPAND, 30 )

        D2 = wx.BoxSizer( wx.HORIZONTAL )

        self.name1 = wx.StaticText( self, wx.ID_ANY, _(u"Battery Level : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name1.Wrap( -1 )

        self.name1.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D2.Add( self.name1, 0, wx.ALIGN_CENTER, 5 )

        bSizer18 = wx.BoxSizer( wx.VERTICAL )

        bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

        self.battlevel_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.battlevel_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer19.Add( self.battlevel_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit1 = wx.StaticText( self, wx.ID_ANY, _(u"%"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit1.Wrap( -1 )

        self.unit1.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer19.Add( self.unit1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer18.Add( bSizer19, 1, wx.EXPAND, 5 )

        self.battlevel_gauge = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 140,20 ), wx.GA_HORIZONTAL )
        self.battlevel_gauge.SetValue( 0 )
        bSizer18.Add( self.battlevel_gauge, 0, wx.ALIGN_LEFT|wx.ALL, 5 )


        D2.Add( bSizer18, 1, wx.ALIGN_CENTER, 5 )


        Data.Add( D2, 1, wx.EXPAND, 5 )

        D3 = wx.BoxSizer( wx.HORIZONTAL )

        self.name2 = wx.StaticText( self, wx.ID_ANY, _(u"Battery Voltage : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name2.Wrap( -1 )

        self.name2.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D3.Add( self.name2, 0, wx.ALIGN_CENTER, 5 )

        self.battvoltage_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.battvoltage_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D3.Add( self.battvoltage_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit2 = wx.StaticText( self, wx.ID_ANY, _(u"V"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit2.Wrap( -1 )

        self.unit2.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D3.Add( self.unit2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D3, 1, wx.EXPAND, 5 )

        D4 = wx.BoxSizer( wx.HORIZONTAL )

        self.name = wx.StaticText( self, wx.ID_ANY, _(u"Battery Temperature : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name.Wrap( -1 )

        self.name.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D4.Add( self.name, 0, wx.ALIGN_CENTER, 5 )

        self.batttemp_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.batttemp_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D4.Add( self.batttemp_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit21 = wx.StaticText( self, wx.ID_ANY, _(u"℃"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit21.Wrap( -1 )

        self.unit21.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D4.Add( self.unit21, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D4, 1, wx.EXPAND, 5 )

        D5 = wx.BoxSizer( wx.HORIZONTAL )

        self.name3 = wx.StaticText( self, wx.ID_ANY, _(u"Charge Counter : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name3.Wrap( -1 )

        self.name3.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D5.Add( self.name3, 0, wx.ALIGN_CENTER, 5 )

        self.chargecount_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.chargecount_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D5.Add( self.chargecount_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit211 = wx.StaticText( self, wx.ID_ANY, _(u"mAh"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit211.Wrap( -1 )

        self.unit211.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D5.Add( self.unit211, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D5, 1, wx.EXPAND, 5 )

        D6 = wx.BoxSizer( wx.HORIZONTAL )

        self.name31 = wx.StaticText( self, wx.ID_ANY, _(u"Current Now : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name31.Wrap( -1 )

        self.name31.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D6.Add( self.name31, 0, wx.ALIGN_CENTER, 5 )

        self.currentnow_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.currentnow_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D6.Add( self.currentnow_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit2111 = wx.StaticText( self, wx.ID_ANY, _(u"mA"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit2111.Wrap( -1 )

        self.unit2111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D6.Add( self.unit2111, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D6, 1, wx.EXPAND, 5 )

        D7 = wx.BoxSizer( wx.HORIZONTAL )

        self.name311 = wx.StaticText( self, wx.ID_ANY, _(u"Battery FirstUseDate : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name311.Wrap( -1 )

        self.name311.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D7.Add( self.name311, 0, wx.ALIGN_CENTER, 5 )

        self.battfirstuse_text = wx.TextCtrl( self, wx.ID_ANY, _(u"None"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.battfirstuse_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D7.Add( self.battfirstuse_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit21111 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit21111.Wrap( -1 )

        self.unit21111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D7.Add( self.unit21111, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D7, 1, wx.EXPAND, 5 )

        D8 = wx.BoxSizer( wx.HORIZONTAL )

        self.name3111 = wx.StaticText( self, wx.ID_ANY, _(u"LLB CAL : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name3111.Wrap( -1 )

        self.name3111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D8.Add( self.name3111, 0, wx.ALIGN_CENTER, 5 )

        self.llbcal_text = wx.TextCtrl( self, wx.ID_ANY, _(u"None"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.llbcal_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D8.Add( self.llbcal_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit211111 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit211111.Wrap( -1 )

        self.unit211111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D8.Add( self.unit211111, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D8, 1, wx.EXPAND, 5 )

        D9 = wx.BoxSizer( wx.HORIZONTAL )

        self.name31111 = wx.StaticText( self, wx.ID_ANY, _(u"LLB MAN : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name31111.Wrap( -1 )

        self.name31111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D9.Add( self.name31111, 0, wx.ALIGN_CENTER, 5 )

        self.llbman_text = wx.TextCtrl( self, wx.ID_ANY, _(u"None"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.llbman_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D9.Add( self.llbman_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit2111111 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit2111111.Wrap( -1 )

        self.unit2111111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D9.Add( self.unit2111111, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D9, 1, wx.EXPAND, 5 )

        D10 = wx.BoxSizer( wx.HORIZONTAL )

        self.name311111 = wx.StaticText( self, wx.ID_ANY, _(u"LLB CURRENT : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name311111.Wrap( -1 )

        self.name311111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D10.Add( self.name311111, 0, wx.ALIGN_CENTER, 5 )

        self.llbcur_text = wx.TextCtrl( self, wx.ID_ANY, _(u"None"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.llbcur_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D10.Add( self.llbcur_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit21111111 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit21111111.Wrap( -1 )

        self.unit21111111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D10.Add( self.unit21111111, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D10, 1, wx.EXPAND, 5 )

        D11 = wx.BoxSizer( wx.HORIZONTAL )

        self.name3111111 = wx.StaticText( self, wx.ID_ANY, _(u"LLB DIFF : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name3111111.Wrap( -1 )

        self.name3111111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D11.Add( self.name3111111, 0, wx.ALIGN_CENTER, 5 )

        self.llbdiff_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.llbdiff_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D11.Add( self.llbdiff_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit211111111 = wx.StaticText( self, wx.ID_ANY, _(u"WEEK"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit211111111.Wrap( -1 )

        self.unit211111111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D11.Add( self.unit211111111, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D11, 1, wx.EXPAND, 5 )

        D12 = wx.BoxSizer( wx.HORIZONTAL )

        self.name11 = wx.StaticText( self, wx.ID_ANY, _(u"ASOC : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name11.Wrap( -1 )

        self.name11.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D12.Add( self.name11, 0, wx.ALIGN_CENTER, 5 )

        bSizer181 = wx.BoxSizer( wx.VERTICAL )

        bSizer191 = wx.BoxSizer( wx.HORIZONTAL )

        self.asoc_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.asoc_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer191.Add( self.asoc_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit11 = wx.StaticText( self, wx.ID_ANY, _(u"%"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit11.Wrap( -1 )

        self.unit11.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer191.Add( self.unit11, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer181.Add( bSizer191, 1, wx.EXPAND, 5 )

        self.asoc_gauge = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 140,20 ), wx.GA_HORIZONTAL )
        self.asoc_gauge.SetValue( 0 )
        bSizer181.Add( self.asoc_gauge, 0, wx.ALIGN_LEFT|wx.ALL, 5 )


        D12.Add( bSizer181, 1, wx.ALIGN_CENTER, 5 )


        Data.Add( D12, 1, wx.EXPAND, 5 )

        D13 = wx.BoxSizer( wx.HORIZONTAL )

        self.name111 = wx.StaticText( self, wx.ID_ANY, _(u"BSOH : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name111.Wrap( -1 )

        self.name111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D13.Add( self.name111, 0, wx.ALIGN_CENTER, 5 )

        bSizer1811 = wx.BoxSizer( wx.VERTICAL )

        bSizer1911 = wx.BoxSizer( wx.HORIZONTAL )

        self.bsoh_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.bsoh_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer1911.Add( self.bsoh_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit111 = wx.StaticText( self, wx.ID_ANY, _(u"%"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit111.Wrap( -1 )

        self.unit111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer1911.Add( self.unit111, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer1811.Add( bSizer1911, 1, wx.EXPAND, 5 )

        self.bsoh_gauge = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 140,20 ), wx.GA_HORIZONTAL )
        self.bsoh_gauge.SetValue( 0 )
        bSizer1811.Add( self.bsoh_gauge, 0, wx.ALIGN_LEFT|wx.ALL, 5 )


        D13.Add( bSizer1811, 1, wx.ALIGN_CENTER, 5 )


        Data.Add( D13, 1, wx.EXPAND, 5 )

        D14 = wx.BoxSizer( wx.HORIZONTAL )

        self.name31111111 = wx.StaticText( self, wx.ID_ANY, _(u"BATTERY CYCLE : "), wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_RIGHT )
        self.name31111111.Wrap( -1 )

        self.name31111111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D14.Add( self.name31111111, 0, wx.ALIGN_CENTER, 5 )

        self.usage_text = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_RIGHT )
        self.usage_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D14.Add( self.usage_text, 0, wx.ALIGN_CENTER, 5 )

        self.unit2111111111 = wx.StaticText( self, wx.ID_ANY, _(u"TIMES"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.unit2111111111.Wrap( -1 )

        self.unit2111111111.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        D14.Add( self.unit2111111111, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        Data.Add( D14, 1, wx.EXPAND, 5 )

        GET = wx.BoxSizer( wx.HORIZONTAL )

        self.Get_btn = wx.Button( self, wx.ID_ANY, _(u"RECEIVE DATA FROM DEVICE"), wx.DefaultPosition, wx.Size( 500,50 ), 0 )
        self.Get_btn.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.Get_btn.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.Get_btn.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        GET.Add( self.Get_btn, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )


        Data.Add( GET, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )


        bSizer79.Add( Data, 1, wx.ALL|wx.EXPAND, 5 )


        base_box.Add( bSizer79, 1, wx.EXPAND, 5 )

        bSizer80 = wx.BoxSizer( wx.VERTICAL )

        self.raw_text = wx.TextCtrl( self, wx.ID_ANY, _(u"RAW Data"), wx.DefaultPosition, wx.Size( 260,600 ), wx.TE_MULTILINE )
        bSizer80.Add( self.raw_text, 0, wx.ALL, 5 )

        bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText86 = wx.StaticText( self, wx.ID_ANY, _(u"Enter Typical Battery : "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText86.Wrap( -1 )

        bSizer81.Add( self.m_staticText86, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_textCtrl44 = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.Size( 80,-1 ), wx.TE_RIGHT )
        self.m_textCtrl44.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer81.Add( self.m_textCtrl44, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticText87 = wx.StaticText( self, wx.ID_ANY, _(u"mAh"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText87.Wrap( -1 )

        bSizer81.Add( self.m_staticText87, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer80.Add( bSizer81, 0, 0, 5 )

        self.calmanualy = wx.Button( self, wx.ID_ANY, _(u"Manual Calculation"), wx.DefaultPosition, wx.Size( 260,-1 ), 0 )
        bSizer80.Add( self.calmanualy, 0, wx.ALL, 5 )


        base_box.Add( bSizer80, 1, wx.EXPAND, 5 )


        self.SetSizer( base_box )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.devices_choice.Bind( wx.EVT_CHOICE, self.DeviceSel )
        self.Device_Refresh.Bind( wx.EVT_BUTTON, self.Devicelist_Refresh )
        self.Get_btn.Bind( wx.EVT_BUTTON, self.recievedatabtn )
        self.calmanualy.Bind( wx.EVT_BUTTON, self.CalManualy )
        
        

    def __del__( self ):
        pass

    def DeviceSel( self, event ):
        index = self.devices_choice.GetSelection()
        serial = self.devices_choice.GetString(index)
        print(serial)

    def Devicelist_Refresh( self, event ):
        device_list = get_adb_devices()
        self.devices_choice.SetItems(device_list)
        
        if device_list:
            self.devices_choice.SetSelection(0)

    def recievedatabtn( self, event ):
        index = self.devices_choice.GetSelection()      
        if(index <= -1):
            dlg = wx.MessageDialog(
                None,
                "Please select your device first.",
                "Warning",
                wx.OK | wx.ICON_ERROR
            )
            dlg.ShowModal()
        else:
            serial = self.devices_choice.GetString(index)
            raw = adb_batt(serial).stdout
            output = parse_battery_log(raw)
            self.batttech_text.SetLabelText(output[0])
            self.battlevel_text.SetLabelText(str(output[1]))
            self.battlevel_gauge.SetValue(output[1])
            self.battvoltage_text.SetLabelText(str(output[2] / 1000))
            self.batttemp_text.SetLabelText(str(output[3] / 10))
            self.chargecount_text.SetLabelText(str(output[4] / 1000))
            self.currentnow_text.SetLabelText(str(output[5]))
            self.battfirstuse_text.SetLabelText(str(output[6]))
            self.llbcal_text.SetLabelText(str(output[7]))
            self.llbman_text.SetLabelText(str(output[8]))
            self.llbcur_text.SetLabelText(str(output[9]))
            self.llbdiff_text.SetLabelText(str(output[10]))
            self.asoc_text.SetLabelText(str(output[11]))
            self.asoc_gauge.SetValue(output[11])
            self.bsoh_text.SetLabelText(str(output[12]))
            self.bsoh_gauge.SetValue(output[12])
            self.usage_text.SetLabelText(str(output[13]))
            self.raw_text.SetLabelText(str(raw))
            
    def CalManualy( self, event ):
        typical = float(self.m_textCtrl44.GetValue())
        chargecount = float(self.chargecount_text.GetValue())
        level = int(self.battlevel_text.GetValue())

        if(level <= 0 or chargecount <= 0 or typical <= 0):
            dlg = wx.MessageDialog(
                None,
                "Please enter ChargeCount, Battery Level, and Typical Battery accurately.",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
            dlg.ShowModal()
        else:
            eff = (chargecount / (level / 100) / typical) * 100
            dlg = wx.MessageDialog(
                None,
                "The manually calculated value is " + str(round(eff, 2)) + "%.\nIt is an estimate, not an exact measurement, \nand is most accurate when the battery is around 50%\nand the temperature is between 20 and 30°C.",
                "Manual Calculation",
                wx.OK
            )
            dlg.ShowModal()

        
        
    
if __name__ == "__main__":
    app = wx.App(False)
    frame = Samsung_Battery_Tool(None)
    frame.Show()
    try:
        out = adb("version")
    except FileNotFoundError:
        dlg = wx.MessageDialog(
            None,
            "Install ADB first.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )
        dlg.ShowModal()
        sys.exit(0)
    
    app.MainLoop()
