# (c) Copyright 2015 - 2016, XBRL US Inc. All rights reserved.
# See license.md for license information.
# See PatentNotice.md for patent infringement notice.
import unittest
from unittest import mock
from dqc_us_rules import util as util

import dqc_us_rules.dqc_us_0013 as dqc_us_0013


class TestDQC0013(unittest.TestCase):
    def setUp(self):
        """
        Sets up values for unit tests
        """
        m_qn_fire1 = mock.Mock(
            localName='EffectiveIncomeTaxRateReconciliationTaxCredits',
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31'
        )
        m_qn_fire2 = mock.Mock(
            localName=(
                'EffectiveIncomeTaxRateReconciliation'
                'NondeductibleExpenseLifeInsurance'
            ),
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31'
        )
        m_qn_precondition = mock.Mock(
            localName=(
                'IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic'
            ),
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31'
        )
        m_qn_no_blacklist = mock.Mock(
            localName='concept1',
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31'
        )
        mock_type = mock.Mock()
        mock_type.name = 'monetaryItemType'
        mock_concept1 = mock.Mock(qname=m_qn_fire1, type=mock_type)
        mock_concept2 = mock.Mock(qname=m_qn_fire2, type=mock_type)
        mock_precondition_concept = mock.Mock(
            qname=m_qn_precondition, type=mock_type
        )
        mock_concept_no_blacklist = mock.Mock(
            qname=m_qn_no_blacklist, type=mock_type
        )
        mock_no_dimensions = {}
        mock_context = mock.Mock(segDimValues=mock_no_dimensions)
        # Concept is in blacklist, type is numeric with decimal, value is
        # NEGATIVE = Fire
        self.fact_fire1 = mock.Mock(
            concept=mock_concept1, qname=m_qn_fire1, xValue=-.0010,
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Concept is in blacklist, type is numeric without decimal, value is
        # NEGATIVE = Fire
        self.fact_fire2 = mock.Mock(
            concept=mock_concept2, qname=m_qn_fire2, xValue=-10,
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Concept is in blacklist, type is numeric with decimal, value is
        # POSITIVE = No Fire
        self.fact_no_fire1 = mock.Mock(
            concept=mock_concept1, qname=m_qn_fire1, xValue=.1010,
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Concept is in blacklist, type is numeric without decimal, value is
        # POSITIVE = No Fire
        self.fact_no_fire2 = mock.Mock(
            concept=mock_concept2, qname=m_qn_fire2, xValue=100,
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Concept is NOT in blacklist, type is numeric without decimal, value
        # is NEGATIVE = No Fire
        self.fact_no_fire3 = mock.Mock(
            concept=mock_concept_no_blacklist, qname=m_qn_no_blacklist,
            xValue=-7777,
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Concept is NOT in blacklist, type is numeric without decimal, value
        # is POSITIVE = No Fire
        self.fact_no_fire4 = mock.Mock(
            concept=mock_concept_no_blacklist, qname=m_qn_no_blacklist,
            xValue=7777, namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Concept is in blacklist, type is numeric, value is ZERO = No Fire
        self.fact_no_fire5 = mock.Mock(
            concept=mock_concept1, qname=m_qn_fire1, xValue=0,
            namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Precondition fact that will cause the rule to fire (value is > 0)
        self.fact_precondition_positive = mock.Mock(
            concept=mock_precondition_concept, qname=m_qn_precondition,
            xValue=77, namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Precondition fact that will NOT cause the rule to fire (value is = 0)
        self.fact_precondition_zero = mock.Mock(
            concept=mock_precondition_concept, qname=m_qn_precondition,
            xValue=0, namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )
        # Precondition fact that will NOT cause the rule to fire (value is < 0)
        self.fact_precondition_negative = mock.Mock(
            concept=mock_precondition_concept, qname=m_qn_precondition,
            xValue=-77, namespaceURI='http://xbrl.sec.gov/us-gaap/2014-01-31',
            context=mock_context
        )

    def test_precondition_fact_exists(self):
        """
        Verifies that the check for whether a precondition concept exists
            returns
        the expected results
        """
        # Contains precondition element and the associated value is
        # positive = Fire
        fact_list1 = [
            self.fact_fire1, self.fact_fire2, self.fact_no_fire1,
            self.fact_no_fire2, self.fact_no_fire3, self.fact_no_fire4,
            self.fact_no_fire5, self.fact_precondition_positive
        ]
        # Contains precondition element and the associated value is
        # zero = No Fire
        fact_list2 = [
            self.fact_fire1, self.fact_fire2, self.fact_no_fire1,
            self.fact_no_fire2, self.fact_no_fire3, self.fact_no_fire4,
            self.fact_no_fire5, self.fact_precondition_zero
        ]
        # Contains precondition element and the associated value is
        # negative = No Fire
        fact_list3 = [
            self.fact_fire1, self.fact_fire2, self.fact_no_fire1,
            self.fact_no_fire2, self.fact_no_fire3, self.fact_no_fire4,
            self.fact_no_fire5, self.fact_precondition_negative
        ]
        # The precondition element does not exist = No Fire
        fact_list4 = [
            self.fact_fire1, self.fact_fire2, self.fact_no_fire1,
            self.fact_no_fire2, self.fact_no_fire3, self.fact_no_fire4,
            self.fact_no_fire5
        ]

        result1 = util.facts.precondition_fact_exists(
            fact_list1,
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic'
        )
        self.assertEqual(True, result1[0])
        self.assertEqual(77, result1[1])
        result2 = util.facts.precondition_fact_exists(
            fact_list2,
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic'
        )
        self.assertEqual(True, result2[0])
        self.assertEqual(0, result2[1])
        result3 = util.facts.precondition_fact_exists(
            fact_list3,
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic'
        )
        self.assertEqual(True, result3[0])
        self.assertEqual(-77, result3[1])
        result4 = util.facts.precondition_fact_exists(
            fact_list4,
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic'
        )
        self.assertEqual(False, result4[0])
        self.assertEqual(0, result4[1])

    def test_negative_number_with_dependence(self):
        """
        Verifies the check for negative numbers with dependencies works as
            expected
        """
        # The precondition fact is positive so the rule should execute
        mock_fact_model1 = mock.Mock(
            modelXbrl=mock.Mock(
                facts=[
                    self.fact_fire1, self.fact_fire2, self.fact_no_fire1,
                    self.fact_no_fire2, self.fact_no_fire3, self.fact_no_fire4,
                    self.fact_no_fire5, self.fact_precondition_positive
                ]
            )
        )
        # The precondition fact is zero so the rule should not execute
        mock_fact_model2 = mock.Mock(
            modelXbrl=mock.Mock(
                facts=[
                    self.fact_fire1, self.fact_fire2, self.fact_no_fire1,
                    self.fact_no_fire2, self.fact_no_fire3, self.fact_no_fire4,
                    self.fact_no_fire5, self.fact_precondition_zero
                ]
            )
        )
        # The precondition fact is negative so the rule should not execute
        mock_fact_model3 = mock.Mock(
            modelXbrl=mock.Mock(
                facts=[
                    self.fact_fire1, self.fact_fire2, self.fact_no_fire1,
                    self.fact_no_fire2, self.fact_no_fire3, self.fact_no_fire4,
                    self.fact_no_fire5, self.fact_precondition_negative
                ]
            )
        )
        # The precondition fact does not exist so the rule should not execute
        mock_fact_model4 = mock.Mock(
            modelXbrl=mock.Mock(
                facts=[
                    self.fact_fire1, self.fact_fire2, self.fact_no_fire1,
                    self.fact_no_fire2, self.fact_no_fire3, self.fact_no_fire4,
                    self.fact_no_fire5
                ]
            )
        )
        blacklist_dict = util.neg_num.concept_map_from_csv(
            dqc_us_0013._DEFAULT_CONCEPTS_FILE
        )
        results1 = dqc_us_0013.filter_negative_number_with_dependence_facts(
            mock_fact_model1, blacklist_dict.keys()
        )
        self.assertEqual(2, len(results1))
        results2 = dqc_us_0013.filter_negative_number_with_dependence_facts(
            mock_fact_model2, blacklist_dict.keys()
        )
        self.assertEqual(0, len(results2))
        results3 = dqc_us_0013.filter_negative_number_with_dependence_facts(
            mock_fact_model3, blacklist_dict.keys()
        )
        self.assertEqual(0, len(results3))
        results4 = dqc_us_0013.filter_negative_number_with_dependence_facts(
            mock_fact_model4, blacklist_dict.keys()
        )
        self.assertEqual(0, len(results4))
