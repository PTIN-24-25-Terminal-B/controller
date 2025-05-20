# Gestió de Cotxes - Documentació de Funcions (Redis)

Aquest fitxer documenta les funcions relacionades amb la gestió de cotxes en una API REST utilitzant Redis com a base de dades. Les funcions realitzen operacions CRUD sobre dades emmagatzemades en claus Redis amb el format `car:{id}`.

---

## `get_car(car_id: str)`

**Propòsit**: Obtenir les dades d'un cotxe específic pel seu ID.  

**Paràmetres**:
- `car_id` (str): ID únic del cotxe (emmagatzemat com a string).

**Funcionament**:
1. Connexió a Redis:  
   ```python
   r = redis.Redis(host='localhost', port=6379, db=0)
   ```
2. Cerca el cotxe a Redis amb la clau `car:{car_id}`:  
   ```python
   car_data = redis_conn.get(key)
   ```
3. Si no es troba (`if not car_data`), llança un error HTTP 404.
4. Converteix les dades JSON a un objecte `Car` amb els models `Point` i `Path`.
5. Retorna les dades del cotxe en format JSON.

**Exemple de Resposta**:
```json
{
    "id": "car1",
    "batery": 85.5,
    "position": {"x": 10, "y": 20},
    "working": true,
    "currentPath": {
        "id": "path1",
        "points": [{"x": 10, "y": 20}, {"x": 30, "y": 40}]
    }
}
```

---

## `get_all_cars()`

**Propòsit**: Llistar tots els cotxes disponibles a Redis.  

**Funcionament**:
1. Connexió a Redis.
2. Obté totes les claus amb el patró `car:*`:  
   ```python
   car_keys = redis_conn.keys("car:*")
   ```
3. Converteix cada entrada de Redis a un objecte `Car` i retorna una llista de diccionaris.

**Exemple de Resposta**:
```json
{
    "cars": [
        {
            "id": "car1",
            "batery": 85.5,
            "position": {"x": 10, "y": 20},
            "working": true,
            "currentPath": null
        },
        {
            "id": "car2",
            "batery": 70.0,
            "position": {"x": 5, "y": 5},
            "working": false,
            "currentPath": {
                "id": "path2",
                "points": [{"x": 5, "y": 5}, {"x": 15, "y": 15}]
            }
        }
    ]
}
```

---

## `edit_car(car_id: str, update_data: dict)`

**Propòsit**: Actualitzar camps específics d'un cotxe (operació PUT).  

**Diferències amb l'exemple original**:
- Utilitza PUT però permet actualitzacions parcials (com PATCH).
- No requereix tots els camps.

**Validacions**:
- Només permet camps: `batery`, `position`, `working`, `currentPath`.
- Verifica que el cotxe existeix abans d'actualitzar (error 404 si no es troba).

**Funcionament**:
1. Connexió a Redis.
2. Parseja les dades d'entrada:
   - `position`: Converteix el diccionari a objecte `Point`.
   - `currentPath`: Converteix el diccionari a objecte `Path`.
3. Actualitza el cotxe amb `modifyCar()`.
4. Desa els canvis a Redis amb `save_car()`.

**Exemple d'Ús**:
```python
edit_car("car1", {
    "batery": 90.0,
    "position": {"x": 15, "y": 25},
    "working": false
})
```

**Exemple de Resposta**:
```json
{
    "id": "car1",
    "batery": 90.0,
    "position": {"x": 15, "y": 25},
    "working": false,
    "currentPath": null
}
```

---

## `delete_car(car_id: str)`

**Propòsit**: Eliminar un cotxe de Redis.  

**Funcionament**:
1. Connexió a Redis.
2. Intenta esborrar la clau `car:{car_id}`.
3. Si la clau no existeix (`deleted_count == 0`), llança error 404.

**Exemple de Resposta**:
```json
{
    "message": "Car deleted successfully"
}
```

---

## Models Utilitzats

### `Point`
- **Camps**:
  - `x` (float o int): Coordenada X.
  - `y` (float o int): Coordenada Y.

### `Path`
- **Camps**:
  - `id` (str): ID del trajecte.
  - `path` (llista de `Point`): Llista de punts que defineixen el trajecte.

---

## Errors Comuns

- **404 Not Found**: 
  - Quan no es troba un cotxe amb l'ID proporcionat.
  - Quan no hi ha cotxes registrats (`get_all_cars` retorna llista buida).
  
- **400 Bad Request**: 
  - S'inclouen camps no permesos a `edit_car`.
  
- **500 Internal Server Error**: 
  - Errors de connexió amb Redis.
  - Errors inesperats durant el processament.
