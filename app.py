"""
Aplicación Flask para división de gastos grupales con soporte para múltiples viajes
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import DataStore
from calculator import BillCalculator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Almacenamiento en memoria
data_store = DataStore()
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

    totals = calculator.calculate_totals()
    grand_total = calculator.get_grand_total()
    current_trip = data_store.get_trip(trip_id)

    return render_template(
        'trip_detail.html',
        current_trip=current_trip,
        persons=data_store.persons,
        items=data_store.items,
        shared_costs=data_store.shared_costs,
        totals=totals,
        grand_total=grand_total
    )


# Rutas para viajes
@app.route('/trip/add', methods=['POST'])
def add_trip():
    """Crear un nuevo viaje"""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    if name:
        trip = data_store.add_trip(name, description)
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
    url = request.form.get('url', '').strip()

    try:
        quantity = int(quantity)
        unit_price = float(unit_price)
        if name and quantity > 0 and unit_price > 0 and trip_id:
            data_store.set_current_trip(int(trip_id))
            data_store.add_item(name, quantity, unit_price, url)
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
            totals = calculator.calculate_totals()
            return jsonify({
                'success': True,
                'totals': totals
            })

    return jsonify({'success': False}), 400


# Rutas para costos compartidos
@app.route('/shared/add', methods=['POST'])
def add_shared_cost():
    """Agregar un costo compartido"""
    trip_id = request.form.get('trip_id')
    name = request.form.get('name', '').strip()
    cost = request.form.get('cost', 0)

    try:
        cost = float(cost)
        if name and cost > 0 and trip_id:
            data_store.set_current_trip(int(trip_id))
            data_store.add_shared_cost(name, cost)
            return redirect(url_for('trip_detail', trip_id=trip_id))
    except ValueError:
        pass

    return redirect(url_for('index'))


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
    print("Starting Flask server on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

