
# ******************************************************
# * Copyright © 2016-2023 - Jordan Irwin (AntumDeluge) *
# ******************************************************
# * This software is licensed under the MIT license.   *
# * See: LICENSE.txt for details.                      *
# ******************************************************

## @module dbr.language

import gettext
import locale
import os

from libdbr.logger import Logger
from libdebreate   import appinfo


__logger = Logger(__name__)

__domain = appinfo.getName().lower()
__translator = None
__native_code = "en_US"


## Formats translatable strings.
#
#  @param str_value
#    \b \e str : String to be translated.
#  @fixme
#    Use `str` function as default translator.
def GT(str_value):
  if not __translator:
    return str_value
  return __translator(str_value)


## Retrieves the path of gettext locale translations.
#
#  @deprecated
#    Use `libdebreate.appinfo.getLocaleDir`.
def GetLocaleDir():
  __logger.deprecated(GetLocaleDir, alt=appinfo.getLocaleDir)

  return appinfo.getLocaleDir()


## Sets locale translator.
#
#  @param path
#    Directory to search for gettext locale translations.
def setTranslator(path):
  global __translator
  l_code = locale.getlocale()[0]
  __logger.debug("locale code: {}".format(l_code))
  __logger.debug("locale directory: {}".format(path))
  if l_code != __native_code:
    try:
      __translator = gettext.translation(__domain, path).gettext
    except FileNotFoundError:
      __logger.warn("translation for locale '{}' unavailable".format(l_code))
