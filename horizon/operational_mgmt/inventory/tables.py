# Copyright 2016, IBM US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from django.template import defaultfilters as filters
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import messages
from horizon import tables

import opsmgr.inventory.resource_mgr as resource_mgr

import logging


class AddResourceLink(tables.LinkAction):
    name = "addResource"
    verbose_name = _("Add Resource")
    url = "horizon:op_mgmt:inventory:addResource"
    classes = ("ajax-modal",)
    icon = "plus"
    rack_id = ""

    # required to prime the add resource dialog with the rack id
    def get_link_url(self, datum=None):
        if self.rack_id != "":
            return reverse(self.url, args=[self.rack_id])
        else:
            return self.url


class RemoveResources(tables.DeleteAction):
    name = "removeResources"
    success_url = reverse_lazy('horizon:op_mgmt:inventory:index')

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Remove Resource",
            u"Remove Resources",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Removed Resource",
            u"Removed Resources",
            count
        )

    def delete(self, request, obj_id):
        __method__ = 'tables.RemoveResources.delete'
        logging.debug("%s: Attempt to remove resource %s ",
                      __method__, obj_id)

        (rc, result_dict) = resource_mgr.remove_resource(None, False,
                                                         [obj_id])

        if rc != 0:
            # Log details of the unsuccessful attempt.
            logging.error("%s: Attempt to remove resource with id: %s"
                          " failed.", __method__, obj_id)
            logging.error(
                "%s: Unable to remove resource with id: %s. A Non-0 "
                " return code returned from resource_mgr.remove_resource."
                " The return code is: %s. Details of the attempt: "
                " %s", __method__, obj_id, rc, result_dict)

            # Show failure details
            msg = str(
                'Attempt to remove resource was not successful.  ' +
                'Details of the attempt: ' + result_dict)
            messages.error(request, msg)
            # Raise exception so that tables.delete shows generic failure
            raise Exception(msg)
        else:
            return


class RemoveResourcesLink(tables.LinkAction):
    # Link opens custom dialog to remove multiple resources from
    # a rack definition
    name = "removeResourcesLink"
    verbose_name = _("Remove Resources")
    url = "horizon:op_mgmt:inventory:removeResources"
    classes = ("ajax-modal", "btn-danger")
    icon = "trash"
    rack_id = ""

    # required to prime the remove resources dialog with the rack id
    def get_link_url(self, datum=None):
        if self.rack_id != "":
            return reverse(self.url, args=[self.rack_id])
        else:
            return self.url

    def allowed(self, request, datum):
        __method__ = 'tables.RemoveResourcesLink.allowed'
        # The Remove Resources button should always be displayed, but we want
        # it to be disabled when there are NO resources present.  For now
        # assume button is NOT disabled.
        disable_remove = False
        if self.rack_id != "":
            # Retrieve the resources for the selected rack
            logging.debug("%s: before retrieving resources for rack: %s",
                          __method__, self.rack_id)

            (rc, result_dict) = resource_mgr.list_resources(None, False, None,
                                                            None, False, False,
                                                            [self.rack_id])

            if rc != 0:
                # Unexpected.  Unable to retrieve rack information for selected
                # rack.  Log that fact, and allow the remove rack button to be
                # active
                msg = str('Unable to retrieve Operational Management inventory'
                          ' information for resources.')
                messages.error(request, msg)
                logging.error('%s: Unable to retrieve Operational Management'
                              ' inventory information. A Non-0 return code'
                              ' returned from resource_mgr.list_resources.'
                              ' The return code is: %s', __method__, rc)
            else:
                resources = result_dict['resources']
                # if the rack doesn't have any resources associated with it in
                # the inventory don't allow the user to delete it
                logging.debug("%s: got resource info for rack %s.  Number of "
                              "resources for this rack is: %s",
                              __method__, self.rack_id, len(resources))
                if len(resources) <= 0:
                    disable_remove = True

        if disable_remove:
            # Add the disabled class to the button (if it's not already
            # there)
            if 'disabled' not in self.classes:
                self.classes = list(self.classes) + ['disabled']
        else:
            # Remove the disabled class from the button (if it's still there)
            if 'disabled' in self.classes:
                self.classes.remove('disabled')
        return True


class EditResourceLink(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Resource")
    url = "horizon:op_mgmt:inventory:editResource"
    classes = ("ajax-modal",)
    icon = "pencil"


class ChangePasswordLink(tables.LinkAction):
    name = "changePassword"
    verbose_name = _("Change Password")
    url = "horizon:op_mgmt:inventory:changePassword"
    classes = ("ajax-modal",)
    icon = "pencil"


class EditRackLink(tables.LinkAction):
    name = "editRack"
    verbose_name = _("Edit Rack")
    url = "horizon:op_mgmt:inventory:editRack"
    classes = ("ajax-modal",)
    icon = "pencil"
    rack_id = ""

    # required to prime the edit rack dialog with the rack id
    def get_link_url(self, datum=None):
        if self.rack_id != "":
            return reverse(self.url, args=[self.rack_id])
        else:
            return self.url


class RemoveRackLink(tables.LinkAction):
    name = "removeRack"
    verbose_name = _("Remove Rack")
    url = "horizon:op_mgmt:inventory:removeRack"
    classes = ("ajax-modal", "btn-danger",)
    icon = "trash"
    rack_id = ""

    # required to prime the remove rack dialog with the rack id
    def get_link_url(self, datum=None):
        if self.rack_id != "":
            return reverse(self.url, args=[self.rack_id])
        else:
            return self.url

    def allowed(self, request, datum):
        return False  # hide Remove Rack function for now
        __method__ = 'tables.RemoveRackLink.allowed'

        # The Remove Rack button should always be displayed, but we want
        # it to be disabled when there are any resources present.  For now
        # assume button is NOT disabled.
        disable_delete = False
        if self.rack_id != "":
            # list_resources(labels=None, isbriefly=False, device_types=None,
            # resourceids=None, list_device_id=False, is_detail=False,
            # racks=None)
            # Retrieve the resources for the selected rack
            logging.debug("%s: before retrieving resources for rack: %s",
                          __method__, self.rack_id)

            (rc, result_dict) = resource_mgr.list_resources(None, False, None,
                                                            None, False, False,
                                                            [self.rack_id])

            if rc != 0:
                # Unexpected.  Unable to retrieve rack information for selected
                # rack.  Log that fact, and allow the remove rack button to be
                # active
                msg = str('Unable to retrieve Operational Management inventory'
                          ' information for resources.')
                messages.error(request, msg)
                logging.error('%s: Unable to retrieve Operational Management'
                              ' inventory information. A Non-0 return code'
                              ' returned from resource_mgr.list_resources.'
                              ' The return code is: %s', __method__, rc)
            else:
                resources = result_dict['resources']
                # if the rack has any resources associated with it in the
                # inventory don't allow the user to delete it
                logging.debug("%s: got resource info for rack %s.  Number of "
                              "resources for this rack is: %s",
                              __method__, self.rack_id, len(resources))
                if len(resources) > 0:
                    disable_delete = True

        if disable_delete:
            # Add the disabled class to the button (if it's not already
            # there)
            if 'disabled' not in self.classes:
                self.classes = list(self.classes) + ['disabled']
        else:
            # Remove the disabled class from the button (if it's still there)
            if 'disabled' in self.classes:
                self.classes.remove('disabled')
        return True


class ResourceFilterAction(tables.FilterAction):
    name = "resource_filter"

    def filter(self, table, resources, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [resource for resource in resources
                if q in resource.name.lower()]


class NameLinkColumn(tables.Column):
    # Will make the label column a link if there is a web_url associated with
    # the resource. Also ensure the link opens to a new window (that is a
    # unique window for that particular resource)
    def get_link_url(self, datum=None):
        if datum.web_url:
            self.link_attrs['target'] = datum.name
            return datum.web_url
        else:
            return None


class ResourcesTable(tables.DataTable):
    name = NameLinkColumn('name',
                          verbose_name=_('Label'),
                          link=True)
    type = tables.Column('type',
                         verbose_name=_("Type"))
    arch = tables.Column('arch',
                         verbose_name=("Architecture"))
    capabilities = tables.Column(
        lambda obj: getattr(obj, 'capabilities', []),
        verbose_name=_("Capabilities"),
        hidden=True,
        wrap_list=False,
        filters=(filters.unordered_list,))
    rack_loc = tables.Column('rack_loc',
                             verbose_name=_("EIA Location"))
    userid = tables.Column('userid',
                           verbose_name=_("Management User"))
    mtm = tables.Column('mtm',
                        verbose_name=_("Machine Type/Model"))
    serial_num = tables.Column('sn',
                               verbose_name=_("Serial Number"))
    host_name = tables.Column(
        lambda obj: getattr(obj, 'host_name', []),
        verbose_name=_("Host Name"),
        wrap_list=True,
        filters=(filters.unordered_list,))
    version = tables.Column('version',
                            verbose_name=_("Installed Version"))
    resource_id = tables.Column('resource_id',
                                hidden=True,
                                verbose_name=_("Resource ID"))

    class Meta(object):
        name = "resources"
        verbose_name = _("Resources")
        multi_select = False
        row_actions = (EditResourceLink, ChangePasswordLink,
                       RemoveResources)
        table_actions = (ResourceFilterAction, AddResourceLink,
                         RemoveResourcesLink)


class RackDetailsTable(tables.DataTable):
    # This is a generic table (id, label/title, value)
    row_title = tables.Column('row_title',
                              attrs={'width': '150px', },
                              verbose_name=_("Rack Property"))
    row_value = tables.Column('row_value',
                              attrs={'width': '400px', },
                              verbose_name=_("Value"))

    class Meta(object):
        name = "rack_details"
        verbose_name = _("Rack Details")
        multi_select = False
        footer = False
        filter = False
        # Until we have Add Rack function, we don't allow
        # remove rack to be present (Remove Rack is hidden
        # via its 'allowed' function)
        table_actions = (EditRackLink, RemoveRackLink)


class RemoveResourcesTable(tables.DataTable):
    name = NameLinkColumn('name',
                          verbose_name=_('Label'))
    type = tables.Column('type',
                         verbose_name=_("Type"))
    hostname = tables.Column('hostname',
                             verbose_name=_("Host Name"))
    ip_address = tables.Column('ip_address',
                               verbose_name=_("IP Address"))

    class Meta(object):
        name = "removeResources"
        verbose_name = _("Remove Resources")
        multi_select = True
        # Allow resource filtering, and the ability to remove
        # multiple resources as table actions
        table_actions = (ResourceFilterAction, RemoveResources)
