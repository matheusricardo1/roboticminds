from rolepermissions.roles import AbstractUserRole


class Teacher(AbstractUserRole):
    available_permissions = {'habilitar_conta_aluno': True,
                             'habilitar_conta_professor': True,
                             'habilitar_conta_ajudante': True,
                             'habilitar_certificado': True,
                             'ver_certificado': True}


class Student(AbstractUserRole):
    available_permissions = {'habilitar_conta_aluno': True,
                             'habilitar_conta_professor': True,
                             'habilitar_conta_ajudante': True,
                             'habilitar_certificado': False,
                             'ver_certificado': True}


class Student(AbstractUserRole):
    available_permissions = {'habilitar_conta_aluno': False,
                             'habilitar_conta_ajudante': False,
                             'habilitar_conta_professor': False,
                             'habilitar_certificado': False,
                             'ver_certificado': True}
