# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class project_issue(osv.Model):
    _inherit = 'project.issue'
    
    _columns = {
		'complaintno':fields.char('Complaint Number', required=True, readonly=True),    
		'x_actionby': fields.many2one('res.users', 'Action by', required=False, select=1), 
		'x_comments': fields.text('Comments'),
	    'x_actionreq': fields.text('Corrective Actions'),
		'x_followup': fields.text('Follow Up'),
        'x_tags': fields.selection([('C','Commercial'), ('EN','Environmental'), ('EQ','Equipment'),('S','Safety/Health'),('M','Maintenance'),('O','Operations')], 'Type', select=True),
    }
    
    _defaults = {
        'complaintno': 'NEW',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('complaintno', 'NEW') == 'NEW':
            vals['complaintno'] = self.pool.get('ir.sequence').get(cr, uid, 'project.issue') or 'NEW'
        context = dict(context or {})
        if vals.get('project_id') and not context.get('default_project_id'):
            context['default_project_id'] = vals.get('project_id')
        if vals.get('user_id') and not vals.get('date_open'):
            vals['date_open'] = fields.datetime.now()
        if 'stage_id' in vals:
            vals.update(self.onchange_stage_id(cr, uid, None, vals.get('stage_id'), context=context)['value'])

        # context: no_log, because subtype already handle this
        create_context = dict(context, mail_create_nolog=True)
        return super(project_issue, self).create(cr, uid, vals, context=create_context)

    def for_validation(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'stage_id': 8})

    def validate(self, cr, uid, ids, context=None):
	    return self.write(cr, uid, ids, {'stage_id': 9})
    def done(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'stage_id': 10})
    def completed(self, cr, uid, ids, context=None):	
        return self.write(cr, uid, ids, {'stage_id': 11})
    		
    
