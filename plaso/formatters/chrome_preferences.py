# -*- coding: utf-8 -*-
"""The Google Chrome Preferences file event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class ChromeContentSettingsExceptionsFormatter(
    interface.ConditionalEventFormatter):
  """Formatter for a Chrome content_settings exceptions event."""

  DATA_TYPE = 'chrome:preferences:content_settings:exceptions'

  FORMAT_STRING_PIECES = [
      'Permission {permission}',
      'used by {primary_url}',
      'embedded in {secondary_url}']

  FORMAT_STRING_SHORT_PIECES = [
      'Permission {permission}',
      'used by {primary_url}',
      'embedded in {secondary_url}']

  def FormatEventValues(self, event_values):
    """Formats event values using the helpers.

    Args:
      event_values (dict[str, object]): event values.
    """
    # There is apparently a bug, either in GURL.cc or
    # content_settings_pattern.cc where URLs with file:// scheme are stored in
    # the URL as an empty string, which is later detected as being Invalid, and
    # Chrome produces the following example logs:
    # content_settings_pref.cc(469)] Invalid pattern strings: https://a.com:443,
    # content_settings_pref.cc(295)] Invalid pattern strings: ,
    # content_settings_pref.cc(295)] Invalid pattern strings: ,*
    # More research needed, could be related to https://crbug.com/132659

    primary_url = event_values.get('primary_url', None)
    if primary_url == '':
      primary_url = 'local file'

    secondary_url = event_values.get('secondary_url', None)
    if secondary_url == '':
      secondary_url = 'local file'

    if secondary_url in (primary_url, '*'):
      secondary_url = None

    event_values['primary_url'] = primary_url
    event_values['secondary_url'] = secondary_url


manager.FormattersManager.RegisterFormatter(
    ChromeContentSettingsExceptionsFormatter)
