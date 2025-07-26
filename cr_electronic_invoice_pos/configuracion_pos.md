
<a href="buymeacoffee.com/jartavia05" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" height="41" width="174"></a>

 
[![AGPL License](https://img.shields.io/badge/license-AGPL--3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0-standalone.html)


# Configuración del POS para Odoo versión 17.

## 1. Configuración de las secuencias

Ir a Ajustes - Técnico - Secuencias

* Crear una secuencia para cada terminal del punto de venta (caja)
* Nombre de la secuencia + POS 001 (terminando con el terminal para crear una secuencia unica)
* código de la secuencia: sequence.FE.pos.001
* Tamaño de la secuencia: 10
* Siguiente número: Asignar la numeracion de Facturacion Elctronica.
* Todos los demás campos se dejan como están


## 2. Configuración de los Diarios

Vamos a configurar un diario de ventas para la facturación. Se crea un diario por punto de venta.

Ir a Contabilidad - Configuración - Diarios

* Crear un diario para cada punto de venta.
* Nombre corto: F2001 (F+Sucursal+Terminal)
* Ir a la pestaña Factura Electronica y seleccionar las secuencias creadas en el paso anterior
* Asignar numero de Sucursal y Terminal según corresponda.

## 3. Configuración del Punto de Venta

Ir a Punto de Venta - Configuración 

* Configurar los metodos de pago.
* Seleccionar el "Método de pago contable" que corresponda. (Efectivo, Tarjeta, Sinpe)
* Configurar el impuesto de venta predeterminado.
* Seleccionar el diario para facturas. (diario creado en el paso 1)
* Seleccionar cliente predeterminado.
* Modificar el diario de la sesion para que coincida con el nombre del Punto de Venta.


## PARA EMITIR FACTURA ELECTRONICA: 

Para poder emitir una Factura electrónica se deben cumplir con los siguientes requisitos:

* El cliente debe estar Inscrito. (Se actualiza con el modulo hacienda_info_query)
* El cliente debe tener configuradas las actividades economicas prederterminadas.

En caso contrario, el sistema creará un tiquete electrónico.

Créditos
-------
* Autor: Jose Artavia
* Contacto: jartavia05@gmail.com


Bug Tracker
-----------
Todos los errores y mejoras se están registrando en [Github Issues](https://github.com/OdooFeCR/FE-CR/issues). En caso de problemas, por favor verifique primero si su problema ya ha sido registrado previamente y cual es el estado.

Agradecemos todos los aportes para que este proyecto siga evolucionando. 💙
