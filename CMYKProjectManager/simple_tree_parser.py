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

import gtk
import os
import icon_library


class TreeParser():
    def __init__(self):
        # id, filename, description, [pixbuf]
        self.ls = gtk.TreeStore( str, str ,str, gtk.gdk.Pixbuf )
        
        self.currentfile = None
        self.ilibrary = icon_library.GnomeFileIcons()
        
    def sort_tree(self, model, item1, item2, column):
        data1 = model.get_value(iter1, 0)[column]
        data2 = model.get_value(iter1, 0)[column]  
        print "sorting:", data1, data2, cmp(data1,data2)
        return cmp(data1,data2)

    def parsePath(self, path, c_iter):

        def isDir(a): return os.path.isdir(a) and not os.path.islink(a)

        def scanPath(path,c_iter):
            if(path == ''): return False
            for infile in sorted(os.listdir(path)):
                file_path = os.path.join(path,infile)
                if(isDir(file_path)):
                    #print "current directory: "+ infile

                    new_dir_to_scan = self.ls.append(c_iter,( file_path, infile, 'folder', self.ilibrary.get_icon_pixbuf(file_path) ))
                    scanPath(file_path,new_dir_to_scan)
                else:
                    # print "current file is: " + infile + " -> " +self.ilibrary.get_icon_pixbuf(file_path)

                    self.ls.append(c_iter, ( file_path, infile ,'file', self.ilibrary.get_icon_pixbuf(file_path)))

        scanPath(path, c_iter)
        return self.ls

    def cellrenderer(self, treeviewcolumn, ctr, treemodel, it):
        name = treemodel.get_value(it, 1)
        ctr.set_property("text", name)

    def pixbufrenderer(self, column, crp, treemodel, it):
        icon = treemodel.get_value(it, 3)
        #print "PixbufRenderer> "+icon
        crp.set_property("pixbuf",icon)

