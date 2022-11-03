Release Notes
=============

2.0.0
----------
* New: Support for Django 3.2 and 4.0
* Dropped Django <3.2 support.
* New: Support for Python 3.9 and 3.10.
* Moved CI to GitHub Actions.
* Dropped support for Python 3.5 and 3.6.
* Add detection for Chromium-based Edge browser
* Rename OS X to macOS
* Add detection for newere macOS versions

1.7.0
-----
* new: Support for Django 2.2+.
* Dropped Django <2.2 support.

1.6.0
-----
* New: Support for Django 2.0.
* Dropped Django <1.11 support.
* Command for migrating existing sessions to the new session store (#33).

1.5.3
-----
* Fixed issue with incorrect location being displayed.

1.5.2
-----
* Also work with GeoIP2 country database.

1.5.1
-----
* Updated documentation for GeoIP2 library.
* Correctly detect macOS version on Firefox.

1.5.0
-----
* Added Django 1.11 support.
* Added support for GeoIP2 library.
* Added detection of Windows 10 and macOS from user-agent.
* Fixed #73 -- Error when deleting individual session from list view.
* Fixed #74 -- user agent not being shown in list view.
* Resolved Django’s deprecation warnings (preliminary Django 2.0 support).
* Make templatetags return None instead of 'unknown', provide your own fallback
  value with `default_if_none:`.
* Allow translation of fallback values.

1.4.0
-----
* Added Django Channels support.
* Fixed #62 -- Provide request.user in signals.
* Ending current session will logout instead, make sure LOGOUT_REDIRECT_URL is
  set.

1.3.1
-----
* Added Django 1.10 support.

1.3.0
-----
* Added Django 1.9 support.
* Dropped support for Django 1.7 and below.

1.2.0
-----
* New feature: delete all-but-current sessions.
* Added clearsessions command.

1.1.1
-----
* Added Django 1.8 support.

1.1.0
-----
* Fixed #14 -- Truncate long user agents strings.
* Fixed #23 -- Cannot use admin view search.
* Added Django 1.7 migrations.

1.0.0
-----
* #8 -- Consistent URL patterns.
* #11 -- Support Django 1.6's `ATOMIC_REQUESTS`.
* German translation added.

0.1.4
-----
* Python 3.4 support.
* Django 1.7 (beta) support.
* Italian translation added.
* Chinese translation added.
* Arabic translation updated.

0.1.3
-----
* Documentation.
* Hebrew translation added.
* Arabic translation added.
* Fixed #3 -- Reset `user_id` on logout.
* Fixed #4 -- Add explicit license text.

0.1.2
-----
* Ship with default templates.
* Added Dutch translation.

0.1.1
-----
* Added South migrations.

0.1.0
-----
* Initial release.
