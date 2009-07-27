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

import os.path
import pygtk
import gtk
import gnomevfs


class GnomeFileIcons:
    def __init__( self ):
        self.all_icons = gtk.icon_theme_get_default().list_icons()
        self.cache = {}
        self.iconTheme = gtk.IconTheme()
        self.icon_theme_icons = gtk.icon_theme_get_default()
        self.piximage = gtk.Image()

    def getIcon( self, path ):
        if not os.path.exists(path):
            return gtk.STOCK_FILE

        #get mime type
        mime_type = gnomevfs.get_mime_type( path ).replace( '/', '-' )

        #search in the cache
        if mime_type in self.cache:
            return self.cache[mime_type]

        #try gnome mime
        items = mime_type.split('-')
        for aux in xrange(len(items)-1):
            icon_name = "gnome-mime-" + '-'.join(items[:len(items)-aux])
            if icon_name in self.all_icons:
                #print "icon: " + icon_name
                self.cache[mime_type] = icon_name
                return icon_name

        #try folder
        if os.path.isdir(path):
            icon_name = 'folder'
            if icon_name in self.all_icons:
                #print "icon: " + icon_name
                self.cache[mime_type] = icon_name
                return icon_name

            #print "icon: " + icon_name
            icon_name = gtk.STOCK_DIRECTORY
            self.cache[mime_type] = icon_name
            return icon_name

        #try simple mime
        for aux in xrange(len(items)-1):
            icon_name = '-'.join(items[:len(items)-aux])
            if icon_name in self.all_icons:
                #print "icon: " + icon_name
                self.cache[mime_type] = icon_name
                return icon_name

        #file icon
        icon_name = gtk.STOCK_FILE
        self.cache[mime_type] = icon_name
        return icon_name

    def getIconPixbuf(self, path):
        # if path is wrong
        if not os.path.exists(path):
            return self.icon_theme_icons.load_icon(gtk.STOCK_FILE,gtk.ICON_SIZE_MENU,0)


        #get mime type
        mime_type = gnomevfs.get_mime_type( path ).replace( '/', '-' )

        #search in the cache
        if mime_type in self.cache:
            return self.cache[mime_type]

        #try gnome mime
        items = mime_type.split('-')
        for aux in xrange(len(items)-1):
            icon_name = "gnome-mime-" + '-'.join(items[:len(items)-aux])
            if icon_name in self.all_icons:
#                print "icon: " + icon_name
                self.cache[mime_type] = self.icon_theme_icons.load_icon(icon_name,gtk.ICON_SIZE_MENU,0)

                return self.cache[mime_type]
        #try folder
        if os.path.isdir(path):
            icon_name = 'folder'
            self.cache[mime_type] = self.icon_theme_icons.load_icon(icon_name,gtk.ICON_SIZE_MENU,0)
            return self.cache[mime_type]

        #try simple mime
        for aux in xrange(len(items)-1):
            icon_name = '-'.join(items[:len(items)-aux])
            if icon_name in self.all_icons:
                #print "icon: " + icon_name
                self.cache[mime_type] = self.icon_theme_icons.load_icon(icon_name,gtk.ICON_SIZE_MENU,0)
                return self.cache[mime_type]

        #file icon
#        icon = gtk.Image()
#        icon.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        icon_name = gtk.STOCK_FILE
        self.cache[mime_type] = self.icon_theme_icons.load_icon(icon_name,gtk.ICON_SIZE_MENU,0)
        return self.cache[mime_type]

    def set_icon(self, path):
#        iconname, pxbuf = self.getIconPixbuf(path)

        #print iconname,": ", pxbuf
        return self.getIconPixbuf(path)

    def get_icon_pixbuf(self, path):
        return self.getIconPixbuf(path)


#import gnomefileicons
#
#fileicons = gnomefileicons.GnomeFileIcons()
#print fileicons.getIcon('/path/file.tar.gz')

