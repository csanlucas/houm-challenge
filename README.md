# houm-challenge

## Problema

En Houm tenemos un gran equipo de Houmers que muestran las propiedades y solucionan todos los problemas que podrían ocurrir en ellas. Ellos son parte fundamental de nuestra operación y de la experiencia que tienen nuestros clientes. Es por esta razón que queremos incorporar ciertas métricas para monitorear cómo operan, mejorar la calidad de servicio y para asegurar la seguridad de nuestros Houmers.

---

## Requisitos
Crear un servicio REST que:

- Permita que la aplicación móvil mande las coordenadas del Houmer
- Para un día retorne todas las coordenadas de las propiedades que visitó y cuanto tiempo se quedó en cada una
- Para un día retorne todos los momentos en que el houmer se trasladó con una velocidad superior a cierto parámetro

---

## Setup for development

Este proyecto se encuentra configurado con Docker y docker-compose, con la finalidad de agilizar un deployment LOCAL para mantener un entorno de desarrollo independiente. Es necesario verificar de tener una instalación de Docker

**1)** Clonar repositorio
```sh
git clone https://github.com/csanlucas/houm-challenge.git
```
**2)** Ingresar a la carpeta del proyecto y ejecutar docker-compose up, este comando realizará la configuración de las imágenes de Docker para backend y para la DB
```sh
cd houm-challenge
docker-compose up
```
**3)** [Optional] Dump data backup para inicializar data de entorno de desarrollo, para ser consultada y realizar operaciones desde los Rest APIs endpoints
```sh
cp init_backup.sql .dbdata/
docker-compose exec db bash
psql houmdb < /var/lib/postgresql/data/init_backup.sql
rm /var/lib/postgresql/data/init_backup.sql
exit
```

---

## Solución planteada y uso
Se realiza el desarrollo de un REST Api haciendo uso del siguiente stack de tecnologías:
    - Python 3.10+
    - Django 3.2.11
    - Django-Rest-Framework 3.13.1

### **Asunciones**
    - Se mantiene un registro de varios Houmers en nuestra base de datos para vincular las diferentes acciones realizadas
    - [En funcionalidad 2] Cuando se registra la ubicación del houmer se puede mantener un proceso que busque las propiedades registradas, en caso de existir una permitida, la aplicación envia un request hacer el registro de visita a la propiedad.
    Luego de existir una variacion de la ubicacion en la app se hace una actualizacion llamando al ENDPOINT para indicar la hora de salida. Por lo que se asume que en este requerimiento ya existen y se encuentran almacenados, los registros de hora y salida de visita a la propiedad.
    - [En funcionalidad 3] Al registrar la ubicación del houmer, tambien existe la posibilidad de registrar la velocidad en la que se traslada, por defecto la velocidad sera 0 en caso de no enviar el parámetro de velocidad. Unidad [km/h]

### **USO**
Se debe realizar los request a los endpoints haciendo uso de algún cliente de HTTP, se recomienda utilizar *Postman*

#### [FUNCIONALIDAD 1] - Permita que la aplicación móvil mande las coordenadas del Houmer
* **URL** : http://localhost:8101/locator/houmer/
* **Method** `POST`
* **Data Params**
    ```json
    {
        "latitude": -2.114880,
        "longitude": -79.968221,
        "houmerId": 1,
        "deviceId": "DVID-TABLET1"
    }
    ```
* **Success Response:**
    * **Code** 200 <br/>
    **Content** 
    ```json
    {
        "id": 7,
        "latitude": -2.11488,
        "longitude": -79.968221,
        "deviceId": "DVID-TABLET1",
        "created_at": "2022-01-27T06:54:38.501648Z",
        "velocity_kmh": 140,
        "houmerId": 1
    }
    ```
---
#### [FUNCIONALIDAD 2] - Para un día retorne todas las coordenadas de las propiedades que visitó y cuanto tiempo se quedó en cada una
* **URL** : http://localhost:8101/locator/property/
* **Method** `GET`
* **URL Params:**

  **Required**
  
  `on_date=[date('YYYY-MM-DD')] & houmer_id=[integer]`

* **Success Response:**
    * **Code** 200 <br/>
    **Content** 
    ```json
    [
        {
            "visited_by": 1,
            "arrive_at": "2022-01-27T03:24:12.864839Z",
            "departure_at": "2022-01-27T06:30:28.618000Z",
            "latitude": -33.456329,
            "longitude": -70.644175,
            "elapsed_time_ms": 11175753,
            "elapsed_time_str": "3:06:15.753161"
        }
    ]
    ```
---
#### [FUNCIONALIDAD 3] - Para un día retorne todos los momentos en que el houmer se trasladó con una velocidad superior a cierto parámetro
* **URL** : http://localhost:8101/locator/houmer/
* **SAMPLE:** http://localhost:8101/locator/houmer/?houmer_id=1&on_date=2022-01-27&velocity_kmh=100
* **Method** `GET`
* **URL Params:**

  **Optional**
  
  `on_date=[date('YYYY-MM-DD')] & velocity_kmh=[integer]`

* **Success Response:**
    * **Code** 200 <br/>
    **Content** 
    ```json
    [
        {
            "id": 5,
            "latitude": -2.11488,
            "longitude": -79.968221,
            "deviceId": "DVID-TABLET1",
            "created_at": "2022-01-27T06:54:26.062454Z",
            "velocity_kmh": 110,
            "houmerId": 1
        },
        {
            "id": 6,
            "latitude": -2.11488,
            "longitude": -79.968221,
            "deviceId": "DVID-TABLET1",
            "created_at": "2022-01-27T06:54:31.585970Z",
            "velocity_kmh": 115,
            "houmerId": 1
        },
        {
            "id": 7,
            "latitude": -2.11488,
            "longitude": -79.968221,
            "deviceId": "DVID-TABLET1",
            "created_at": "2022-01-27T06:54:38.501648Z",
            "velocity_kmh": 140,
            "houmerId": 1
        }
    ]
    ```
---
