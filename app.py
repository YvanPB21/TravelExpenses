"""
Aplicación Flask para división de gastos grupales
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
    """Página principal"""
    totals = calculator.calculate_totals()
    grand_total = calculator.get_grand_total()

    return render_template(
        'index.html',
        persons=data_store.persons,
        items=data_store.items,
        shared_costs=data_store.shared_costs,
        totals=totals,
        grand_total=grand_total
    )


# Rutas para personas
@app.route('/person/add', methods=['POST'])
def add_person():
    """Agregar una persona"""
    name = request.form.get('name', '').strip()
    if name:
        data_store.add_person(name)
    return redirect(url_for('index'))


@app.route('/person/remove/<int:person_id>', methods=['POST'])
def remove_person(person_id):
    """Eliminar una persona"""
    data_store.remove_person(person_id)
    return redirect(url_for('index'))


# Rutas para ítems
@app.route('/item/add', methods=['POST'])
def add_item():
    """Agregar un ítem"""
    name = request.form.get('name', '').strip()
    cost = request.form.get('cost', 0)

    try:
        cost = float(cost)
        if name and cost > 0:
            data_store.add_item(name, cost)
    except ValueError:
        pass

    return redirect(url_for('index'))


@app.route('/item/remove/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    """Eliminar un ítem"""
    data_store.remove_item(item_id)
    return redirect(url_for('index'))


@app.route('/item/toggle', methods=['POST'])
def toggle_item_person():
    """Alternar la participación de una persona en un ítem"""
    data = request.get_json()
    item_id = data.get('item_id')
    person_id = data.get('person_id')

    if item_id and person_id:
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
    name = request.form.get('name', '').strip()
    cost = request.form.get('cost', 0)

    try:
        cost = float(cost)
        if name and cost > 0:
            data_store.add_shared_cost(name, cost)
    except ValueError:
        pass

    return redirect(url_for('index'))


@app.route('/shared/remove/<int:shared_cost_id>', methods=['POST'])
def remove_shared_cost(shared_cost_id):
    """Eliminar un costo compartido"""
    data_store.remove_shared_cost(shared_cost_id)
    return redirect(url_for('index'))


# Ruta para limpiar todo
@app.route('/clear', methods=['POST'])
def clear_all():
    """Limpiar todos los datos"""
    data_store.clear_all()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

