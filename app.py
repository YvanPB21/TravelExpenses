"""
Aplicación Flask para división de gastos grupales con soporte para múltiples viajes
"""
import sys
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import DataStore
from calculator import BillCalculator
from db.firebase_client import FirebaseConfig

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Configurar Firebase
firebase_config = None
credentials_file = 'firebase-credentials.json'
if os.path.exists(credentials_file):
    # Solo usar database_id si está explícitamente configurado en variable de entorno
    # Por defecto usará "(default)" que es la base de datos estándar de Firebase
    database_id = os.getenv('FIRESTORE_DATABASE_ID')  # None si no está configurado
    firebase_config = FirebaseConfig(
        credentials_path=credentials_file,
        database_id=database_id
    )

# Almacenamiento en memoria
data_store = DataStore(firebase_config=firebase_config)
calculator = BillCalculator(data_store)


@app.route('/')
def index():
    """Página principal - lista de viajes"""
    return render_template(
        'trips.html',
        trips=data_store.trips
    )


@app.route('/trip/<int:trip_id>')
def trip_detail(trip_id):
    """Vista de detalle de un viaje específico"""
    if not data_store.set_current_trip(trip_id):
        return redirect(url_for('index'))

    current_trip = data_store.get_trip(trip_id)
    if not current_trip:
        return redirect(url_for('index'))

    totals = calculator.calculate_totals()
    grand_total = calculator.get_grand_total()
    summary = calculator.get_summary()
    payments_summary = calculator.calculate_payments_summary()

    # Organizar datos por día
    days_data = []
    for day in range(1, current_trip.days + 1):
        day_items = data_store.get_items_by_day(day)
        day_totals = calculator.calculate_totals_by_day(day)
        day_total = calculator.get_day_total(day)

        days_data.append({
            'day_number': day,
            'day_items': day_items,
            'day_totals': day_totals,
            'day_total': day_total
        })

    return render_template(
        'trip_detail.html',
        current_trip=current_trip,
        persons=data_store.persons,
        shared_costs=data_store.shared_costs,
        totals=totals,
        grand_total=grand_total,
        summary=summary,
        payments_summary=payments_summary,
        days_data=days_data
    )


# Rutas para viajes
@app.route('/trip/add', methods=['POST'])
def add_trip():
    """Crear un nuevo viaje"""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    days = request.form.get('days', 1)

    try:
        days = int(days)
        if days < 1:
            days = 1
    except ValueError:
        days = 1

    if name:
        trip = data_store.add_trip(name, description, days)
        return redirect(url_for('trip_detail', trip_id=trip.id))
    return redirect(url_for('index'))


@app.route('/trip/remove/<int:trip_id>', methods=['POST'])
def remove_trip(trip_id):
    """Eliminar un viaje"""
    data_store.remove_trip(trip_id)
    return redirect(url_for('index'))


# Rutas para personas
@app.route('/person/add', methods=['POST'])
def add_person():
    """Agregar una persona"""
    trip_id = request.form.get('trip_id')
    name = request.form.get('name', '').strip()
    if name and trip_id:
        data_store.set_current_trip(int(trip_id))
        data_store.add_person(name)
        return redirect(url_for('trip_detail', trip_id=trip_id))
    return redirect(url_for('index'))


@app.route('/person/remove/<int:trip_id>/<int:person_id>', methods=['POST'])
def remove_person(trip_id, person_id):
    """Eliminar una persona"""
    data_store.set_current_trip(trip_id)
    data_store.remove_person(person_id)
    return redirect(url_for('trip_detail', trip_id=trip_id))


# Rutas para ítems
@app.route('/item/add', methods=['POST'])
def add_item():
    """Agregar un ítem"""
    trip_id = request.form.get('trip_id')
    name = request.form.get('name', '').strip()
    quantity = request.form.get('quantity', 1)
    unit_price = request.form.get('unit_price', 0)
    day = request.form.get('day', 1)
    url = request.form.get('url', '').strip()
    paid_by = request.form.get('paid_by_person_id')

    try:
        quantity = int(quantity)
        unit_price = float(unit_price)
        day = int(day)
        paid_by_person_id = int(paid_by) if paid_by else None

        if name and quantity > 0 and unit_price > 0 and trip_id and day > 0:
            data_store.set_current_trip(int(trip_id))
            data_store.add_item(name, quantity, unit_price, day, url, paid_by_person_id)
            return redirect(url_for('trip_detail', trip_id=trip_id))
    except ValueError:
        pass

    return redirect(url_for('index'))


@app.route('/item/remove/<int:trip_id>/<int:item_id>', methods=['POST'])
def remove_item(trip_id, item_id):
    """Eliminar un ítem"""
    data_store.set_current_trip(trip_id)
    data_store.remove_item(item_id)
    return redirect(url_for('trip_detail', trip_id=trip_id))


@app.route('/item/update/<int:trip_id>/<int:item_id>', methods=['POST'])
def update_item(trip_id, item_id):
    """Actualizar un ítem"""
    data_store.set_current_trip(trip_id)

    name = request.form.get('name', '').strip()
    quantity = request.form.get('quantity')
    unit_price = request.form.get('unit_price')
    day = request.form.get('day')
    url = request.form.get('url', '').strip()
    paid_by = request.form.get('paid_by_person_id')

    try:
        quantity = int(quantity) if quantity else None
        unit_price = float(unit_price) if unit_price else None
        day = int(day) if day else None
        paid_by_person_id = int(paid_by) if paid_by else None

        data_store.update_item(item_id, name=name, quantity=quantity,
                              unit_price=unit_price, day=day, url=url,
                              paid_by_person_id=paid_by_person_id)
    except ValueError:
        pass

    return redirect(url_for('trip_detail', trip_id=trip_id))


@app.route('/item/toggle', methods=['POST'])
def toggle_item_person():
    """Alternar la participación de una persona en un ítem"""
    data = request.get_json()
    item_id = data.get('item_id')
    person_id = data.get('person_id')
    trip_id = data.get('trip_id')

    if item_id and person_id and trip_id:
        data_store.set_current_trip(int(trip_id))
        success = data_store.toggle_person_for_item(int(item_id), int(person_id))
        if success:
            # Calcular todos los totales actualizados
            current_trip = data_store.get_trip(int(trip_id))
            totals = calculator.calculate_totals()
            grand_total = calculator.get_grand_total()
            summary = calculator.get_summary()

            # Totales por día
            days_totals = {}
            for day in range(1, current_trip.days + 1):
                day_totals = calculator.calculate_totals_by_day(day)
                day_total = calculator.get_day_total(day)
                days_totals[day] = {
                    'totals': {str(p.id): {'items_total': day_totals[p.id]['items_total'],
                                           'shared_total': day_totals[p.id]['shared_total'],
                                           'total': day_totals[p.id]['total']}
                              for p in data_store.persons},
                    'day_total': day_total
                }

            return jsonify({
                'success': True,
                'totals': {str(p.id): {'items_total': totals[p.id]['items_total'],
                                       'shared_total': totals[p.id]['shared_total'],
                                       'total': totals[p.id]['total']}
                          for p in data_store.persons},
                'grand_total': grand_total,
                'summary': summary,
                'days_totals': days_totals
            })

    return jsonify({'success': False}), 400


# Rutas para costos compartidos
@app.route('/shared/add', methods=['POST'])
def add_shared_cost():
    """Agregar un costo compartido"""
    trip_id = request.form.get('trip_id')
    name = request.form.get('name', '').strip()
    cost = request.form.get('cost', 0)
    paid_by_person_ids = request.form.getlist('paid_by_person_ids[]')

    try:
        cost = float(cost)
        # Convertir paid_by_person_ids a lista de enteros
        paid_by_person_ids = [int(pid) for pid in paid_by_person_ids if pid]
        
        if name and cost > 0 and trip_id:
            data_store.set_current_trip(int(trip_id))
            data_store.add_shared_cost(name, cost, paid_by_person_ids)
            return redirect(url_for('trip_detail', trip_id=trip_id))
    except ValueError:
        pass

    return redirect(url_for('index'))


@app.route('/shared/update/<int:trip_id>/<int:shared_cost_id>', methods=['POST'])
def update_shared_cost(trip_id, shared_cost_id):
    """Actualizar un costo compartido"""
    data_store.set_current_trip(trip_id)

    name = request.form.get('name', '').strip()
    cost = request.form.get('cost')
    paid_by_person_ids = request.form.getlist('paid_by_person_ids[]')

    try:
        cost = float(cost) if cost else None
        # Convertir paid_by_person_ids a lista de enteros
        paid_by_person_ids = [int(pid) for pid in paid_by_person_ids if pid] if paid_by_person_ids else None

        data_store.update_shared_cost(shared_cost_id, name=name, cost=cost,
                                     paid_by_person_ids=paid_by_person_ids)
    except ValueError:
        pass

    return redirect(url_for('trip_detail', trip_id=trip_id))


@app.route('/shared/remove/<int:trip_id>/<int:shared_cost_id>', methods=['POST'])
def remove_shared_cost(trip_id, shared_cost_id):
    """Eliminar un costo compartido"""
    data_store.set_current_trip(trip_id)
    data_store.remove_shared_cost(shared_cost_id)
    return redirect(url_for('trip_detail', trip_id=trip_id))


# Ruta para limpiar todo
@app.route('/clear/<int:trip_id>', methods=['POST'])
def clear_all(trip_id):
    """Limpiar todos los datos del viaje actual"""
    data_store.set_current_trip(trip_id)
    data_store.clear_all()
    return redirect(url_for('trip_detail', trip_id=trip_id))


if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    print(f"Starting Flask server on http://0.0.0.0:{port} (debug={debug_mode})", flush=True)
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
