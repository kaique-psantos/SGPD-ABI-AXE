from django.test import TestCase


# import MySQLdb

# connection = MySQLdb.connect(
#     host='localhost',
#     user='root',
#     passwd='root',
#     db='sgpd_abiaxe',
#     port=3306
# )

# cursor = connection.cursor()
# cursor.execute("SELECT 1")
# result = cursor.fetchone()
# print(result)  # Deve imprimir (1,)
# cursor.close()
# connection.close()

import os
from django.conf import settings  # Certifique-se de que o settings está disponível

# Defina o caminho do arquivo .jasper corretamente
jasper_file = os.path.join(settings.MEDIA_ROOT, 'reports', 'Oficio.jasper')

# Verifique se o arquivo existe
print(os.path.exists(jasper_file))  # Deve retornar True se o arquivo existir

