#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class ResultsService(object):
    RESOURCE = 'results'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        return self.service.list(self.base, filter, sort, limit, page)

    def list_csv(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        return self.service.list(self.base, filter, sort, limit, page, format='csv')

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get_id(self.base, id)

    def stop(self, id, when=None): # pylint: disable=invalid-name,redefined-builtin
        return self.service.post(self.base+str(id)+'/stop/', params={'when': when})

    def stop_end_of_test(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.stop(id, 'end-of-test')

    def stop_end_of_loop(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.stop(id, 'end-of-loop')

    def pause(self, id, when=None): # pylint: disable=invalid-name,redefined-builtin
        return self.service.post(self.base+str(id)+'/pause/', params={'when': when})

    def pause_end_of_test(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.pause(id, 'end-of-test')

    def pause_end_of_loop(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.pause(id, 'end-of-loop')

    def unpause(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.service.post(self.base+str(id)+'/unpause/')

    def edit(self, resource):
        return self.service.edit(self.base, resource['id'], resource)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.service.shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id, exclude_captures=False): # pylint: disable=invalid-name,redefined-builtin
        return self.service.export(self.base, id, params={'exclude_captures': exclude_captures})

    def bulk_export(self, ids, exclude_captures=False):
        return self.service.bulk_export(self.base, ids, params={'exclude_captures': exclude_captures})

    def bulk_copy(self, ids):
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        return self.service.bulk_edit(self.base, self.RESOURCE, fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)

    def all_stats(self):
        return self.service.post(self.base, params={'stats': 'all'})

    def set_stats(self, ids):
        return self.service.post(self.base, params={'stats': 'set'}, json=[{'id': str(x)} for x in ids])

    def single_stats(self, id): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get(self.base+str(id)+'/', params={'stats': 'all'})

    def list_logdir(self, id, filter=None, sort=None): # pylint: disable=invalid-name,redefined-builtin
        return self.service.list(self.base+str(id)+'/logdir/', filter, sort)

    def get_logdir_file(self, id, filename): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get(self.base+str(id)+'/logdir/'+filename+'/')

    def download_logdir_archive(self, id, filename, format='zip', exclude_captures=False): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get(self.base+str(id)+'/logdir/'+filename+'/', params={'format': format, 'exclude_captures': exclude_captures})

    def get_test_metric(self, id, name, metric, format=None): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get(self.base+str(id)+'/metrics/'+name+'/'+metric+'/',
                                params={'format': format})

    def get_test_metric_csv(self, id, name, metric): # pylint: disable=invalid-name,redefined-builtin
        return self.get_test_metric(id, name, metric, format='csv')
