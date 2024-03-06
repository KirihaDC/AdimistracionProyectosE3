from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator, RegexValidator

curp_validador = RegexValidator(
    regex='^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$',
    message='El CURP no tiene un formato válido',
    code='curp_invalido'
)


documentos_validador = FileExtensionValidator(
    allowed_extensions=['pdf'],
    message="Sólo se permiten Documentos PDF"
)

imagen_validador = FileExtensionValidator(
    allowed_extensions=['png','jpg'],
    message="Sólo se permiten imágenes PNG"
)