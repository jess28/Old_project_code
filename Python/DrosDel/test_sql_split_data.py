# tests the sql_split_data script for correct funtionality
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
import sql_split_data

class SqlSplitDataTest(unittest.TestCase):
    """Tests for sql_split_data"""

    def test_import_data(self):
        """Does the function collect the appropriate data with necessary 'NA's?"""
        self.assertEqual(sql_split_data.import_data())