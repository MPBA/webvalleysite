from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import json
import re

class DictWidget(forms.Widget):
    def __init__(self,
                 mandatory_choices,
                 optional_choices=[],
                 allow_others=False,
                 attrs=None,
                 **kwargs):
        super(DictWidget, self).__init__(attrs)
        self.attrs['class'] = 'marks_widget'
        
        self.mandatory_choiches = mandatory_choices
        self.optional_choiches = optional_choices
        self.allow_others = allow_others
        
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif type(value) != tuple:
            newval_k = {}
            newval_v = {}
            for i,key in enumerate(value.keys()):
                newval_k[str(i)] = key
                newval_v[str(i)] = value[key]
            value = (newval_k, newval_v)
        final_attrs = self.build_attrs(attrs, name=name)
        
        js_allow_others = None;
        if self.allow_others == True:
            js_allow_others = 'true'
        elif self.allow_others == False:
            js_allow_others = 'false'
        else:
            raise ValueError(u"DictWidget: error: argument allow_others"+
                             u"must be boolean")
        return mark_safe(
            u"""
<script type="text/javascript">
  mw_params["{name}"] = {{}};
  mw_params["{name}"].mandatory = {mandatory};
  mw_params["{name}"].optional = {optional};
  mw_params["{name}"].allow_other = {allow_other};
  $(function(){{ marks_widget_init("{name}"); }});
</script>
<span{attrs}><span class="field_content" style="display:none;">{val}</span></span>
             """ .format( name = name,
                          mandatory = json.dumps(self.mandatory_choiches),
                          optional = json.dumps(self.optional_choiches),
                          allow_other = js_allow_others,
                          attrs = flatatt(final_attrs),
                          val = json.dumps(value), )
        )

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        rk = re.compile("%s_(\d+)_key" % name)
        rv = re.compile("%s_(\d+)_val" % name)

        ret_k = {}
        ret_v = {}
        
        for elem in data.keys():
            res = rk.search(elem)
            if res:
                num = res.groups()[0]
                ret_k[num] = data[elem]
            res = rv.search(elem)
            if res:
                num = res.groups()[0]
                ret_v[num] = data[elem]
        if ret_k or ret_v:
            return ret_k, ret_v
        else:
            return None
        
        #for elem in data.keys():
        #    res = r.search(elem)
        #    if res:
        #        num = res.groups[0]
        #        k = data[elem]
        #        v = data["%s_%s_val" % (name, num)]
        #        ret[k] = v
        #return json.dumps(ret)

class DictField(forms.Field):
    def __init__(self,
                 mandatory_choices,
                 optional_choices,
                 allow_others,
                 min_optional_fields=0,
                 **kwargs):
        # set default widget: will be overriden by super.__init__
        # if 'widget' was specified in kwargs
        self.widget = DictWidget(mandatory_choices,
                                 optional_choices,
                                 allow_others)
        super(DictField, self).__init__(**kwargs)
        self.mandatory_choices = mandatory_choices
        self.optional_choices = optional_choices
        self.allow_others = allow_others
        self.min_optional_fields = min_optional_fields

    def to_python(self, value):
        if not value:
            return None
        (keys, vals) = value
        ret = {}
        for i in keys:
            # add the key[i]:val[i] pair only if both are not empty
            if keys[i] and (i in vals):
                if vals[i]:
                    if keys[i] not in ret:
                        ret[keys[i]] = vals[i]
                    else:
                        raise forms.ValidationError(
                            _(u"Duplicate field value (only one was kept)."))
        return ret

    def validate(self, value):
        super(DictField, self).validate(value)
        for mand in self.mandatory_choices:
            if mand not in value:
                raise forms.ValidationError(_(u"Blank mandatory field"))
        if not self.allow_others:
            for key in value:
                if ((key not in self.mandatory_choices) and
                    (key not in self.optional_choices)
                    ):
                    raise forms.ValidationError(
                        _(u"Optional field not allowed."))
        if (len(value) - len(self.mandatory_choices)) < self.min_optional_fields:
            raise forms.ValidationError(
                _(u"You must specify at least %i fields, excluding the mandatory ones.")
                    % self.min_optional_fields)
                

class HiddenField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = forms.HiddenInput()
        super(HiddenField, self).__init__(*args, **kwargs)
