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
from gtk import glade
from gtk import gdk
import gobject
import gconf
import os
#import glob
import icon_library
#import imagelibrary

from simple_tree_parser import TreeParser

#from os import path

if not os.access("%s" % os.environ['HOME'] + '/.gnome2/gedit/plugins/CMYKProjectManager/CMYKProjectManager.projects', os.F_OK):
    os.system("touch %s" % os.environ['HOME'] + '/.gnome2/gedit/plugins/CMYKProjectManager/CMYKProjectManager.projects')

PROJECTS_FILE=os.environ['HOME'] + '/.gnome2/gedit/plugins/CMYKProjectManager/CMYKProjectManager.projects'

ui_str = """
<ui>
    <menubar name="MenuBar">
        <menu name="ToolsMenu" action="Tools">
            <placeholder name="ToolsOps_7">
                <menuitem name="Add Project" action="addProject"/>
            </placeholder>
        </menu>
    </menubar>
</ui>
"""

class CMYKProjectManager:
    TARGET_URI = 105
    dnd_target_list = [('text/uri-list', 0, TARGET_URI)]

    def __init__(self,  plugin, window):
#        print "Plugin created for", window
        self._window = window
        self._plugin = plugin

        self.create_menu_item()

        self.id_name = "CMYKProjectManager_Plugin"
        self.tree_parser = TreeParser()

        #imagelibrary.initialise()

        try: self.encoding = gedit.encoding_get_current()
        except: self.encoding = gedit.gedit_encoding_get_current()


        # create tab
        self._tab = gtk.ScrolledWindow()
        self._tab.set_property("hscrollbar-policy",gtk.POLICY_AUTOMATIC)
        self._tab.set_property("vscrollbar-policy",gtk.POLICY_AUTOMATIC)
        self._tab.set_property("shadow-type",gtk.SHADOW_IN)

#        self._tab.add(self._area)
#        self._tab.show_all()

#        sw = gtk.ScrolledWindow()
#       sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
#        sw.set_shadow_type(gtk.SHADOW_IN)
        self.projectbrowser = gtk.TreeView()
        self.projectbrowser.set_headers_visible(False)

        self._tab.add(self.projectbrowser)
        self.projectbrowser.connect("button_press_event",self.__onClick)

#        self.pack_start(self._tab)

        # add a text column to the treeview
        self.column = gtk.TreeViewColumn()
        self.column.set_sort_column_id(0) 
        self.projectbrowser.append_column(self.column)

        self.cellrendererpixbuf = gtk.CellRendererPixbuf()
        self.column.pack_start(self.cellrendererpixbuf,False)

        self.crt = gtk.CellRendererText()
        self.column.pack_start(self.crt,False)

        # connect stuff
        self.projectbrowser.connect("row-activated",self.on_row_activated)

        # connect Drag & Drop
        self.projectbrowser.connect('drag_data_received', self.on_tree_view_drag_data_received)

        # Set it as a drag source for exporting snippets
        self.projectbrowser.drag_source_set(gdk.BUTTON1_MASK, self.dnd_target_list, gdk.ACTION_DEFAULT | gdk.ACTION_COPY)

        # Set it as a drag destination for importing snippets
        self.projectbrowser.drag_dest_set(gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, self.dnd_target_list, gdk.ACTION_DEFAULT | gdk.ACTION_COPY)


#        self.show_all()

        self._tab.show_all()

        self.putTab()
        self.getProjectsList()

    def set_model(self):
        self.tree_parser.ls.set_sort_func(0, self.tree_parser.sort_tree)
        self.projectbrowser.set_model(self.tree_parser.ls)

    def create_menu_item(self):

        manager = self._window.get_ui_manager()
        self._action_group = gtk.ActionGroup("CMYKProjectManagerActions")
        pm_action = gtk.Action("addProject", _("Add Project"), _("Add a project in CMYK Project Manager"), gtk.STOCK_DIRECTORY)
#        pm_action.connect("activate", self.on_open_regex_dialog)
        self._action_group.add_action_with_accel( pm_action, "<Ctrl><Shift>a" )
        manager.insert_action_group( self._action_group, -1)
        manager.add_ui_from_string(ui_str)
        #manager.ensure_update()

    def getProjectsList(self):
        ilibrary = icon_library.GnomeFileIcons()
        self.projectbrowser.set_model(None)
        self.tree_parser.ls.clear()
        p_file = open(PROJECTS_FILE,"r")

        for line in p_file:
            line = line.strip()
            p_data = line.split('|')
            path = p_data[0]

            if (path == ''): continue
            if len(p_data) == 1:
                path_breadcrumb = path.split('/')
                p_alias =path_breadcrumb[len(path_breadcrumb)-2]
            else:
                p_alias = p_data[1]

#            i_name, pxbuf =ilibrary.set_icon(path)
            project_root = self.tree_parser.ls.append(None,( path, p_alias,'project_root', ilibrary.get_icon_pixbuf(path)))
            # Riga non corretta!! modificare..
            self.tree_parser.parsePath(path, project_root)

            #self.projectbrowser.set_model(self.tree_parser.ls)
            self.column.set_cell_data_func(self.crt, self.tree_parser.cellrenderer)
            self.column.set_cell_data_func(self.cellrendererpixbuf, self.tree_parser.pixbufrenderer)
        p_file.close()

        self.set_model()

#        self.column.set_cell_data_func(self.crt, self.tree_parser.cellrenderer)
#        self.column.set_cell_data_func(self.cellrendererpixbuf, parser.pixbufrenderer)
#            import os, glob
#           path = 'sequences/'
#for infile in glob.glob( os.path.join(path, '*.fasta') ):
#  print "current file is: " + infile

    def on_tree_view_drag_data_get(self, widget, context, selection_data, info, time):
        selection_data.set_uris(['file://' + gnomevfs.escape_path_string(self._temp_export)])

    def on_tree_view_drag_begin(self, widget, context):
        self.dragging = True


        # Generate temporary file name
        self.export_snippets(filename, False)
        self._temp_export = filename

    def on_tree_view_drag_end(self, widget, context):
            self.dragging = False

    def on_tree_view_drag_data_received(self, widget, context, x, y, selection, info, timestamp):
        uris = selection.get_uris()


        self.add_project(uris)

    def on_tree_view_drag_motion(self, widget, context, x, y, timestamp):
            # Return False if we are dragging
            if self.dragging:
                    return False

            # Check uri target
            if not gtk.targets_include_uri(context.targets):
                    return False

            # Check action
            action = None
            if context.suggested_action == gdk.ACTION_COPY:
                    action = gdk.ACTION_COPY
            else:
                for act in context.actions:
                    if act == gdk.ACTION_COPY:
                        action = gdk.ACTION_COPY
                        break

            if action == gdk.ACTION_COPY:
                context.drag_status(gdk.ACTION_COPY, timestamp)
                return True
            else:
                return False

    def remove_project_at_pos(self,path):
        c_path = self.tree_parser.ls[path]
        if c_path == None: return False
        else:
            file_path, file_name, file_type, file_icon=c_path
#            p_file = open(PROJECTS_FILE,"a")
#            p_file.close()
            data = open(PROJECTS_FILE, 'r').readlines()
            i=0
            while i<len(data):
                tmp = data[i].strip()
                if tmp == file_path or tmp == '':
                    del data[i]
                i = i+1
            open(PROJECTS_FILE,'w').writelines(data)

            # Refreshing projects list
            self.getProjectsList()


    def add_project(self, filenames):
        p_file = open(PROJECTS_FILE,"a")
        for filename in filenames:
            if (filename.find('file://')!=-1): filename = filename[7:]

            if not filename.endswith('/'): filename = filename+'/'

            if (os.path.isdir(filename) and not os.path.islink(filename)):
                p_file.write(filename+"\n")

        p_file.close()

        # Refreshing projects list
        self.getProjectsList()


    def putTab(self):
        panel = self._window.get_side_panel()
        icon = gtk.Image()
        icon.set_from_stock(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_MENU)
	
        panel.add_item(self._tab, "CMYKProjectManager", icon)



    def open_file_at_pos(self, path):

        c_path = self.tree_parser.ls[path]
        if c_path == None: return False
        else:
            file_path, file_name, file_type, file_icon=c_path
	    if os.path.isdir(file_path):
		if self.projectbrowser.row_expanded(path):
			self.projectbrowser.collapse_row(path)
		else:
			self.projectbrowser.expand_row(path,False)
	    else:
            	self.__openDocumentAtLine('file://'+file_path,1)

    def on_row_activated(self, treeview, path, view_column):

        self.open_file_at_pos(path)

        return True

    def open_project_folder(self, path):
        c_path = self.tree_parser.ls[path]
        if c_path == None: return False
        else:
            file_path, file_name, file_type, file_icon=c_path

            os.system("xdg-open '%s'" % file_path)

    def __onClick(self, treeview, event):
        #print "Clicked:Event>",event.button
        if event.button == 2:
            x, y = int(event.x), int(event.y)
            pthinfo = treeview.get_path_at_pos(x, y)

            if pthinfo is None: return
            path, col, cellx, celly = pthinfo
            self.open_file_at_pos(path)

            return True

        if event.button == 3:

            x, y = int(event.x), int(event.y)
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is None: return
            path, col, cellx, celly = pthinfo
            #treeview.grab_focus()
            #treeview.set_cursor(path)

            menu = gtk.Menu()

            # it's a project root!
            if len(path)==1:
                # Compress menubar
                #comp = gtk.ImageMenuItem(gtk.STOCK_CDROM)

                # Open Project Folder
                f = gtk.ImageMenuItem(gtk.STOCK_OPEN)
                menu.append(f)
                f.show()
                f.connect("activate",lambda w,p: self.open_project_folder(p), path)

                m = gtk.ImageMenuItem(gtk.STOCK_DELETE)
                menu.append(m)
                m.show()

                m.connect("activate", lambda w,p: self.remove_project_at_pos(p), path)
#            else:

            # add the menu items from the parser

#            m = gtk.SeparatorMenuItem()
#            m.show()
#            menu.append( m )


#            m = gtk.CheckMenuItem("autocollapse")
#            menu.append(m)
#            m.show()
#            m.set_active( options.singleton().autocollapse )
#            def setcollapse(w):
#                options.singleton().autocollapse = w.get_active()
#            m.connect("toggled", setcollapse )

                menu.popup( None, None, None, event.button, event.time)

        if event.button == 5:
            print "Double Clicked"

    def deactivate(self):
        print "Plugin stopped for", self._window
        self._window = None
        self._plugin = None
        self._action_group = None



    def __open_selected_document(self, path):
        try:
            path, line = self.parser.get_tag_position(self.projectbrowser.get_model(),path)
            self.__openDocumentAtLine(path, line)
        except:
            pass

    def update_ui(self):
        pass

    def __openDocumentAtLine(self, filename, line, column=1, register_history=True):
        """ open a the file specified by filename at the given line and column
        number. Line and column numbering starts at 1. """

        if line == 0 or column == 0:
            raise ValueError, "line and column numbers start at 1"

        documents = self._window.get_documents()
        found = None
        for d in documents:
            if d.get_uri() == filename:
                found = d
                break

        # open an existing tab or create a new one
        if found is not None:
            tab = gedit.tab_get_from_document(found)
            self._window.set_active_tab(tab)
            doc = tab.get_document()
            doc.begin_user_action()
            #it = doc.get_iter_at_line_offset(line-1,column-1)
            #doc.place_cursor(it)
            #(start, end) = doc.get_bounds()
            #self._window.get_active_view().scroll_to_iter(end,0.0)
            #self._window.get_active_view().scroll_to_iter(it,0.0)
            self._window.get_active_view().grab_focus()
            doc.end_user_action()
        else:
            tab = self._window.create_tab_from_uri(filename,self.encoding,line,False,False)
            self._window.set_active_tab(tab)
            found = self._window.get_active_document()

