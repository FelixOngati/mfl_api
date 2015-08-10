from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from facilities.models import Facility
from common.models import Ward, County, Constituency
from model_mommy import mommy


class TestFacilityCountByCountyReport(APITestCase):
    def setUp(self):
        super(TestFacilityCountByCountyReport, self).setUp()

    def test_facility_count_per_county_report(self):
        county = mommy.make(County)
        county_2 = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        constituency_2 = mommy.make(Constituency, county=county_2)
        ward = mommy.make(Ward, constituency=constituency)
        ward_2 = mommy.make(Ward, constituency=constituency_2)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility, ward=ward_2)
        mommy.make(Facility, ward=ward_2)
        url = reverse("api:reporting:facility_by_county_report")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_data = {
            "results": [
                {
                    "county_name": county.name,
                    "number_of_facilities": 5
                },
                {
                    "county_name": county_2.name,
                    "number_of_facilities": 2
                }
            ],
            "total": 7
        }
        self.assertEquals(expected_data, response.data)
