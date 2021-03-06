#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tools/development/cx_freeze.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os
import site
import sys

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from king_phisher import version

import matplotlib
import pytz
import requests
from mpl_toolkits import basemap
from cx_Freeze import setup, Executable

is_debugging_build = bool(os.environ.get('DEBUG'))

include_dll_path = os.path.join(site.getsitepackages()[1], 'gnome')

# DLLs from site-packages\gnome\ last updated for pygi-aio 3.14.0 rev22
missing_dlls = [
	'lib\enchant\libenchant_aspell.dll',
	'lib\enchant\libenchant_hspell.dll',
	'lib\enchant\libenchant_ispell.dll',
	'lib\enchant\libenchant_myspell.dll',
	'lib\enchant\libenchant_voikko.dll',
	'lib\gio\modules\libgiognomeproxy.dll',
	'lib\gio\modules\libgiognutls.dll',
	'lib\gio\modules\libgiolibproxy.dll',
	'lib\gio\modules\libgsettingsgconfbackend.dll',
	'libaspell-15.dll',
	'libatk-1.0-0.dll',
	'libcairo-gobject-2.dll',
	'libdbus-1-3.dll',
	'libdbus-glib-1-2.dll',
	'libenchant-1.dll',
	'libffi-6.dll',
	'libfontconfig-1.dll',
	'libfreetype-6.dll',
	'libgailutil-3-0.dll',
	'libgconf-2-4.dll',
	'libgdk-3-0.dll',
	'libgdk_pixbuf-2.0-0.dll',
	'libgee-0.8-2.dll',
	'libgeoclue-0.dll',
	'libgio-2.0-0.dll',
	'libgirepository-1.0-1.dll',
	'libglib-2.0-0.dll',
	'libgmodule-2.0-0.dll',
	'libgnutls-26.dll',
	'libgobject-2.0-0.dll',
	'libgstallocators-1.0-0.dll',
	'libgstapp-1.0-0.dll',
	'libgstaudio-1.0-0.dll',
	'libgstbase-1.0-0.dll',
	'libgstcheck-1.0-0.dll',
	'libgstcontroller-1.0-0.dll',
	'libgstfft-1.0-0.dll',
	'libgstnet-1.0-0.dll',
	'libgstpbutils-1.0-0.dll',
	'libgstreamer-1.0-0.dll',
	'libgstriff-1.0-0.dll',
	'libgstrtp-1.0-0.dll',
	'libgstrtsp-1.0-0.dll',
	'libgstrtspserver-1.0-0.dll',
	'libgstsdp-1.0-0.dll',
	'libgsttag-1.0-0.dll',
	'libgstvalidate-1.0-0.dll',
	'libgstvalidate-default-overrides-1.0-0.dll',
	'libgstvideo-1.0-0.dll',
	'libgthread-2.0-0.dll',
	'libgtk-3-0.dll',
	'libgtksourceview-3.0-1.dll',
	'libgtkspell3-3-0.dll',
	'libgxml-0.4-4.dll',
	'libharfbuzz-0.dll',
	'libharfbuzz-gobject-0.dll',
	'libintl-8.dll',
	'libjack.dll',
	'libjasper-1.dll',
	'libjavascriptcoregtk-3.0-0.dll',
	'libjpeg-8.dll',
	'liborc-0.4-0.dll',
	'liborc-test-0.4-0.dll',
	'libp11-kit-0.dll',
	'libpango-1.0-0.dll',
	'libpangocairo-1.0-0.dll',
	'libpangoft2-1.0-0.dll',
	'libpangowin32-1.0-0.dll',
	'libpng16-16.dll',
	'libproxy.dll',
	'librsvg-2-2.dll',
	'libsoup-2.4-1.dll',
	'libsqlite3-0.dll',
	'libtiff-5.dll',
	'libvisual-0.4-0.dll',
	'libwebkitgtk-3.0-0.dll',
	'libwebp-5.dll',
	'libwinpthread-1.dll',
	'libxmlxpat.dll',
	'libxslt-1.dll',
	'libzzz.dll',
]

include_files = []
for dll in missing_dlls:
	include_files.append((os.path.join(include_dll_path, dll), dll))

gtk_libs = ['etc', 'lib', 'share']
for lib in gtk_libs:
	include_files.append((os.path.join(include_dll_path, lib), lib))

# include all site-packages and eggs for pkg_resources to function correctly
for path in os.listdir(site.getsitepackages()[1]):
	if os.path.isdir(os.path.join(site.getsitepackages()[1], path)):
		include_files.append((os.path.join(site.getsitepackages()[1], path), path))

# include windows complied version of geos for basemaps
include_files.append((os.path.join(site.getsitepackages()[1], 'geos.dll'), 'geos.dll'))
include_files.append((os.path.join(site.getsitepackages()[1], 'geos_c.dll'), 'geos_c.dll'))
include_files.append((os.path.join(site.getsitepackages()[1], '_geoslib.pyd'), '_geoslib.pyd'))
include_files.append((os.path.join(site.getsitepackages()[0], 'libs', 'geos_c.lib'), os.path.join('libs', 'geos_c.lib')))
include_files.append((os.path.join(site.getsitepackages()[0], 'libs', 'geos.lib'), os.path.join('libs', 'geos.lib')))


include_files.append((matplotlib.get_data_path(), 'mpl-data'))
include_files.append((basemap.basemap_datadir, 'mpl-basemap-data'))
include_files.append(('data/client/king_phisher', 'king_phisher'))
include_files.append(('data/king_phisher', 'king_phisher'))
include_files.append((pytz.__path__[0], 'pytz'))
include_files.append((requests.__path__[0], 'requests'))

exe_base = 'Win32GUI'
if is_debugging_build:
	exe_base = 'Console'

executables = [
	Executable(
		'KingPhisher',
		base=exe_base,
		icon='data/client/king_phisher/king-phisher-icon.ico',
		shortcutName='King Phisher',
		shortcutDir='ProgramMenuFolder'
	)
]

build_exe_options = dict(
	include_files=include_files,
	packages=[
		'_geoslib',
		'boltons',
		'cairo',
		'cffi',
		'collections',
		'cryptography',
		'dns',
		'email',
		'email_validator',
		'geoip2',
		'geojson',
		'gi',
		'graphene',
		'graphene_sqlalchemy',
		'icalendar',
		'idna',
		'ipaddress',
		'jinja2',
		'jsonschema',
		'king_phisher.client',
		'matplotlib',
		'mpl_toolkits',
		'msgpack',
		'numpy',
		'paramiko',
		'pil',
		'pkg_resources',
		'pluginbase',
		'qrcode',
		'reportlab',
		'requests',
		'smoke_zephyr',
		'tzlocal',
		'websocket',
		'win32api',
		'xlsxwriter',
		'yaml',
	],
	excludes=['jinja2.asyncfilters', 'jinja2.asyncsupport'], # not supported with python 3.4
)

setup(
	name='KingPhisher',
	author='SecureState',
	version=version.distutils_version,
	description='King Phisher Client',
	options=dict(build_exe=build_exe_options),
	executables=executables
)
