from datetime import timedelta
from corehq.apps.reports.datatables import DataTablesHeader, DataTablesColumn
from corehq.apps.reports.generic import GenericTabularReport
from corehq.apps.reports.standard import CustomProjectReport
from corehq.apps.users.models import CommCareUser
from pact.enums import PACT_DOMAIN
from pact.models import PactPatientCase, CObservation
from pact.reports import chw_schedule


class PactCHWAdminReport(GenericTabularReport, CustomProjectReport):
    fields = ['corehq.apps.reports.fields.SelectMobileWorkerField',  'corehq.apps.reports.fields.DatespanField']
    name = "PACT CHW Admin"
    slug = "pactchwadmin"
    emailable = True
    exportable = True
    report_template_path = "pact/admin/pact_chw_schedule_admin.html"

    def tabular_data(self, mode, case_id, start_date, end_date):#, limit=50, skip=0):
        try:
            case_doc = PactPatientCase.get(case_id)
            pactid = case_doc.pactid
        except:
            case_doc = None
            pactid = None

        if case_doc is not None:
            if mode == 'all':
                start_date = end_date - timedelta(1000)
                startkey = [case_id, 'anchor_date', start_date.year,
                            start_date.month, start_date.day]
                endkey = [case_id, 'anchor_date', end_date.year, end_date.month,
                          end_date.day]
                csv_filename = 'dots_csv_pt_%s.csv' % (pactid)
            else:
                startkey = [case_id, 'anchor_date', start_date.year,
                            start_date.month, start_date.day]
                endkey = [case_id, 'anchor_date', end_date.year, end_date.month,
                          end_date.day]
                csv_filename = 'dots_csv_pt_%s-%s_to_%s.csv' % (
                    pactid, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        elif case_doc is None:
            if mode == 'all':
                start_date = end_date - timedelta(1000)
                startkey = [start_date.year, start_date.month, start_date.day]
                endkey = [end_date.year, end_date.month, end_date.day]
                csv_filename = 'dots_csv_pt_all.csv'
            else:
                startkey = [start_date.year, start_date.month, start_date.day]
                endkey = [end_date.year, end_date.month, end_date.day]
                csv_filename = 'dots_csv_pt_all-%s_to_%s.csv' % (
                    start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
                #heading
        view_results = CObservation.view('pact/dots_observations', startkey=startkey, endkey=endkey)#, limit=limit, skip=skip)

        for v in view_results:
            yield v

    @property
    def headers(self):
        headers = DataTablesHeader(
            DataTablesColumn("Scheduled Date"),
            DataTablesColumn("CHW Scheduled"),
            DataTablesColumn("Patient"),
            DataTablesColumn("Scheduled"),
            DataTablesColumn("Visit Kept"),
            DataTablesColumn("Type"),
            DataTablesColumn("Contact"),
            DataTablesColumn("CHW Visited"),
            DataTablesColumn("Observed ART"),
            DataTablesColumn("Pillbox Check"),
            DataTablesColumn("Doc ID"),
        )
        return headers

    def csv_data(self, username, user_context):

        # return_context['date_arr'] = ret
        # return_context['total_scheduled'] = total_scheduled
        # return_context['total_visited'] = total_visited
        # return_context['start_date'] = ret[0][0]
        # return_context['end_date'] = ret[-1][0]

        rowdata = []
        # {% for visit_date, patient_visits in date_arr %}
        # {% if patient_visits %}
        # {% for cpatient, visit in patient_visits %}
        # {% if visit %}

        #this is ugly, but we're repeating the work of the template for rendering the row data
        for visit_date, patient_visits in user_context['date_arr']:
            if len(patient_visits) > 0:
                for patient_case, visit in patient_visits:
                    rowdata = [visit_date.strftime('%Y-%m-%d')]
                    rowdata.append(username)
                    rowdata.append(patient_case['pactid'])
                    if visit is not None:
                        ####is scheduled
                        if visit['scheduled'] == 'yes':
                            rowdata.append('scheduled')
                        else:
                            rowdata.append('unscheduled')

                        ####visit kept
                        if visit['visit_kept'] == 'notice':
                            rowdata.append("no - notice given")
                        elif visit['visit_kept'] == 'yes':
                            rowdata.append("yes")
                        else:
                            rowdata.append(visit['visit_kept'])

                        #visit type
                        rowdata.append(visit['visit_type'])

                        #contact type
                        rowdata.append(visit['contact_type'])

                        rowdata.append(visit['username'])
                        rowdata.append(visit['observed_art'])
                        rowdata.append(visit['has_pillbox_check'])
                        rowdata.append(visit['doc_id'])
                    else:
                        rowdata.append('novisit')
            else:
            #     no patients
                rowdata = [visit_date.strftime('%Y-%m-%d'), username, 'nopatient']
            if len(rowdata) < 11:
                for x in range(11 - len(rowdata)):
                    rowdata.append('---')
            yield rowdata



    @property
    def rows(self):
        """
            Override this method to create a functional tabular report.
            Returns 2D list of rows.
            [['row1'],[row2']]
        """
        user_id = self.request.GET.get('individual', None)

        if user_id is None or user_id == '':
            #all users
            user_docs = CommCareUser.by_domain(PACT_DOMAIN)
        else:
            user_docs = [CommCareUser.get(user_id)]

        for user_doc in user_docs:
            scheduled_context = chw_schedule.chw_calendar_submit_report(self.request, user_doc.raw_username)
            for row in self.csv_data(user_doc.raw_username, scheduled_context):
                yield row

    @property
    def total_records(self):
        """
            Override for pagination.
            Returns an integer.
        """
        return 1000


    @property
    def shared_pagination_GET_params(self):
        """
        Override the params and applies all the params of the originating view to the GET
        so as to get sorting working correctly with the context of the GET params
        """
        ret = []
        for k, v in self.request.GET.items():
            ret.append(dict(name=k, value=v))
        return ret

