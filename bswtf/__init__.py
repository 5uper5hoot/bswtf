import wtforms as __wtf
from markupsafe import Markup
import wtforms.ext.sqlalchemy.fields as __wtfa
from wtforms.widgets import html_params

__all__ = [
    "AccordianWidget",
    "BooleanField",
    "CardWidget",
    "CheckboxInput",
    "DateField",
    "DateTimeField",
    "DecimalField",
    "FieldList",
    "FloatField",
    "Form",
    "FormField",
    "IntegerField",
    "Input",
    "PasswordInput",
    "QuerySelectField",
    "RadioField",
    "RadioInput",
    "Select",
    "SelectField",
    "SelectMultipleField",
    "StringField",
    "SubmitField",
    "SubmitInput",
    "TextArea",
    "TextInput",
    "TimeField",
]


def form_check(fn):
    def wrapper(self, field, *args, **kwargs):
        class_ = kwargs.get("class", kwargs.get("class_", None))
        if not class_:
            kwargs["class_"] = "form-check-input"
        rendered_field = fn(self, field, *args, **kwargs)

        if self.inc_label:
            label = field.label(class_="form-check-label")
        else:
            label = ""

        content = "".join([rendered_field, label])
        return Markup(
            f"""
<div class="form-group form-check">
  {content}
</div>
        """.strip()
        )

    return wrapper


def form_group(fn):
    def wrapper(self, field, *args, **kwargs):
        class_ = kwargs.get("class", kwargs.get("class_", None))
        if not class_:
            kwargs["class_"] = "form-control"
        rendered_field = fn(self, field, *args, **kwargs)

        if self.inc_label:
            label = field.label(class_="form-check-label")
        else:
            label = ""

        content = "".join([label, rendered_field])
        return Markup(
            f"""
<div class="form-group">
  {content}
</div>
        """.strip()
        )

    return wrapper


class CheckMixin:
    def __init__(self, inc_label=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inc_label = inc_label

    @form_check
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class InputMixin:
    def __init__(self, inc_label=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inc_label = inc_label

    @form_group
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class Input(InputMixin, __wtf.widgets.Input):
    pass


class TextInput(InputMixin, __wtf.widgets.TextInput):
    pass


class PasswordInput(InputMixin, __wtf.widgets.PasswordInput):
    pass


class CheckboxInput(CheckMixin, __wtf.widgets.CheckboxInput):
    pass


class RadioInput(CheckMixin, __wtf.widgets.RadioInput):
    pass


class SubmitInput(__wtf.widgets.SubmitInput):
    def __call__(self, field, **kwargs):
        class_ = kwargs.get("class", kwargs.get("class_", None))
        if not class_:
            kwargs["class"] = "btn btn-primary"
        return super().__call__(field, **kwargs)


class TextArea(InputMixin, __wtf.widgets.TextArea):
    pass


class Select(InputMixin, __wtf.widgets.Select):
    pass


class CardWidget:
    def __init__(self, render_fn=None, title_fn=None):
        self.title_fn = title_fn
        if render_fn is None:

            def render_fn(field):
                return "".join(str(sub) for sub in field)

        self.render_fn = render_fn

    def __call__(self, field, **kwargs):
        html = []
        kwargs.setdefault("id", field.id)
        html.append("<div class='card' %s>" % html_params(**kwargs))
        html.append("<div class='card-body'>")
        if self.title_fn:
            html.append(f"<h5 class='card-title'>{self.title_fn(field)}</h5>")
        html.append(self.render_fn(field))
        html.append("</div></div>")
        return Markup("".join(html))


class AccordianWidget:
    def __init__(self, label_fn=None, *args, **kwargs):
        self.label_fn = label_fn or (lambda f: f.label.text)

    def __call__(self, field, **kwargs):
        html = []
        id_ = field.id
        kwargs.setdefault("id", id_)
        html.append("<div class='accordion' %s>" % html_params(**kwargs))
        html.append("<div class='card'>")
        html.append(f"<div class='card-header' id='heading-{id_}'>")
        html.append("<h2 class='mb-0'>")
        html.append(
            "<button {}>{}</button></h2></div>".format(
                html_params(
                    **{
                        "class": "btn btn-link",
                        "type": "button",
                        "data-toggle": "collapse",
                        "data-target": f"#collapse-{id_}",
                        "aria-expanded": "false",
                        "aria-controls": f"collapse-{id_}",
                    }
                ),
                field.label.text,
            )
        )
        html.append(
            "<div {}>".format(
                html_params(
                    **{
                        "id": f"collapse-{id_}",
                        "class": "collapse",
                        "aria-labelledby": f"heading-{id_}",
                        "data-parent": id_,
                    }
                )
            )
        )
        html.append(
            "<div class='card-body'>{}</div></div></div></div>".format(
                "".join(str(f) for f in field)
            )
        )

        return Markup("".join(html))


class StringField(__wtf.StringField):
    widget = TextInput()


class SelectField(__wtf.SelectField):
    widget = Select()


class SelectMultipleField(__wtf.SelectMultipleField):
    widget = Select(multiple=True)


class RadioField(__wtf.RadioField):
    option_widget = RadioInput()


class IntegerField(__wtf.IntegerField):
    widget = TextInput()


class DecimalField(__wtf.DecimalField):
    widget = TextInput()


class FloatField(__wtf.FloatField):
    widget = TextInput()


class BooleanField(__wtf.BooleanField):
    widget = CheckboxInput()


class DateTimeField(__wtf.DateTimeField):
    widget = TextInput()


class DateField(__wtf.DateField):
    widget = TextInput()


class TimeField(__wtf.TimeField):
    widget = TextInput()


class SubmitField(__wtf.SubmitField):
    widget = SubmitInput()


class QuerySelectField(__wtfa.QuerySelectField):
    widget = Select()


class FormField(__wtf.FormField):
    widget = CardWidget()


class FieldList(__wtf.FieldList):
    widget = AccordianWidget()
