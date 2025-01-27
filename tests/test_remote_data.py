from unittest import TestCase

from gig import ent_types

from elections_lk.elections import remote_data


class TestRemoteData(TestCase):
    def test_parse_int(self):
        for x, expected_int in [
            ['1', 1],
            ['1.0', 1],
            ['1.01234', 1],
            ['0.9999', 1],
            ['12', 12],
            ['123.003', 123],
            [0, 0],
            ['0', 0],
            ['', 0],
            [None, 0],
        ]:
            self.assertEqual(remote_data.parse_int(x), expected_int)

    def test_get_raw_result_list(self):
        raw_result_list = remote_data.get_raw_result_list(
            'presidential', 2019
        )
        self.assertEqual(len(raw_result_list), 14_532)
        keys = list(raw_result_list[0].keys())
        for k in ['entity_id', 'valid', 'rejected', 'polled', 'electors']:
            self.assertIn(k, keys)

    def test_filter_by_entity_type(self):
        raw_result_list = remote_data.get_raw_result_list(
            'presidential', 2019
        )
        for entity_type, n_results in [
            [ent_types.ENTITY_TYPE.PD, 182],
            [ent_types.ENTITY_TYPE.ED, 22],
            [ent_types.ENTITY_TYPE.COUNTRY, 1],
        ]:
            filtered_raw_result_list = remote_data.filter_by_entity_type(
                raw_result_list,
                entity_type,
            )
            self.assertEqual(len(filtered_raw_result_list), n_results)
            first_result = filtered_raw_result_list[0]
            self.assertEqual(
                ent_types.get_entity_type(first_result['entity_id']),
                entity_type,
            )

    def test_get_result_list(self):
        for entity_type, n_results, party, votes in [
            [ent_types.ENTITY_TYPE.PD, 182, 'SLPP', 16_986],
            [ent_types.ENTITY_TYPE.ED, 22, 'SLPP', 727_713],
            [ent_types.ENTITY_TYPE.COUNTRY, 1, 'SLPP', 6_924_255],
        ]:
            result_list = remote_data.get_result_list(
                'presidential',
                2019,
                entity_type,
            )
            self.assertEqual(len(result_list), n_results)
            first_result = result_list[0]
            self.assertEqual(
                ent_types.get_entity_type(first_result.entity_id),
                entity_type,
            )
            self.assertEqual(first_result.party_to_votes[party], votes)
