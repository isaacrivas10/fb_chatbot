
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, MultipleFileField, BooleanField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from store.models.logic import Category, Brand, get_name_tuple


datarequired= DataRequired('Por favor llenar este campo')

class ProductForm(FlaskForm):

    imgs= MultipleFileField(label='Imagenes', validators=[datarequired, FileAllowed(['jpg','png','jpeg'])])
    name= StringField('Nombre de Producto', validators=[datarequired, Length(min=4, max=20)])
    brand= SelectField('Marca', validators=[datarequired])
    category= SelectField('Categoria', validators=[datarequired])
    is_available= BooleanField('Disponible', default='checked')
    price= DecimalField('Precio', places=2, validators=[datarequired])
    discount= BooleanField('Esta en descuento?')
    discount_price= DecimalField('Descuento', places=2, validators=[datarequired])
    productStatus= SelectField('Estado',
    choices=[
        ('1', 'Nuevo'),
        ('2', 'Semi Nuevo'),
        ('3', 'Usado'),
        ('4', 'Reparado'),
        ('5', 'Repuestos')
        ], validators=[datarequired])
    delivery= SelectField('Entrega',
        choices=[('1', 'Digital'),
            ('2', 'Fisica')
            ], validators=[datarequired])
    description= TextAreaField('Descripcion del Producto', validators=[datarequired])
    save= SubmitField('Guardar Producto')
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.brand.choices= get_name_tuple(Brand)
        self.category.choices= get_name_tuple(Category)

