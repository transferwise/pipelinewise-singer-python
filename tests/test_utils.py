import unittest
from datetime import datetime as dt
import pytz
import logging
import singer.utils as u


class TestFormat(unittest.TestCase):
    def test_small_years(self):
        self.assertEqual(u.strftime(dt(90, 1, 1, tzinfo=pytz.UTC)),
                         '0090-01-01T00:00:00.000000Z')

    def test_round_trip(self):
        now = dt.utcnow().replace(tzinfo=pytz.UTC)
        dtime = u.strftime(now)
        pdtime = u.strptime_to_utc(dtime)
        fdtime = u.strftime(pdtime)
        self.assertEqual(dtime, fdtime)


    def test_parse_naive_datetime(self):
        """Test that a naive datetime string is assigned UTC."""
        dt_string = "2026-04-17 09:00:00"
        result = u.strptime_with_tz(dt_string)
        self.assertIsNotNone(result.tzinfo)
        self.assertEqual(result.tzinfo, pytz.UTC)
        self.assertEqual(result.year, 2026)
        self.assertEqual(result.hour, 9)

    def test_parse_aware_datetime(self):
        """Test that an existing timezone is preserved (not overwritten by UTC)."""
        # Using an offset of +02:00
        dt_string = "2026-04-17 09:00:00+02:00"
        result = u.strptime_with_tz(dt_string)

        self.assertIsNotNone(result.tzinfo)
        # The offset should be 120 minutes (2 hours)
        self.assertEqual(result.utcoffset().total_seconds(), 7200)
        self.assertNotEqual(result.tzinfo, pytz.UTC)

    def test_parse_iso_format(self):
        """Test that standard ISO formats work correctly."""
        dt_string = "2026-04-17T12:30:45Z"
        result = u.strptime_with_tz(dt_string)

        self.assertEqual(result.hour, 12)
        # 'Z' is UTC
        self.assertEqual(result.tzinfo.utcoffset(result).total_seconds(), 0)

    def test_invalid_string_raises_error(self):
        """Test that completely invalid strings still raise parser errors."""
        with self.assertRaises(Exception):
            u.strptime_with_tz("not-a-date")

class TestHandleException(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)

    def test_successful_fn(self):
        @u.handle_top_exception(self.logger)
        def foo():
            return 3
        self.assertEqual(foo(), 3)

    def test_exception_fn(self):
        @u.handle_top_exception(self.logger)
        def foo():
            raise RuntimeError('foo')
        self.assertRaises(RuntimeError, foo)
