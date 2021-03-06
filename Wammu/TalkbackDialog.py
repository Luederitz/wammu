# -*- coding: UTF-8 -*-
#
# Copyright © 2003 - 2015 Michal Čihař <michal@cihar.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# generated by wxGlade 0.4.1 on Thu Feb  8 13:07:50 2007
# vim: expandtab sw=4 ts=4 sts=4:
'''
Wammu - Phone manager
Gammu Phone Database Talkback window
'''


import httplib
import urllib
import Wammu.Webbrowser
import re
import wx
import Wammu.TalkbackFeaturesDialog
import Wammu.Utils
import Wammu.Data
from Wammu.Locales import StrConv
from Wammu.Locales import ugettext as _
if Wammu.gammu_error is None:
    import gammu

OK_MATCHER = re.compile('Entry created, id=(\d*), url=(.*)')
FAIL_MATCHER = re.compile('Invalid values: (.*)')

# begin wxGlade: dependencies
# end wxGlade

class TalkbackDialog(wx.Dialog):
    def __init__(self, parent, config, phoneid = 0, *args, **kwds):
        # begin wxGlade: TalkbackDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, parent, *args, **kwds)
        self.main_panel = wx.Panel(self, -1)
        self.info_label = wx.StaticText(self, -1, _("Please share your experiences with Wammu and Gammu which is backend library. When you fill in following form, other users can benefit from your experiences in Gammu Phone Database. Only information you see here will be submited."))
        self.top_static_line = wx.StaticLine(self, -1)
        self.manufacturer_label = wx.StaticText(self.main_panel, -1, _("Manufacturer:"), style=wx.ALIGN_CENTRE)
        self.manufacturer_choice = wx.Choice(self.main_panel, -1, choices=[])
        self.model_label = wx.StaticText(self.main_panel, -1, _("Phone model:"))
        self.model_text_ctrl = wx.TextCtrl(self.main_panel, -1, "")
        self.connection_label = wx.StaticText(self.main_panel, -1, _("Connection type:"))
        self.connection_combo_box = wx.ComboBox(self.main_panel, -1, choices=[], style=wx.CB_DROPDOWN)
        self.gammu_model_label = wx.StaticText(self.main_panel, -1, _("Model in gammu configuration:"))
        self.model_combo_box = wx.ComboBox(self.main_panel, -1, choices=[], style=wx.CB_DROPDOWN)
        self.features_label = wx.StaticText(self.main_panel, -1, _("Working features:"))
        self.features_button = wx.Button(self.main_panel, -1, _("Please select features..."))
        self.gammu_version_text_label = wx.StaticText(self.main_panel, -1, _("Gammu version:"))
        self.gammu_version_label = wx.StaticText(self.main_panel, -1, "")
        self.note_label = wx.StaticText(self.main_panel, -1, _("Note:"))
        self.note_text_ctrl = wx.TextCtrl(self.main_panel, -1, "", style=wx.TE_MULTILINE)
        self.name_label = wx.StaticText(self.main_panel, -1, _("Your name:"))
        self.name_text_ctrl = wx.TextCtrl(self.main_panel, -1, "")
        self.email_label = wx.StaticText(self.main_panel, -1, _("Your email:"))
        self.email_text_ctrl = wx.TextCtrl(self.main_panel, -1, "")
        self.mangle_label = wx.StaticText(self.main_panel, -1, _("Email displaying:"), style=wx.ALIGN_CENTRE)
        self.mangle_choice = wx.Choice(self.main_panel, -1, choices=[_("Use [at] and [dot]"), _("Insert NOSPAM text at random position"), _("Display it normally"), _("Don't show email at all")])
        self.bottom_static_line = wx.StaticLine(self, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnFeatures, self.features_button)
        # end wxGlade
        self.ns_string = '<%s>' % _('Not supported')
        self.connection_combo_box.Append(self.ns_string)
        for x in Wammu.Data.Connections:
            self.connection_combo_box.Append(x)
        for x in Wammu.Data.Models:
            self.model_combo_box.Append(x)
        for x in Wammu.Data.ManufacturerMap.keys():
            self.manufacturer_choice.Append(x)
        self.wammu_cfg = config
        self.phoneid = phoneid
        self.features = []
        self.gammu_version_label.SetLabel(gammu.Version()[0])
        self.note_text_ctrl.SetValue('Report has been created using Wammu %s.\n' % Wammu.__version__)
        # Read phone name and manufacturer
        manufacturer = self.wammu_cfg.Read('/Phone-%d/Manufacturer' % phoneid)
        self.manufacturer_choice.SetStringSelection(manufacturer)
        model = self.wammu_cfg.Read('/Phone-%d/Model' % phoneid)
        self.model_text_ctrl.SetValue(model)
        # Set connection type which is being used
        section = self.wammu_cfg.ReadInt('/Gammu/Section')
        config = self.wammu_cfg.gammu.GetConfig(section)
        self.connection_combo_box.SetValue(config['Connection'])
        self.model_combo_box.SetValue(config['Model'])
        self.name_text_ctrl.SetValue(self.wammu_cfg.Read('/User/Name'))
        self.email_text_ctrl.SetValue(self.wammu_cfg.Read('/User/Email'))


    def __set_properties(self):
        # begin wxGlade: TalkbackDialog.__set_properties
        self.SetTitle(_("Gammu Phone Database Talkback"))
        self.features_label.SetToolTipString(_("Select which features work correctly with your phone"))
        self.gammu_version_label.SetToolTipString(_("This information is automatically included in report."))
        self.note_text_ctrl.SetToolTipString(_("Describe some glitches of this phone or other experiences with Gammu."))
        self.email_text_ctrl.SetToolTipString(_("Please enter valid mail here, choose display options below. Your email won't be given or sold to anybody."))
        self.mangle_choice.SetToolTipString(_("If you don't want to display email clear text, please select one mangling option."))
        self.mangle_choice.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        self.button_sizer = wx.StdDialogButtonSizer()
        self.button_sizer.AddButton(wx.Button(self, wx.ID_OK))
        self.button_sizer.AddButton(wx.Button(self, wx.ID_CANCEL))
        self.info_label.Wrap(400)
        # begin wxGlade: TalkbackDialog.__do_layout
        window_grid_sizer = wx.FlexGridSizer(5, 1, 0, 0)
        main_grid_sizer = wx.FlexGridSizer(10, 2, 5, 5)
        window_grid_sizer.Add(self.info_label, 2, wx.ALL|wx.EXPAND, 5)
        window_grid_sizer.Add(self.top_static_line, 0, wx.ALL|wx.EXPAND, 5)
        main_grid_sizer.Add(self.manufacturer_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.manufacturer_choice, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.model_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.model_text_ctrl, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.connection_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.connection_combo_box, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.gammu_model_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.model_combo_box, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.features_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.features_button, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.gammu_version_text_label, 0, wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.gammu_version_label, 0, wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.note_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.note_text_ctrl, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.name_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.name_text_ctrl, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.email_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.email_text_ctrl, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.mangle_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        main_grid_sizer.Add(self.mangle_choice, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        self.main_panel.SetAutoLayout(True)
        self.main_panel.SetSizer(main_grid_sizer)
        main_grid_sizer.Fit(self.main_panel)
        main_grid_sizer.SetSizeHints(self.main_panel)
        main_grid_sizer.AddGrowableRow(5)
        main_grid_sizer.AddGrowableCol(1)
        window_grid_sizer.Add(self.main_panel, 0, wx.EXPAND, 0)
        window_grid_sizer.Add(self.bottom_static_line, 0, wx.ALL|wx.EXPAND, 3)
        self.SetAutoLayout(True)
        self.SetSizer(window_grid_sizer)
        window_grid_sizer.Fit(self)
        window_grid_sizer.SetSizeHints(self)
        window_grid_sizer.AddGrowableRow(1)
        window_grid_sizer.AddGrowableCol(0)
        self.Layout()
        # end wxGlade
        self.button_sizer.Realize()
        window_grid_sizer.Add(self.button_sizer, 0, wx.ALIGN_RIGHT, 0)
        window_grid_sizer.Fit(self)
        self.Layout()
        wx.EVT_BUTTON(self, wx.ID_OK, self.Okay)

    def OnFeatures(self, event): # wxGlade: TalkbackDialog.<event_handler>
        dlg = Wammu.TalkbackFeaturesDialog.TalkbackFeaturesDialog(self)
        dlg.SetFeatures(self.features)
        if dlg.ShowModal() == wx.ID_OK:
            self.features = dlg.GetFeatures()
            self.features_button.SetLabel(', '.join(self.features))

    def Okay(self, evt):
        connection = self.connection_combo_box.GetValue()
        if connection == self.ns_string:
            connection = 'NULL'
        if len(self.features) == 0 and connection != 'NULL':
            wx.MessageDialog(self,
                _('Entry in Gammu Phone Database was not created, following fields are invalid:\n%s') % _('Supported features'),
                _('Entry not created!'),
                wx.OK | wx.ICON_ERROR).ShowModal()
            return
        elif len(self.features) != 0 and connection == 'NULL':
            wx.MessageDialog(self,
                _('Entry in Gammu Phone Database was not created, following fields are invalid:\n%s') % _('Supported features'),
                _('Entry not created!'),
                wx.OK | wx.ICON_ERROR).ShowModal()
            return
        man_str = self.manufacturer_choice.GetStringSelection()
        try:
            man_id = Wammu.Data.ManufacturerMap[man_str]
        except:
            wx.MessageDialog(self,
                _('Entry in Gammu Phone Database was not created, following fields are invalid:\n%s') % _('Manufacturer'),
                _('Entry not created!'),
                wx.OK | wx.ICON_ERROR).ShowModal()
            return
        garble_id = self.mangle_choice.GetSelection()
        try:
            garble_text = Wammu.Data.GarbleMap[garble_id]
        except:
            wx.MessageDialog(self,
                _('Entry in Gammu Phone Database was not created, following fields are invalid:\n%s') % _('Email displaying'),
                _('Entry not created!'),
                wx.OK | wx.ICON_ERROR).ShowModal()
            return

        # Remember user information for next run
        self.wammu_cfg.Write('/User/Name', self.name_text_ctrl.GetValue())
        self.wammu_cfg.Write('/User/Email', self.email_text_ctrl.GetValue())

        # Prepare data to post
        params_dict = {
            'irobot': 'wammu',
            'version': '2',
            'manufacturer': man_id,
            'name': self.model_text_ctrl.GetValue(),
            'model': self.model_combo_box.GetValue(),
            'connection': connection,
            'note': self.note_text_ctrl.GetValue(),
            'author_name': self.name_text_ctrl.GetValue(),
            'author_email': self.email_text_ctrl.GetValue(),
            'email_garble': garble_text,
            'gammu_version': gammu.Version()[0],
        }
        for x in self.features:
            params_dict['fts[%s]' % x] = 1

        # Convert unicode to raw utf-8 strigns so that they can be properly
        # handled by urllib and later by website
        for x in params_dict.keys():
            if type(params_dict[x]) == unicode:
                params_dict[x] = params_dict[x].encode('utf-8')

        # Encode request and prepare headers
        params = urllib.urlencode(params_dict)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/plain'}

        # Perform request
        conn = httplib.HTTPConnection('wammu.eu')
        try:
            conn.request('POST', '/api/phones/new/', params, headers)

            # Check request response
            response = conn.getresponse()
            if response.status != 200:
                wx.MessageDialog(self,
                    _('HTTP request failed with status %(code)d (%(text)s), please retry later or create entry manually.') % {
                        'code': response.status,
                        'text': response.reason,
                        },
                    _('Entry not created!'),
                    wx.OK | wx.ICON_ERROR).ShowModal()
                return
        except Exception, e:
            if hasattr(e, 'message') and e.message != '':
                msg = e.message
            elif hasattr(e, 'args') and len(e.args) > 0:
                msg = e.args[-1]
            else:
                msg = str(e)
            wx.MessageDialog(self,
                _('HTTP request failed with exception:\n%(exception)s\nPlease retry later or create entry manually.') % {
                    'exception': StrConv(msg),
                    },
                _('Entry not created!'),
                wx.OK | wx.ICON_ERROR).ShowModal()
            return

        # Verify acquired data
        data = response.read()
        conn.close()
        ok_test = OK_MATCHER.match(data)
        if ok_test is not None:
            url = 'http://%swammu.eu%s' % (Wammu.Utils.GetWebsiteLang(), ok_test.groups()[1])
            if wx.MessageDialog(self,
                _('Entry in Gammu Phone Database has been created, you can see it on <%s> URL.\nDo you want to open it in browser now?') % url,
                _('Entry created!'),
                wx.YES_NO | wx.ICON_INFORMATION).ShowModal() == wx.ID_YES:
                Wammu.Webbrowser.Open(url)
            self.wammu_cfg.Write('/Wammu/TalkbackDone', 'yes')

            self.EndModal(wx.ID_OK)

        fail_test = FAIL_MATCHER.match(data)
        if fail_test is not None:
            wrong_fields = fail_test.groups()[0].split(',')
            fields_msg = ''
            for field in wrong_fields:
                if field == 'manufacturer':
                    fields_msg += _('Manufacturer') + '\n'
                elif field == 'name':
                    fields_msg += _('Phone model') + '\n'
                elif field == 'model':
                    fields_msg += _('Model in gammu configuration') + '\n'
                elif field == 'connection':
                    fields_msg += _('Connection type') + '\n'
                elif field == 'note':
                    fields_msg += _('Note') + '\n'
                elif field == 'author_name':
                    fields_msg += _('Your name') + '\n'
                elif field == 'author_email':
                    fields_msg += _('Your email') + '\n'
                elif field == 'email_garble':
                    fields_msg += _('Email displaying') + '\n'
                elif field == 'gammu_version':
                    fields_msg += _('Gammu version') + '\n'
                else:
                    fields_msg += _('Field: %s') % field + '\n'

            wx.MessageDialog(self,
                _('Entry in Gammu Phone Database was not created, following fields are invalid:\n%s') % fields_msg,
                _('Entry not created!'),
                wx.OK | wx.ICON_ERROR).ShowModal()
            return

# end of class TalkbackDialog

def DoTalkback(parent, config, phoneid = 0):
    dlg = TalkbackDialog(parent, config, phoneid)
    dlg.Show()
