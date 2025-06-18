from flask import Flask, render_template, request, redirect, url_for
from database_setup import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customer/services')
def customer_services():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch service categories with their services
    cursor.execute('''
        SELECT sc.id as category_id, sc.name as category_name, 
               s.id as service_id, s.name as service_name, 
               s.description, s.cost, s.image_path
        FROM service_categories sc
        JOIN services s ON sc.id = s.category_id
    ''')
    services = cursor.fetchall()
    
    # Group services by category
    categorized_services = {}
    for service in services:
        if service['category_name'] not in categorized_services:
            categorized_services[service['category_name']] = []
        categorized_services[service['category_name']].append(service)
    
    cursor.close()
    connection.close()
    
    return render_template('customer_services.html', services=categorized_services)

@app.route('/customer/service/<int:service_id>')
def service_details(service_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch detailed service information and available providers
    cursor.execute('''
        SELECT s.*, sc.name as category_name, sp.name as provider_name, sp.id as provider_id
        FROM services s
        JOIN service_categories sc ON s.category_id = sc.id
        JOIN service_providers sp ON sp.specialization LIKE CONCAT('%', sc.name, '%')
        WHERE s.id = %s
    ''', (service_id,))
    service_details = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('service_details.html', service=service_details[0], providers=service_details)

@app.route('/service-provider')
def service_provider():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch service providers with their services and requests
    cursor.execute('''
        SELECT sp.*, s.name as service_name, sr.id as request_id, 
               sr.customer_name, sr.contact_info, sr.request_date, sr.status
        FROM service_providers sp
        LEFT JOIN services s ON sp.specialization LIKE CONCAT('%', s.name, '%')
        LEFT JOIN service_requests sr ON sr.service_provider_id = sp.id
    ''')
    provider_data = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('service_provider.html', providers=provider_data)

@app.route('/book-service', methods=['POST'])
def book_service():
    service_id = request.form['service_id']
    provider_id = request.form['provider_id']
    customer_name = request.form['customer_name']
    contact_info = request.form['contact_info']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO service_requests 
        (service_id, service_provider_id, customer_name, contact_info) 
        VALUES (%s, %s, %s, %s)
    ''', (service_id, provider_id, customer_name, contact_info))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('customer_services'))

if __name__ == '__main__':
    app.run(debug=True)