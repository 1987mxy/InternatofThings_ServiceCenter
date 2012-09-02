import Global

from Log import Log
Global.Logger = Log.instance()

from DB.Database import Database
Global.DB = Database.instance()

from Package import Package
Global.Packager = Package.instance()