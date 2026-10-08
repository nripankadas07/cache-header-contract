import unittest
from cache_header_contract import check, parse

class ContractTests(unittest.TestCase):
    def test_good(self):
        self.assertTrue(check([["Cache-Control","public,max-age=20"],["Vary","Accept-Encoding"]],{"require":["public"],"max_shared_ttl":30,"vary":["accept-encoding"]})["ok"])
    def test_repeated_field(self):
        self.assertFalse(check([["Cache-Control","max-age=20"],["Cache-Control","max-age=30"]],{})["ok"])
    def test_shared_precedence(self):
        r=check([["Cache-Control","max-age=300,s-maxage=20"]],{"max_shared_ttl":20})
        self.assertTrue(r["ok"]);self.assertEqual(r["shared_ttl"],20)
    def test_zero_ttl(self):
        self.assertTrue(check([["Cache-Control","max-age=0"]],{"max_shared_ttl":0})["ok"])
    def test_missing_ttl(self):
        self.assertFalse(check([], {"max_shared_ttl":10})["ok"])
    def test_quoted_comma(self):
        self.assertEqual(parse('private="a,b",max-age="20"')[0]["private"],"a,b")
    def test_bad_numeric(self):
        for text in ["max-age=-1","max-age=1.2","max-age","max-age=9999999999999"]:
            with self.assertRaises(ValueError):parse(text)
    def test_unterminated(self):
        with self.assertRaises(ValueError):parse('private="a,b')
    def test_no_cache_not_no_store(self):
        r=check([["Cache-Control","no-cache"]],{"require":["no-store"]})
        self.assertFalse(r["ok"])
    def test_crlf(self):
        with self.assertRaises(ValueError):check([["Cache-Control","public\r\nX: yes"]],{})

if __name__=="__main__":unittest.main()
