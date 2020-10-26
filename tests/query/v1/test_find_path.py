# --coding:utf-8--
#
# Copyright (c) 2020 vesoft inc. All rights reserved.
#
# This source code is licensed under Apache 2.0 License,
# attached with Common Clause Condition 1.0, found in the LICENSES directory.

import pytest

from tests.common.nebula_test_suite import NebulaTestSuite


@pytest.mark.usefixtures('set_vertices_and_edges')
class TestFindPath(NebulaTestSuite):
    @classmethod
    def prepare(self):
        self.use_nba()

    def test_single_pair_constant_input(self):
        stmt = 'FIND SHORTEST PATH FROM "Tim Duncan" TO "Tony Parker" OVER like'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tim Duncan", (b"like", 0, b"Tony Parker")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])

        stmt = 'FIND SHORTEST PATH FROM "Tim Duncan" TO "LaMarcus Aldridge" OVER like'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"LaMarcus Aldridge")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])

        stmt = 'FIND SHORTEST PATH FROM "Tiago Splitter" TO "LaMarcus Aldridge" OVER like'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tiago Splitter", (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker"), (b"like", 0, b"LaMarcus Aldridge")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])

        stmt = 'FIND SHORTEST PATH FROM "Tiago Splitter" TO "LaMarcus Aldridge" OVER like, teammate'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tiago Splitter", (b"like", 0, b"Tim Duncan"), (b"teammate", 0, b"LaMarcus Aldridge")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])

        stmt = 'FIND SHORTEST PATH FROM "Tiago Splitter" TO "LaMarcus Aldridge" OVER *'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tiago Splitter", (b"like", 0, b"Tim Duncan"), (b"teammate", 0, b"LaMarcus Aldridge")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])


    def test_all_pairs_all_paths_constant_input(self):
        stmt = 'FIND ALL PATH FROM "Tim Duncan" TO "Tony Parker" OVER like UPTO 3 STEPS'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tim Duncan", (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Manu Ginobili"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"LaMarcus Aldridge"), (b"like", 0, b"Tony Parker")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])

        stmt = 'FIND ALL PATH FROM "Tim Duncan" TO "Tony Parker","Manu Ginobili" OVER like UPTO 3 STEPS'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tim Duncan", (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Manu Ginobili")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"Manu Ginobili")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Manu Ginobili"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"LaMarcus Aldridge"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Manu Ginobili")],
                [b"Tim Duncan", (b"like", 0, b"Manu Ginobili"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Manu Ginobili")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])

        stmt = 'FIND ALL PATH FROM "Tim Duncan" TO "Tony Parker","LaMarcus Aldridge" OVER like UPTO 3 STEPS'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tim Duncan", (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"LaMarcus Aldridge")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Manu Ginobili"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"LaMarcus Aldridge"), (b"like", 0, b"Tony Parker")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])

        stmt = 'FIND ALL PATH FROM "Tim Duncan" TO "Tony Parker","Spurs" OVER like,serve UPTO 3 STEPS'
        resp = self.execute_query(stmt)
        self.check_resp_succeeded(resp)
        expected_data = {
            "column_names": ["_path"],
            "rows": [
                [b"Tim Duncan", (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"serve", 0, b"Spurs")],
                [b"Tim Duncan", (b"like", 0, b"Manu Ginobili"), (b"serve", 0, b"Spurs")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"serve", 0, b"Spurs")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Manu Ginobili"), (b"like", 0, b"Tim Duncan"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"Tim Duncan"), (b"serve", 0, b"Spurs")],
                [b"Tim Duncan", (b"like", 0, b"Manu Ginobili"), (b"like", 0, b"Tim Duncan"), (b"serve", 0, b"Spurs")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"LaMarcus Aldridge"), (b"like", 0, b"Tony Parker")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"LaMarcus Aldridge"), (b"serve", 0, b"Spurs")],
                [b"Tim Duncan", (b"like", 0, b"Tony Parker"), (b"like", 0, b"Manu Ginobili"), (b"serve", 0, b"Spurs")]
            ]
        }
        self.check_column_names(resp, expected_data["column_names"])
        self.check_path_result_without_prop(resp.data.rows, expected_data["rows"])
