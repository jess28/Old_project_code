# unittest of sqlall functionality
# Copyright (C) 2014 Jessica Strein jessica.strein@uconn.edu
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import unittest
import sqlall

class SqlAllTestCase(unittest.TestCase):
    """Tests for sqlall.py"""

    def test_key_dict(self):
        """Does the function find all keys with no repeats?"""
        dic = {'ID': '', 'Name': '', 'Alias': '', 'Ontology_term': ''}
        keys = ['ID', 'Name', 'Alias', 'Ontology_term']
        self.assertEqual(sqlall.key_dict('test_int.bed'), (dic, keys))

    def test_find_winID(self):
        """Does the function find the correct window number for each entry?"""
        self.assertEqual(sqlall.find_winID(24, 100), 0)

    def test_dict_fill(self):
        """Does the funtion return the correct tuples?"""
        dic = {'ID': '', 'Name': '', 'Alias': '', 'Ontology_term': ''}
        keys = ['ID', 'Name', 'Alias', 'Ontology_term']
        tup = [('123', 'Jose', 'J', 'NA', '2', '30', 'Database', 'gene', '0', 'A'),
               ('456', 'Ben', 'B', 'NA', '150', '170', 'Database', 'match', '1', 'A'),
               ('4567', 'Ben', 'B,Q', 'SO:00000663,GO:0000054', '120', '175', 'Database', 'gene', '1', 'A'),
               ('crazy', 'Woohoo', 'excitement', 'NA', '20', '50', 'Flybase', 'mRNA', '0', 'B'),
               ('00056', 'May-hem', 'madness', 'GO:0005739', '105', '160', 'Flybase', 'gene', '1', 'B')]
        self.assertEqual(sqlall.dict_fill(dic, keys, 'test_int.bed'), tup)

if __name__ == '__main__':
    unittest.main()