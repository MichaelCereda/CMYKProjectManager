# Copyright (C) 2009 Michael Cereda (michael.cereda@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA 02111-1307, USA.

import gedit
import gtk
from CMYKProjectManager import CMYKProjectManager



class CMYKProjectManagerPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = CMYKProjectManager(self, window)

    def deactivate(self, window):
        pane = window.get_side_panel()
        pane.remove_item(self._instances[window])

        #windowdata = window.get_data("ClassBrowserPluginWindowDataKey")

        self._instances[window].deactivate()
        del self._instances[window]
#        manager = window.get_ui_manager()

        #manager.remove_action_group(windowdata["action_group"])

    def update_ui(self, window):
        view = window.get_active_view()
        self._instances[window].update_ui()
#        windowdata = window.get_data("ClassBrowserPluginWindowDataKey")

