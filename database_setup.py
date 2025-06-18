import pymysql

def get_db_connection():
    """
    Establish database connection
    """
    connection = pymysql.connect(
        host='localhost',
        user='root',      
        password='root',  
        database='utility_db',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def create_database_tables():
    """
    Create necessary tables for the utility management project
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Services Categories Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT
    )
    ''')

    # Services Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category_id INT,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        cost DECIMAL(10,2),
        image_path VARCHAR(255),
        FOREIGN KEY (category_id) REFERENCES service_categories(id)
    )
    ''')

    # Service Providers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_providers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        phone VARCHAR(20),
        specialization VARCHAR(100)
    )
    ''')

    # Customer Service Requests Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        service_id INT,
        service_provider_id INT,
        customer_name VARCHAR(100),
        contact_info VARCHAR(100),
        request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending',
        FOREIGN KEY (service_id) REFERENCES services(id),
        FOREIGN KEY (service_provider_id) REFERENCES service_providers(id)
    )
    ''')

    # Insert initial data for service categories
    categories = [
        ('Cleaning', 'Home and office cleaning services'),
        ('Appliances Repair', 'Repair services for household appliances'),
        ('Plumbing and Electrical', 'Comprehensive repair and maintenance services'),
        ('Painting', 'Interior and exterior painting services')
    ]

    cursor.executemany(
        'INSERT INTO service_categories (name, description) VALUES (%s, %s)', 
        categories
    )

    # Insert initial services
    services = [
        (1, 'Home Cleaning', 'Thorough home cleaning service', 50.00, '/static/images/cleaning_services/image1.jpg', 1),
        (1, 'Office Cleaning', 'Professional office space cleaning', 75.00, '/static/images/cleaning_services/image2.jpg', 1),
        (2, 'Refrigerator Repair', 'Diagnosis and repair of refrigerators', 100.00, '/static/images/appliance_repair/image3.jpg', 2),
        (2, 'Washing Machine Repair', 'Comprehensive washing machine service', 85.00, '/static/images/appliance_repair/image4.jpg', 2),
        (3, 'Electrical Wiring', 'Complete electrical system checkup', 120.00, '/static/images/plumbing_electrical/image5.jpg', 3),
        (3, 'Plumbing Maintenance', 'Comprehensive plumbing services', 90.00, '/static/images/plumbing_electrical/image6.jpg', 3),
        (4, 'Interior Painting', 'Professional interior wall painting', 200.00, '/static/images/painting/image7.jpg', 3),
        (4, 'Exterior Painting', 'Comprehensive exterior painting service', 350.00, '/static/images/painting/image8.jpg', 3)
    ]
    
    
    
    
    cursor.executemany(
        'INSERT INTO services (category_id, name, description, cost, image_path, provider_id) VALUES (%s, %s, %s, %s, %s, %s)', 
        services
    )

    # Insert initial service providers
    providers = [
        ('Clean Masters', 'clean.masters@example.com', '1234567890', 'Cleaning Services'),
        ('Quick Repair', 'quick.repair@example.com', '9876543210', 'Appliances and Electronics'),
        ('Home Solutions', 'home.solutions@example.com', '5555555555', 'Plumbing, Electrical, and Painting')
     ]

    cursor.executemany(
        'INSERT INTO service_providers (name, email, phone, specialization) VALUES (%s, %s, %s, %s)', 
        providers
    )

    connection.commit()
    cursor.close()
    connection.close()

# Call this function to set up the database
if __name__ == '__main__':
    create_database_tables()