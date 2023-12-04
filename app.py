# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import re
import sgtk
import nuke
import pathlib


class NukeOCIO(sgtk.platform.Application):
    """
    The app entry point. This class is responsible for initializing and tearing down
    the application, handle menu registration etc.
    """

    def init_app(self):
        """
        Called as the application is being initialized
        """

        # this app should not do anything if nuke is run without gui.

        if nuke.env['gui']:

            self._ctx = self.context
            self._set_ocio_settings_on_root()

        else:
            pass

    def _set_ocio_settings_on_root(self):

        ocio = self._get_ocio_file()

        nuke.knobDefault('Root.colorManagement', 'OCIO')
        nuke.knobDefault('Root.OCIO_config', 'custom')
        nuke.knobDefault('Root.customOCIOConfigPath', ocio)

    def _get_ocio_file(self):

        context_locations = self._ctx.filesystem_locations

        if context_locations:
            match = re.search(r'^.*(projects).(\w*)', context_locations[0])
        else:
            return None

        if match is not None:
            projects_location = match.group(0)
            colour_location = os.path.join(projects_location, 'colour')
        else:
            return None

        for file in os.listdir(colour_location):
            if file.endswith('.ocio'):
                ocio_path = os.path.join(colour_location, file)
                ocio_file_pure_path = pathlib.PureWindowsPath(ocio_path)
                ocio_file_location = str(ocio_file_pure_path.as_posix())

                return ocio_file_location

            else:
                return None


