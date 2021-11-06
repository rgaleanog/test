# Pruebas unitarias en ficheros independientes de los métodos de acceso a la base de datos.

En este directorio se disponibilizan una serie de métodos de acceso a la base de datos de DynamoDB de manera independiente y unas pruebas unitarias asociadas.
Dichas pruebas unitarias ejecutan contra la librería moto y contra una imagen de docker de DynamoDB levantada en un contexto local.

Para poder llevarlas a cabo se han de cumplir los siguientes requisitos:


* Librerías
  * Python3.8
  * boto3==1.16.35
  * moto==1.3.14
  * mock==4.0.3
  * coverage==5.5


* Imagen de Docker

  * DynamoDB oficial de AWS.



Pasos para ejecutar DynamoDB en local

```
docker run -p 8000:8000 amazon/dynamodb-local
```

Pasos para ejecutar las pruebas

```
test$ coverage run -m TestToDo
One or more parameter values are not valid. The AttributeValue for a key attribute cannot contain an empty string value. Key: id
One or more parameter values were invalid: An AttributeValue may not contain an empty string
One or more parameter values were invalid: An AttributeValue may not contain an empty string
One or more parameter values were invalid: An AttributeValue may not contain an empty string
....One or more parameter values are not valid. The AttributeValue for a key attribute cannot contain an empty string value. Key: id
One or more parameter values were invalid: An AttributeValue may not contain an empty string
One or more parameter values were invalid: An AttributeValue may not contain an empty string
.
----------------------------------------------------------------------
Ran 11 tests in 1.947s

OK

test$ coverage report -m
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
TestToDo.py            108      0   100%
ToDoCreateTable.py      11      2    82%   32, 38
ToDoDeleteItem.py       17      1    94%   32
ToDoGetItem.py          17      3    82%   18-19, 31
ToDoListItems.py        17      6    65%   16-17, 23-25, 29
ToDoPutItem.py          19      1    95%   38
ToDoUpdateItem.py       19      1    95%   48
--------------------------------------------------
TOTAL                  208     14    93%
```

# TODO

El alumno deberá de incluir en este directorio un nuevo fichero de pruebas unitarias para la clase que se especifica desarrollar, usando como base las funciones python aquí desarrolladas y las pruebas que se ofrecen a modo de ejemplo. El esqueleto de la clase se encuentra disponible en [todos/todoTableClass.py](/todos/todoTableClass.py)

El fichero de pruebas se denominará:

```
TestToDoTableClass.py
```
