from __future__ import absolute_import

import mock

from corehq.apps.userreports.expressions.factory import ExpressionFactory
from corehq.apps.userreports.specs import FactoryContext, EvaluationContext
from corehq.apps.userreports.expressions.factory import SubcasesExpressionSpec
from custom.enikshay.ucr.tests.util import TestDataSourceExpressions

EPISODE_DATA_SOURCE = 'episode_2b_v4.json'


class TestEpisode2B(TestDataSourceExpressions):

    data_source_name = EPISODE_DATA_SOURCE

    def _get_expression(self, column_id, column_type):
        column = self._get_column(column_id)
        self.assertEqual(column['datatype'], column_type)
        return ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

    def test_treating_phi_property_when_clause_true(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': None,
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('treating_phi')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertEqual(expression(episode_case, EvaluationContext(episode_case, 0)), 'owner-id')

    def test_key_populations(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': None,
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ],
            'key_populations': 'test test2 test3'
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self._get_column('key_populations')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertEqual(expression(episode_case, EvaluationContext(episode_case, 0)), 'test, test2, test3')

    def test_treating_phi_property_when_clause_treatment_initiation_date_is_null(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': None,
            'archive_reason': None,
            'treatment_outcome': None,
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('treating_phi')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertIsNone(expression(episode_case, EvaluationContext(episode_case, 0)))

    def test_treating_phi_property_when_clause_archive_reason_is_not_null(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': 'test',
            'treatment_outcome': None,
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('treating_phi')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertIsNone(expression(episode_case, EvaluationContext(episode_case, 0)))

    def test_treating_phi_property_when_clause_treatment_outcome_is_not_null(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('treating_phi')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertIsNone(expression(episode_case, EvaluationContext(episode_case, 0)))

    def test_tu_name_property_when_clause_true(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': None,
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'tu_name': 'test'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('tu_name')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertEqual(expression(episode_case, EvaluationContext(episode_case, 0)), 'test')

    def test_tu_name_property_when_clause_treatment_initiation_date_is_null(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': None,
            'archive_reason': None,
            'treatment_outcome': None,
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id',
            'tu_name': 'test'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('treating_phi')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertIsNone(expression(episode_case, EvaluationContext(episode_case, 0)))

    def test_tu_name_property_when_clause_archive_reason_is_not_null(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': 'test',
            'treatment_outcome': None,
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id',
            'tu_name': 'test'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('treating_phi')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertIsNone(expression(episode_case, EvaluationContext(episode_case, 0)))

    def test_tu_name_property_when_clause_treatment_outcome_is_not_null(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id',
            'tu_name': 'test'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('treating_phi')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertIsNone(expression(episode_case, EvaluationContext(episode_case, 0)))

    def test_microbiological_properties(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_ip',
                'test_requested_date': '2017-09-28',
                'test_type_value': 'microscopy-zn',
                'result_recorded': 'yes'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'test_type_value': 'microscopy-zn',
                'result_recorded': 'yes'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'test_type_value': 'microscopy-zn',
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self.get_column('endofip_test_requested_date')
        self.assertEqual(column['datatype'], 'date')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        column2 = self.get_column('endofcp_test_requested_date')
        self.assertEqual(column2['datatype'], 'date')
        expression2 = ExpressionFactory.from_spec(
            column2['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(expression(episode_case, EvaluationContext(episode_case, 0)), '2017-09-28')
            self.assertEqual(expression2(episode_case, EvaluationContext(episode_case, 0)), '2017-09-28')

    def test_microbiological_properties_when_clause_is_false(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_ip',
                'test_requested_date': '2017-09-28',
                'test_type_value': 'not-microscopy'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'test_type_value': 'not-microscopy',
                'result_recorded': 'yes'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'test_type_value': 'microscopy-zn',
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        endofip_test_requested_date = self.get_column('endofip_test_requested_date')
        self.assertEqual(endofip_test_requested_date['datatype'], 'date')
        endofip_test_requested_date_expression = ExpressionFactory.from_spec(
            endofip_test_requested_date['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        endofcp_test_requested_date = self.get_column('endofcp_test_requested_date')
        self.assertEqual(endofcp_test_requested_date['datatype'], 'date')
        endofcp_test_requested_date_expression = ExpressionFactory.from_spec(
            endofcp_test_requested_date['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertIsNone(
                endofip_test_requested_date_expression(episode_case, EvaluationContext(episode_case, 0))
            )
            self.assertIsNone(
                endofcp_test_requested_date_expression(episode_case, EvaluationContext(episode_case, 0))
            )

    def test_microbiological_endofip_test_requested_date(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'test_type_value': 'microscopy-zn',
                'result_recorded': 'yes'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'yes',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'test_type_value': 'microscopy-zn',
                'result_recorded': 'yes'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'test_type_value': 'microscopy-zn',
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        endofip_test_requested_date = self.get_column('endofip_test_requested_date')
        self.assertEqual(endofip_test_requested_date['datatype'], 'date')
        endofip_test_requested_date_expression = ExpressionFactory.from_spec(
            endofip_test_requested_date['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        endofcp_test_requested_date = self.get_column('endofcp_test_requested_date')
        self.assertEqual(endofcp_test_requested_date['datatype'], 'date')
        endofcp_test_requested_date_expression = ExpressionFactory.from_spec(
            endofcp_test_requested_date['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                endofip_test_requested_date_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-09-28'
            )
            self.assertEqual(
                endofcp_test_requested_date_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-08-10'
            )

    def test_microbiological_endofip_result_smear(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'test_type_value': 'microscopy-zn',
                'result': 'result',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'yes',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'test_type_value': 'microscopy-zn',
                'result': 'result',
                'result_recorded': 'yes',
                'result_summary_display': 'result'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'test_type_value': 'microscopy-zn',
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        endofip_result = self.get_column('endofip_result')
        self.assertEqual(endofip_result['datatype'], 'string')
        endofip_result_expression = ExpressionFactory.from_spec(
            endofip_result['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        endofcp_result = self.get_column('endofcp_result')
        self.assertEqual(endofcp_result['datatype'], 'string')
        endofcp_result_expression = ExpressionFactory.from_spec(
            endofcp_result['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                endofip_result_expression(episode_case, EvaluationContext(episode_case, 0)),
                'result'
            )
            self.assertEqual(
                endofcp_result_expression(episode_case, EvaluationContext(episode_case, 0)),
                'result'
            )

    def test_not_microbiological_result(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-10',
                'test_type_value': 'cytopathology',
                'test_type_label': 'Cytopathology',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result_cytopathology',
                'result': 'result_cytopathology',
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'yes',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-09-10',
                'date_reported': '2017-09-10',
                'test_type_value': 'igra',
                'result': 'result',
                'result_recorded': 'yes',
                'result_summary_display': 'result_igra'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'rft_dstb_followup': 'end_of_cp',
                'test_requested_date': '2017-10-10',
                'date_reported': '2017-10-10',
                'test_type_value': 'other_clinical',
                'test_type_label': 'Other clinical',
                'result_summary_display': 'result_other_clinical'
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        not_microbiological = self._get_column('not_microbiological_result')
        self.assertEqual(not_microbiological['datatype'], 'string')
        not_microbiological_result_expression = ExpressionFactory.from_spec(
            not_microbiological['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                not_microbiological_result_expression(episode_case, EvaluationContext(episode_case, 0)),
                'Cytopathology, result_cytopathology'
            )

    def test_microscopy_expressions(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-10',
                'test_type_value': 'microscopy-zn',
                'test_type_label': 'Microscopy ZN',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result microscopy',
                'lab_serial_number': '1'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-12',
                'test_type_value': 'microscopy-zn',
                'test_type_label': 'Microscopy ZN',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result microscopy',
                'lab_serial_number': '2'
            },
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        date_reported_expression = self._get_expression('microscopy_test_result_date', 'date')
        testing_facility_name_expression = self._get_expression('microscopy_test_testing_facility_name', 'string')
        lab_serial_number_expression = self._get_expression('microscopy_test_lab_serial_number', 'string')
        result_summary_display_expression = self._get_expression(
            'microscopy_test_result_summary_display',
            'string'
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                date_reported_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-08-12'
            )
            self.assertEqual(
                testing_facility_name_expression(episode_case, EvaluationContext(episode_case, 0)),
                'Test Facility'
            )
            self.assertEqual(
                lab_serial_number_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2'
            )
            self.assertEqual(
                result_summary_display_expression(episode_case, EvaluationContext(episode_case, 0)),
                'tb_detected, result_grade'
            )

    def test_microscopy_tb_not_detected_expressions(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-10',
                'test_type_value': 'microscopy-zn',
                'test_type_label': 'Microscopy ZN',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result microscopy',
                'lab_serial_number': '1'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-12',
                'test_type_value': 'microscopy-zn',
                'test_type_label': 'Microscopy ZN',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result microscopy',
                'lab_serial_number': '2'
            },
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        date_reported_expression = self._get_expression('microscopy_test_result_date', 'date')
        testing_facility_name_expression = self._get_expression('microscopy_test_testing_facility_name', 'string')
        lab_serial_number_expression = self._get_expression('microscopy_test_lab_serial_number', 'string')
        result_summary_display_expression = self._get_expression(
            'microscopy_test_result_summary_display',
            'string'
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                date_reported_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-08-10'
            )
            self.assertEqual(
                testing_facility_name_expression(episode_case, EvaluationContext(episode_case, 0)),
                'Test Facility'
            )
            self.assertEqual(
                lab_serial_number_expression(episode_case, EvaluationContext(episode_case, 0)),
                '1'
            )
            self.assertEqual(
                result_summary_display_expression(episode_case, EvaluationContext(episode_case, 0)),
                'tb_not_detected'
            )

    def test_cbnaat_expressions(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-10',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '1'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-12',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '2'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-13',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '3',
                'drug_resistance_list': 'r cfx'
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        date_reported_expression = self._get_expression('cbnaat_test_result_date', 'date')
        testing_facility_name_expression = self._get_expression('cbnaat_test_testing_facility_name', 'string')
        lab_serial_number_expression = self._get_expression('cbnaat_test_lab_serial_number', 'string')
        result_summary_display_expression = self._get_expression(
            'cbnaat_test_result_summary_display',
            'string'
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                date_reported_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-08-12'
            )
            self.assertEqual(
                testing_facility_name_expression(episode_case, EvaluationContext(episode_case, 0)),
                'Test Facility'
            )
            self.assertEqual(
                lab_serial_number_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2'
            )
            self.assertEqual(
                result_summary_display_expression(episode_case, EvaluationContext(episode_case, 0)),
                'TB Detected, R: Indeterminate'
            )

    def test_cbnaat_rr_not_confirmed_drtb_expressions(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-10',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '1'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-13',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '2',
                'drug_resistance_list': 'r cfx'
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        date_reported_expression = self._get_expression('cbnaat_test_result_date', 'date')
        testing_facility_name_expression = self._get_expression('cbnaat_test_testing_facility_name', 'string')
        lab_serial_number_expression = self._get_expression('cbnaat_test_lab_serial_number', 'string')
        result_summary_display_expression = self._get_expression(
            'cbnaat_test_result_summary_display',
            'string'
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                date_reported_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-08-13'
            )
            self.assertEqual(
                testing_facility_name_expression(episode_case, EvaluationContext(episode_case, 0)),
                'Test Facility'
            )
            self.assertEqual(
                lab_serial_number_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2'
            )
            self.assertEqual(
                result_summary_display_expression(episode_case, EvaluationContext(episode_case, 0)),
                'TB Detected, R: Res'
            )

    def test_cbnaat_rr_expressions(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'episode_type': 'confirmed_drtb',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-10',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '1'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-12',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '2'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-13',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '3',
                'drug_resistance_list': 'r cfx'
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        date_reported_expression = self._get_expression('cbnaat_test_result_date', 'date')
        testing_facility_name_expression = self._get_expression('cbnaat_test_testing_facility_name', 'string')
        lab_serial_number_expression = self._get_expression('cbnaat_test_lab_serial_number', 'string')
        result_summary_display_expression = self._get_expression(
            'cbnaat_test_result_summary_display',
            'string'
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                date_reported_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-08-13'
            )
            self.assertEqual(
                testing_facility_name_expression(episode_case, EvaluationContext(episode_case, 0)),
                'Test Facility'
            )
            self.assertEqual(
                lab_serial_number_expression(episode_case, EvaluationContext(episode_case, 0)),
                '3'
            )
            self.assertEqual(
                result_summary_display_expression(episode_case, EvaluationContext(episode_case, 0)),
                'TB Detected, R: Res'
            )

    def test_cbnaat_rr_sensitive_expressions(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'episode_type': 'confirmed_drtb',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-10',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '1'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-12',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '2',
                'drug_sensitive_list': 'r cfx'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-13',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '3'
            }
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        date_reported_expression = self._get_expression('cbnaat_test_result_date', 'date')
        testing_facility_name_expression = self._get_expression('cbnaat_test_testing_facility_name', 'string')
        lab_serial_number_expression = self._get_expression('cbnaat_test_lab_serial_number', 'string')
        result_summary_display_expression = self._get_expression(
            'cbnaat_test_result_summary_display',
            'string'
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                date_reported_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-08-12'
            )
            self.assertEqual(
                testing_facility_name_expression(episode_case, EvaluationContext(episode_case, 0)),
                'Test Facility'
            )
            self.assertEqual(
                lab_serial_number_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2'
            )
            self.assertEqual(
                result_summary_display_expression(episode_case, EvaluationContext(episode_case, 0)),
                'TB Detected, R: Sens'
            )

    def test_cbnaat_tb_not_detected_expressions(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        subcases = [
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-10',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '1'
            },
            {
                'domain': 'enikshay-test',
                'type': 'test',
                'is_direct_test_entry': 'no',
                'rft_dstb_followup': 'end_of_ip',
                'rft_general': 'diagnosis_dstb',
                'test_requested_date': '2017-09-28',
                'date_tested': '2017-08-10',
                'date_reported': '2017-08-12',
                'test_type_value': 'cbnaat',
                'test_type_label': 'CBNAAT',
                'testing_facility_name': 'Test Facility',
                'result': 'tb_not_detected',
                'result_grade': 'result_grade',
                'result_recorded': 'yes',
                'result_summary_display': 'result cbnaat',
                'lab_serial_number': '2'
            },
        ]

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        date_reported_expression = self._get_expression('cbnaat_test_result_date', 'date')
        testing_facility_name_expression = self._get_expression('cbnaat_test_testing_facility_name', 'string')
        lab_serial_number_expression = self._get_expression('cbnaat_test_lab_serial_number', 'string')
        result_summary_display_expression = self._get_expression(
            'cbnaat_test_result_summary_display',
            'string'
        )

        with mock.patch.object(SubcasesExpressionSpec, '__call__', lambda *args: subcases):
            self.assertEqual(
                date_reported_expression(episode_case, EvaluationContext(episode_case, 0)),
                '2017-08-10'
            )
            self.assertEqual(
                testing_facility_name_expression(episode_case, EvaluationContext(episode_case, 0)),
                'Test Facility'
            )
            self.assertEqual(
                lab_serial_number_expression(episode_case, EvaluationContext(episode_case, 0)),
                '1'
            )
            self.assertEqual(
                result_summary_display_expression(episode_case, EvaluationContext(episode_case, 0)),
                'TB Not Detected'
            )

    def test_disease_classification_pulmonary(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'disease_classification': 'pulmonary',
            'site_choice': 'Other',
            'site_detail': 'test detail',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self._get_column('disease_classification')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertEqual(expression(episode_case, EvaluationContext(episode_case, 0)), 'Pulmonary')

    def test_disease_classification_extra_pulmonary_site_choice_not_other(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'disease_classification': 'extra_pulmonary',
            'site_choice': 'test',
            'site_detail': 'test detail',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self._get_column('disease_classification')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertEqual(expression(episode_case, EvaluationContext(episode_case, 0)), 'Extra Pulmonary, test')

    def test_disease_classification_extra_pulmonary_site_choice_other(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'treatment_initiation_date': '2017-09-28',
            'archive_reason': None,
            'treatment_outcome': 'test',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        occurrence_case = {
            '_id': 'occurrence_case_id',
            'domain': 'enikshay-test',
            'disease_classification': 'extra_pulmonary',
            'site_choice': 'other',
            'site_detail': 'test detail',
            'indices': [
                {'referenced_id': 'person_case_id'}
            ]
        }

        person_case = {
            '_id': 'person_case_id',
            'domain': 'enikshay-test',
            'owner_id': 'owner-id'
        }

        self.database.mock_docs = {
            'episode_case_id': episode_case,
            'occurrence_case_id': occurrence_case,
            'person_case_id': person_case
        }

        column = self._get_column('disease_classification')
        self.assertEqual(column['datatype'], 'string')
        expression = ExpressionFactory.from_spec(
            column['expression'],
            context=FactoryContext(self.named_expressions, {})
        )

        self.assertEqual(
            expression(episode_case, EvaluationContext(episode_case, 0)),
            'Extra Pulmonary, Other, test detail'
        )

    def test_type_of_regimen_confirmed_drtb(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'episode_type': 'confirmed_drtb',
            'treatment_regimen': 'test_regimen',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        expression = self._get_expression('type_of_regimen', 'string')
        self.assertEqual(
            expression(episode_case, EvaluationContext(episode_case, 0)),
            'test_regimen'
        )

    def test_type_of_regimen_confirmed_tb_new(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'episode_type': 'confirmed_tb',
            'treatment_initiated': 'yes_phi',
            'patient_type_choice': 'new',
            'treatment_regimen': 'test_regimen',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        expression = self._get_expression('type_of_regimen', 'string')
        self.assertEqual(
            expression(episode_case, EvaluationContext(episode_case, 0)),
            'New'
        )

    def test_type_of_regimen_confirmed_tb_outside_rntcp(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'episode_type': 'confirmed_tb',
            'treatment_initiated': 'yes_private',
            'treatment_status': 'yes_private',
            'patient_type_choice': 'recurrent',
            'treatment_regimen': 'test_regimen',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        expression = self._get_expression('type_of_regimen', 'string')
        self.assertEqual(
            expression(episode_case, EvaluationContext(episode_case, 0)),
            'Outside RNTCP'
        )

    def test_type_of_regimen_confirmed_tb_previously_treated(self):
        episode_case = {
            '_id': 'episode_case_id',
            'domain': 'enikshay-test',
            'episode_type': 'confirmed_tb',
            'treatment_initiated': 'yes_private',
            'treatment_status': 'yes_phi',
            'patient_type_choice': 'recurrent',
            'treatment_regimen': 'test_regimen',
            'indices': [
                {'referenced_id': 'occurrence_case_id'}
            ]
        }

        expression = self._get_expression('type_of_regimen', 'string')
        self.assertEqual(
            expression(episode_case, EvaluationContext(episode_case, 0)),
            'Previously Treated'
        )
