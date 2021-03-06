#coding=utf-8

########################################################################
#@author:   bobfu
#@email:    fubo@cnic.cn
#@date:     2015-10-16
#@desc:    宿主机相关的API函数，每一个函数封装并实现一个API接口的功能。
########################################################################

from compute.api import HostAPI
from compute.api import GroupAPI
from .tools import args_required
from .tools import catch_error
from .tools import api_log
from .error import ERR_AUTH_PERM

@api_log
@catch_error
@args_required('host_id')
def get(args):
    host_api = HostAPI()
    host = host_api.get_host_by_id(args['host_id'])
    
    if not host.managed_by(args['req_user']):
        return {'res': False, 'err': ERR_AUTH_PERM}
     
    return {'res': True,
            'info': {
                     'id': host.id,
                     'group_id': host.group_id,
                     'vlan_list': host.vlans,
                     'ipv4': host.ipv4,
                     'vcpu_total': host.vcpu_total,
                     'vcpu_allocated': host.vcpu_allocated,
                     'mem_total': host.mem_total,
                     'mem_allocated': host.mem_allocated,
                     'mem_reserved': host.mem_reserved,
                     'vm_limit': host.vm_limit,
                     'vm_created': host.vm_created,
                     'enable': host.enable
                     }}

@api_log
@catch_error
@args_required('group_id')
def get_list(args):
    '''获取宿主机列表'''
    ret_list = []
    group_api = GroupAPI()
    group = group_api.get_group_by_id(args['group_id'])
    
    if not group.managed_by(args['req_user']):
        return {'res': False, 'err': ERR_AUTH_PERM}
    
    host_api = HostAPI()
    host_list = host_api.get_host_list_by_group_id(args['group_id'])
     
    for host in host_list:
        ret_list.append({
            'id':   host.id,
            'group_id': host.group_id,
            'ipv4': host.ipv4,
            'vcpu_total': host.vcpu_total,
            'vcpu_allocated': host.vcpu_allocated,
            'mem_total': host.mem_total,
            'mem_allocated': host.mem_allocated,
            'mem_reserved': host.mem_reserved,
            'vm_limit': host.vm_limit,
            'vm_created': host.vm_created,
            'enable': host.enable,
            'net_types':[vlan[1] for vlan in host.vlan_types]})
    return {'res': True, 'list': ret_list}