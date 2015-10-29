# -*- coding:utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Savoir-faire Linux. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, fields, models, _


class HrActivity(models.Model):
    """Employee Activity"""

    _name = 'hr.activity'
    _description = _(__doc__)

    name = fields.Char(
        'Activity Name',
        compute='_compute_name',
        store=True,
        readonly=True,
    )
    activity_type = fields.Selection(
        [
            ('leave', 'Leave'),
            ('job', 'Job'),
        ],
        'Activity Type',
        required=True,
    )
    job_id = fields.Many2one(
        'hr.job',
        'Job',
        ondelete='cascade',
    )
    leave_id = fields.Many2one(
        'hr.holidays.status',
        'Leave Type',
        ondelete='cascade',
    )

    _order = 'type,name'

    @api.one
    @api.depends('activity_type', 'job_id', 'leave_id')
    def _compute_name(self):
        if self.activity_type == 'job':
            self.name = self.job_id.name_get()[1]

        elif self.activity_type == 'leave':
            self.name = self.leave_id.name_get()[1]

    @api.onchange('activity_type')
    def onchange_activity_type(self):
        if self.activity_type == 'job':
            self.leave_id = None

        elif self.activity_type == 'leave':
            self.job_id = None