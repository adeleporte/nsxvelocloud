#!/usr/bin/python
def retrieve_scope(session, tz_name):
    vdn_scopes = session.read('vdnScopes', 'read')['body']
    vdn_scope_dict_list = vdn_scopes['vdnScopes']['vdnScope']
    vdn_scope_id = None
    if isinstance(vdn_scope_dict_list, dict):
        if vdn_scope_dict_list['name'] == tz_name:
            vdn_scope_id = vdn_scope_dict_list['objectId']
    elif isinstance(vdn_scope_dict_list, list):
        try:
            vdn_scope_id = [scope['objectId'] for scope in vdn_scope_dict_list if scope['name'] == tz_name][0]
        except IndexError:
            vdn_scope_id = None

    if vdn_scope_id:
        return vdn_scope_id
    else:
        return None

def get_lswitch_id(session, lswitchname, scope):
    lswitches_api = session.read_all_pages('logicalSwitches', uri_parameters={'scopeId': scope})
    all_lswitches = session.normalize_list_return(lswitches_api)

    for lswitch_dict in all_lswitches:
        if lswitchname == lswitch_dict.get('name'):
            return [lswitch_dict.get('objectId')]

    return []


def get_lswitch_details(session, lswitch_id):
    return session.read('logicalSwitch', uri_parameters={'virtualWireID': lswitch_id})['body']


class FilterModule(object):
  def filters(self):
    return {
             'to_portgroup': self.to_portgroup,
           }
 
  def to_portgroup(self, a_variable, nsxmanager_spec, transportzone):
    from nsxramlclient.client import NsxClient
    client_session=NsxClient(nsxmanager_spec['raml_file'], nsxmanager_spec['host'],
                             nsxmanager_spec['user'], nsxmanager_spec['password'])

    vdn_scope=retrieve_scope(client_session, transportzone)
    lswitch_id=get_lswitch_id(client_session, a_variable, vdn_scope)
    if len(lswitch_id) is not 0:
        lswitch_details=get_lswitch_details(client_session,lswitch_id[0])
        a_new_variable = 'vxw-' + lswitch_details['virtualWire']['vdsContextWithBacking']['switch']['objectId'] + '-' \
                                + lswitch_details['virtualWire']['objectId'] + '-sid-' \
                               + lswitch_details['virtualWire']['vdnId'] + '-' \
                              + lswitch_details['virtualWire']['name']
        return a_new_variable
    else:
        return None
