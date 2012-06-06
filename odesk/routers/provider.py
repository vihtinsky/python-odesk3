"""
Python3 bindings to odesk API
python-odesk3 version 0.1
(C) 2012 oDesk
"""

from odesk.namespaces import Namespace


class Provider(Namespace):
    api_url = 'profiles/'
    version = 1

    resume_info_result_keys = {'otherexp': 'experiences',
                               'skills': 'skills',
                               'tests': 'tests',
                               'certificates': 'certificates',
                               'employments': 'employments',
                               'educations': 'educations',
                               'projects': 'projects',
                               'quickinfo': 'quick_info'
                               }

    def get_provider(self, provider_ciphertext):
        """
        Retrieve an exhastive list of atributes associated with the referenced provider

        Parameters
          provider_ciphertext   The provider's cipher text (key)
        """
        url = 'providers/%s' % str(provider_ciphertext)
        result = self.get(url)
        return result['profile']

    def get_provider_brief(self, provider_ciphertext):
        """
        Retrieve an brief list of atributes associated with the referenced provider

        Parameters
          provider_ciphertext   The provider's cipher text (key)
        """
        url = 'providers/%s/brief' % str(provider_ciphertext)
        result = self.get(url)
        return result['profile']

    def get_providers(self, data=None, page_offset=0, page_size=20, order_by=None):
        """
        Search oDesk providers

        Parameters
          data          A dict (q:query, c1:Job Category, c2:Secondary Category,
                        fb:Feedback, hrs:Hours, ir:Is Recent, min:Min Hourly Rate,
                        max:Max Hourly Rate, loc:Location, pt:Provider Type,
                        last:Last Activity, test:Test, port:Total Portfolio Items,
                        rdy:Is oDesk Ready, ui:English Skills, ag:Agency,
                        to:Titles Only, g:Group Member)
          page_offset   Start of page (number of results to skip) (optional)
          page_size     Page size (number of results) (optional: default 20)
          order_by
        """
        url = 'search/providers'
        if data is None:
            data = {}     # shouldn't use data={} as default arg value (mutations persist throughout calls)
        data['page'] = '%d;%d' % (page_offset, page_size)
        if order_by is not None:
            data['order_by'] = order_by
        result = self.get(url, data=data)
        return result['providers']

    def get_jobs(self, data=None, page_offset=0, page_size=20, order_by=None):
        """
        Search oDesk jobs

        Parameters
          data          A dict (q:query, c1:Job Category, c2:Secondary Category,
                        fb:Feedback, min:Min Budget, max:Max Budget, t:Job Type,
                        wl:Hours/Week, dur:Duration of Engagement, dp:Date Posted,
                        st:Status for Search, tba:Total Billed Assignments,
                        gr:Pref Group, to:Titles Only)
          page_offset   Start of page (number of results to skip) (optional)
          page_size     Page size (number of results) (optional: default 20)
          order_by
        """
        url = 'search/jobs'
        if data is None:
            data = {}     # shouldn't use data={} as default arg value (mutations persist throughout calls)
        data['page'] = '%d;%d' % (page_offset, page_size)
        if order_by is not None:
            data['order_by'] = order_by
        result = self.get(url, data=data)
        return result['jobs']

    def _get_resume_info(self, provider_ciphertext, info_type):
        """
        info_type can be one of
        (otherexp|skills|tests|certificates|employments|\
        educations|projects)
        """
        strinfo = str(info_type)
        if strinfo not in self.resume_info_result_keys:
            raise ValueError('invalid info_type %s' % strinfo)
        url = 'providers/%s/%s' % (str(provider_ciphertext), strinfo)
        result = self.get(url)
        result_key = self.resume_info_result_keys[strinfo]
        return result[result_key]

    def _add_resume_info_item(self, provider_ciphertext, info_type, \
        item_data):
        """
        info_type can be one of
        (otherexp|skills|tests|certificates|employments|\
        educations|projects
        """
        strinfo = str(info_type)
        if strinfo not in self.resume_info_result_keys:
            raise ValueError('invalid info_type %s' % strinfo)
        url = 'providers/%s/%s' % (str(provider_ciphertext), strinfo)
        return self.post(url, item_data)

    def _update_resume_info_item(self, provider_ciphertext, \
        resource_id, info_type, item_data):
        """
        info_type can be one of (otherexp|skills|tests|certificates|\
        employments|educations|projects
        """
        strinfo = str(info_type)
        if strinfo not in self.resume_info_result_keys:
            raise ValueError('invalid info_type %s' % strinfo)

        if resource_id is not None:
            url = 'providers/%s/%s/%s' % (str(provider_ciphertext), \
                str(resource_id), strinfo)
        else:
            url = 'providers/%s/%s' % (str(provider_ciphertext), \
                strinfo)
        return self.post(url, item_data)

    def _delete_resume_info_item(self, provider_ciphertext, \
        resource_id, info_type):
        """
        info_type can be one of (otherexp|skills|tests|certificates|\
        employments|educations|projects
        """
        strinfo = str(info_type)
        if strinfo not in self.resume_info_result_keys:
            raise ValueError('invalid info_type %s' % strinfo)

        if resource_id is not None:
            url = 'providers/%s/%s/%s' % (str(provider_ciphertext), \
                str(resource_id), strinfo)
        else:
            url = 'providers/%s/%s' % (str(provider_ciphertext), \
                strinfo)

        return self.delete(url)

    def get_skills(self, provider_ciphertext):
        """
        Retrieve provider skills info

        Parameters
          provider_ciphertext   Provider cipher text (key)
        """
        return self._get_resume_info(provider_ciphertext, 'skills')

    def get_quickinfo(self, provider_ciphertext):
        """
        Retrieve provider 'quick info'

        Parameters
          provider_ciphertext   Provider cipher text (key)
        """
        return self._get_resume_info(provider_ciphertext, 'quickinfo')

    def update_quickinfo(self, provider_ciphertext, data):
        """
        Update provider 'quick info'

        Parameters
          provider_ciphertext   Provider cipher text (key)
          data                  A dict containing updated 'quick info'
        """
        return self._update_resume_info_item(provider_ciphertext, None, \
                                            'quickinfo', data)

    def get_affiliates(self, affiliate_key):
        """
        Retrieve provider affiliates

        Parameters
          affiliate_key
        """
        url = 'affiliates/%s' % affiliate_key
        result = self.get(url)
        return result['profile']
