# This script is created to validate the data and is designed to be used in the notebook file
# That means it follows the business logic and the data validation is done in the notebook file 

# 1. Check if the data is complete
# 2. Check if the data is correct
# 3. Check if the data is consistent

import pandas as pd

def validate_id(data):
    """
    Validate that for every unique 'id', the corresponding 'delivery_person_id' is the same,
    and vice versa.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'id' and 'delivery_person_id'.

    Returns:
        list: A list of discrepancies found, if any.
    """
    discrepancies = []

    # Check if the required columns exist
    if 'id' not in data.columns or 'delivery_person_id' not in data.columns:
        raise ValueError("The DataFrame must contain 'id' and 'delivery_person_id' columns.")

    # Group by 'id' and check if all 'delivery_person_id' are the same
    id_groups = data.groupby('id')['delivery_person_id'].nunique()
    for id_value, count in id_groups.items():
        if count > 1:
            discrepancies.append(f"ID {id_value} has multiple delivery_person_ids.")

    # Group by 'delivery_person_id' and check if all 'id' are the same
    delivery_person_groups = data.groupby('delivery_person_id')['id'].nunique()
    for delivery_person_id, count in delivery_person_groups.items():
        if count > 1:
            discrepancies.append(f"Delivery Person ID {delivery_person_id} has multiple ids.")

    return discrepancies

def validate_delivery_person_id(data):
    """
    Validate IDs and return the results as a list.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'id' and 'delivery_person_id'.

    Returns:
        list: A list containing validation messages.
    """
    issues = validate_id(data)
    if not issues:
        return ["Validation passed: All IDs and delivery_person_ids are consistent."]
    else:
        return ["Validation failed. Issues found:"] + issues

def validate_delivery_person_age(data):
    """
    Validate that the same delivery_person_id has the same delivery_person_age.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'delivery_person_id' and 'delivery_person_age'.

    Returns:
        dict: A dictionary with delivery_person_id as keys and lists of different ages as values.
    """
    discrepancies = {}

    # Check if the required columns exist
    if 'delivery_person_id' not in data.columns or 'delivery_person_age' not in data.columns:
        raise ValueError("The DataFrame must contain 'delivery_person_id' and 'delivery_person_age' columns.")

    # Group by 'delivery_person_id' and collect unique ages
    age_groups = data.groupby('delivery_person_id')['delivery_person_age'].unique()

    # Check for discrepancies
    for delivery_person_id, ages in age_groups.items():
        if len(ages) > 1:  # More than one unique age
            discrepancies[delivery_person_id] = ages.tolist()  # Convert to list for easier readability

    return discrepancies

def validate_delivery_time(data):
    """
    Validate that delivery times are non-negative and within a reasonable range.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'delivery_time'.

    Returns:
        list: A list of discrepancies found, if any.
    """
    discrepancies = []
    if 'delivery_time' not in data.columns:
        raise ValueError("The DataFrame must contain 'delivery_time' column.")

    # Check for negative delivery times
    negative_times = data[data['delivery_time'] < 0]
    if not negative_times.empty:
        discrepancies.append("Negative delivery times found.")

    # Check for delivery times that are too high (e.g., over 120 minutes)
    high_times = data[data['delivery_time'] > 120]
    if not high_times.empty:
        discrepancies.append("Delivery times exceeding 120 minutes found.")

    return discrepancies # adjust this return to be concise and readable after testing
                 

def validate_delivery_person_rating(data):
    """
    Validate that delivery_person_rating is within a valid range and consistent for each delivery_person_id.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'delivery_person_id' and 'delivery_person_rating'.

    Returns:
        str: A message indicating the validation results.
    """
    discrepancies = {}

    # Check if the required columns exist
    if 'delivery_person_id' not in data.columns or 'delivery_person_rating' not in data.columns:
        raise ValueError("The DataFrame must contain 'delivery_person_id' and 'delivery_person_rating' columns.")

    # Check for valid rating range
    invalid_ratings = data[(data['delivery_person_rating'] < 1) | (data['delivery_person_rating'] > 5)]
    if not invalid_ratings.empty:
        for _, row in invalid_ratings.iterrows():
            discrepancies.setdefault(row['delivery_person_id'], []).append(f"Invalid rating: {row['delivery_person_rating']}")

    # Check for consistency of ratings
    rating_groups = data.groupby('delivery_person_id')['delivery_person_rating'].unique()
    for delivery_person_id, ratings in rating_groups.items():
        if len(ratings) > 1:  # More than one unique rating
            discrepancies.setdefault(delivery_person_id, []).append(f"Inconsistent ratings: {ratings.tolist()}")

    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in delivery person ratings:\n"
        for delivery_person_id, issues in discrepancies.items():
            result_message += f"Delivery Person ID {delivery_person_id} has issues: {issues}\n"
    else:
        result_message = "All delivery_person_ids have valid and consistent ratings."

    return result_message

def validate_restaurant_coordinate(data):
    """
    Validate that restaurant_latitude and restaurant_longitude are within valid ranges
    and consistent for each restaurant_id.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'restaurant_id', 'restaurant_latitude', and 'restaurant_longitude'.

    Returns:
        dict: A dictionary with restaurant_id as keys and lists of issues as values.
    """
    discrepancies = {}

    # Check if the required columns exist
    if 'restaurant_id' not in data.columns or 'restaurant_latitude' not in data.columns or 'restaurant_longitude' not in data.columns:
        raise ValueError("The DataFrame must contain 'restaurant_id', 'restaurant_latitude', and 'restaurant_longitude' columns.")

    # Check for valid latitude range
    invalid_latitudes = data[(data['restaurant_latitude'] < -90) | (data['restaurant_latitude'] > 90)]
    if not invalid_latitudes.empty:
        for _, row in invalid_latitudes.iterrows():
            discrepancies.setdefault(row['restaurant_id'], []).append(f"Invalid latitude: {row['restaurant_latitude']}")

    # Check for valid longitude range
    invalid_longitudes = data[(data['restaurant_longitude'] < -180) | (data['restaurant_longitude'] > 180)]
    if not invalid_longitudes.empty:
        for _, row in invalid_longitudes.iterrows():
            discrepancies.setdefault(row['restaurant_id'], []).append(f"Invalid longitude: {row['restaurant_longitude']}")

    # Check for consistency of coordinates
    coordinate_groups = data.groupby('restaurant_id')[['restaurant_latitude', 'restaurant_longitude']].unique()
    for restaurant_id, coords in coordinate_groups.iterrows():
        if len(coords) > 1:  # More than one unique coordinate pair
            discrepancies.setdefault(restaurant_id, []).append(f"Inconsistent coordinates: {coords.tolist()}")

    return discrepancies

def validate_delivery_location_coordinate(data):
    """
    Validate that delivery_location_latitude and delivery_location_longitude are within valid ranges
    and consistent for each delivery_location_id.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'delivery_location_id', 'delivery_location_latitude', and 'delivery_location_longitude'.

    Returns:
        dict: A dictionary with delivery_id as keys and lists of issues as values.
    """
    discrepancies = {}

    # Check if the required columns exist
    if 'delivery_location_id' not in data.columns or 'delivery_location_latitude' not in data.columns or 'delivery_location_longitude' not in data.columns:
        raise ValueError("The DataFrame must contain 'delivery_location_id', 'delivery_location_latitude', and 'delivery_location_longitude' columns.")

    # Check for valid latitude range
    invalid_latitudes = data[(data['delivery_location_latitude'] < -90) | (data['delivery_location_latitude'] > 90)]
    if not invalid_latitudes.empty:
        for _, row in invalid_latitudes.iterrows():
            discrepancies.setdefault(row['delivery_location_id'], []).append(f"Invalid latitude: {row['delivery_location_latitude']}")

    # Check for valid longitude range
    invalid_longitudes = data[(data['delivery_location_longitude'] < -180) | (data['delivery_location_longitude'] > 180)]
    if not invalid_longitudes.empty:
        for _, row in invalid_longitudes.iterrows():
            discrepancies.setdefault(row['delivery_location_id'], []).append(f"Invalid longitude: {row['delivery_location_longitude']}")

    # Check for consistency of coordinates
    coordinate_groups = data.groupby('delivery_location_id')[['delivery_location_latitude', 'delivery_location_longitude']].unique()
    for delivery_location_id, coords in coordinate_groups.iterrows():
        if len(coords) > 1:  # More than one unique coordinate pair
            discrepancies.setdefault(delivery_location_id, []).append(f"Inconsistent coordinates: {coords.tolist()}")

    return discrepancies

def validate_order_date(data):
    """
    Validate that order_date is in a valid format, complete, and logically consistent.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'order_date'.

    Returns:
        dict: A dictionary with issues found related to order_date.
    """
    discrepancies = {}

    # Check if the required column exists
    if 'order_date' not in data.columns:
        raise ValueError("The DataFrame must contain 'order_date' column.")

    # Check for missing values
    missing_dates = data[data['order_date'].isnull()]
    if not missing_dates.empty:
        discrepancies['missing_dates'] = f"Missing order dates found: {len(missing_dates)}"

    # Convert to datetime and check for invalid dates
    data['order_date'] = pd.to_datetime(data['order_date'], errors='coerce')

    # Check for invalid dates (NaT values)
    invalid_dates = data[data['order_date'].isna()]
    if not invalid_dates.empty:
        discrepancies['invalid_dates'] = f"Invalid order dates found: {invalid_dates['order_date'].tolist()}"

    # Check for future dates
    future_dates = data[data['order_date'] > pd.Timestamp.now()]
    if not future_dates.empty:
        discrepancies['future_dates'] = f"Future order dates found: {future_dates['order_date'].tolist()}"

    # Check if the order_date is in datetime64[ns] format
    if not pd.api.types.is_datetime64_any_dtype(data['order_date']):
        discrepancies['format_error'] = "order_date is not in datetime64[ns] format."

    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in order dates:\n"
        for issue, details in discrepancies.items():
            result_message += f"{issue}: {details}\n"
    else:
        result_message = "All order dates are valid and consistent."

    return result_message

def validate_order_time(data):
    """
    Validate that time_ordered and time_order_picked are in valid formats,
    complete, and logically consistent.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'time_ordered' and 'time_order_picked'.

    Returns:
        dict: A dictionary with issues found related to time_ordered and time_order_picked.
    """
    discrepancies = {}

    # Check if the required columns exist
    if 'time_ordered' not in data.columns or 'time_order_picked' not in data.columns:
        raise ValueError("The DataFrame must contain 'time_ordered' and 'time_order_picked' columns.")

    # Check for missing values
    missing_ordered = data[data['time_ordered'].isnull()]
    missing_picked = data[data['time_order_picked'].isnull()]
    
    if not missing_ordered.empty:
        discrepancies['missing_time_ordered'] = f"Missing time_ordered found: {len(missing_ordered)}"
    if not missing_picked.empty:
        discrepancies['missing_time_order_picked'] = f"Missing time_order_picked found: {len(missing_picked)}"

    # Check for valid time format and logical consistency
    invalid_times = []
    inconsistent_times = []
    
    for index, row in data.iterrows():
        try:
            time_ordered = pd.to_datetime(row['time_ordered'], format='%H:%M:%S', errors='raise')
            time_order_picked = pd.to_datetime(row['time_order_picked'], format='%H:%M:%S', errors='raise')
            
            if time_order_picked < time_ordered:
                inconsistent_times.append((row['time_ordered'], row['time_order_picked']))
        except ValueError:
            invalid_times.append((row['time_ordered'], row['time_order_picked']))

    if invalid_times:
        discrepancies['invalid_times'] = f"Invalid time formats found: {invalid_times}"
    if inconsistent_times:
        discrepancies['inconsistent_times'] = f"Inconsistent times found: {inconsistent_times}"

    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in order times:\n"
        for issue, details in discrepancies.items():
            result_message += f"{issue}: {details}\n"
    else:
        result_message = "All order times are valid and consistent."

    return result_message

def validate_weather_condition(data):
    """
    Validate that weather_condition is within expected values, complete, and consistent.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'weather_condition'.

    Returns:
        dict: A dictionary with issues found related to weather_condition.
    """
    discrepancies = {}

    # Check if the required column exists
    if 'weather_condition' not in data.columns:
        raise ValueError("The DataFrame must contain 'weather_condition' column.")

    # Define expected weather conditions
    expected_conditions = {"Fog", "Cloudy", "Sunny", "Sandstorms", "Windy", "Stormy"}

    # Check for missing values
    missing_conditions = data[data['weather_condition'].isnull()]
    if not missing_conditions.empty:
        discrepancies['missing_weather_conditions'] = f"Missing weather conditions found: {len(missing_conditions)}"

    # Check for valid weather conditions
    invalid_conditions = data[~data['weather_condition'].isin(expected_conditions)]
    if not invalid_conditions.empty:
        discrepancies['invalid_weather_conditions'] = {
            "count": len(invalid_conditions),
            "list": invalid_conditions['weather_condition'].unique().tolist()
        }

    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in weather conditions:\n"
        for issue, details in discrepancies.items():
            if isinstance(details, dict):
                result_message += f"{issue}: {details['count']} found. List: {details['list']}\n"
            else:
                result_message += f"{issue}: {details}\n"
    else:
        result_message = "All weather conditions are valid and consistent."

    return result_message

def validate_road_traffic_density(data):
    """
    Validate that road_traffic_density is within expected values, complete, and consistent.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'road_traffic_density'.

    Returns:
        dict: A dictionary with issues found related to road_traffic_density.
    """
    discrepancies = {}

    # Check if the required column exists
    if 'road_traffic_density' not in data.columns:
        raise ValueError("The DataFrame must contain 'road_traffic_density' column.")
    
    # Define expected road traffic densities
    expected_densities = {"Low", "Medium", "High", "Jam"}
    
    # Check for missing values
    missing_densities = data[data['road_traffic_density'].isnull()]
    if not missing_densities.empty:
        discrepancies['missing_road_traffic_density'] = f"Missing road traffic densities found: {len(missing_densities)}"
    
    # Check for valid road traffic densities
    invalid_densities = data[~data['road_traffic_density'].isin(expected_densities)]
    if not invalid_densities.empty:
        discrepancies['invalid_road_traffic_density'] = {
            "count": len(invalid_densities),
            "list": invalid_densities['road_traffic_density'].unique().tolist()
        }
    
    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in road traffic densities:\n"
        for issue, details in discrepancies.items():
            if isinstance(details, dict):
                result_message += f"{issue}: {details['count']} found. List: {details['list']}\n"
            else:
                result_message += f"{issue}: {details}\n"
    else:
        result_message = "All road traffic densities are valid and consistent."

    return result_message

def validate_vehicle_condition(data):
    """
    Validate that vehicle_condition is within expected values, complete, and consistent.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'vehicle_condition'.

    Returns:
        dict: A dictionary with issues found related to vehicle_condition.
    """
    discrepancies = {}

    # Check if the required column exists
    if 'vehicle_condition' not in data.columns:
        raise ValueError("The DataFrame must contain 'vehicle_condition' column.")  
    
    # Define expected vehicle conditions
    expected_conditions = {0: "Terrible", 1: "Bad", 2: "Average", 3: "Good"}

    # Check for missing values
    missing_conditions = data[data['vehicle_condition'].isnull()]
    if not missing_conditions.empty:
        discrepancies['missing_vehicle_conditions'] = f"Missing vehicle conditions found: {len(missing_conditions)}"

    # Check for valid vehicle conditions
    invalid_conditions = data[~data['vehicle_condition'].isin(expected_conditions)]
    if not invalid_conditions.empty:
        discrepancies['invalid_vehicle_conditions'] = {
            "count": len(invalid_conditions),
            "list": invalid_conditions['vehicle_condition'].unique().tolist()
        }

    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in vehicle conditions:\n"
        for issue, details in discrepancies.items():
            if isinstance(details, dict):
                result_message += f"{issue}: {details['count']} found. List: {details['list']}\n"
            else:
                result_message += f"{issue}: {details}\n"
    else:
        result_message = "All vehicle conditions are valid and consistent."

    return result_message

def validate_type_of_order(data):
    """
    Validate that type_of_order is within expected values, complete, and consistent.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'type_of_order'.

    Returns:
        dict: A dictionary with issues found related to type_of_order.
    """
    discrepancies = {}
    
    # Check if the required column exists
    if 'type_of_order' not in data.columns:
        raise ValueError("The DataFrame must contain 'type_of_order' column.")
    
    # Define expected type of orders
    expected_orders = {"Meal", "Snack", "Drinks", "Buffet"}  
    
    # Check for missing values
    missing_orders = data[data['type_of_order'].isnull()]
    if not missing_orders.empty:
        discrepancies['missing_type_of_order'] = f"Missing type of orders found: {len(missing_orders)}"
    
    # Check for valid type of orders
    invalid_orders = data[~data['type_of_order'].isin(expected_orders)]
    if not invalid_orders.empty:
        discrepancies['invalid_type_of_order'] = {
            "count": len(invalid_orders),
            "list": invalid_orders['type_of_order'].unique().tolist()
        }   
    
    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in type of orders:\n"
        for issue, details in discrepancies.items():
            if isinstance(details, dict):
                result_message += f"{issue}: {details['count']} found. List: {details['list']}\n"   
            else:
                result_message += f"{issue}: {details}\n"
    else:
        result_message = "All type of orders are valid and consistent."

    return result_message
    
def validate_type_of_vehicle(data):
    """
    Validate that type_of_vehicle is within expected values, complete, and consistent.

    Args:
        data (pd.DataFrame): The input DataFrame containing 'type_of_vehicle'.

    Returns:
        dict: A dictionary with issues found related to type_of_vehicle.
    """
    discrepancies = {}  
    
    # Check if the required column exists
    if 'type_of_vehicle' not in data.columns:
        raise ValueError("The DataFrame must contain 'type_of_vehicle' column.")
    
    # Define expected type of vehicles
    expected_vehicles = {'motorcycle', 'scooter', 'electric_scooter', 'bicycle'}
    
    # Check for missing values
    missing_vehicles = data[data['type_of_vehicle'].isnull()]
    if not missing_vehicles.empty:
        discrepancies['missing_type_of_vehicle'] = f"Missing type of vehicles found: {len(missing_vehicles)}"
    
    # Check for valid type of vehicles
    invalid_vehicles = data[~data['type_of_vehicle'].isin(expected_vehicles)]
    if not invalid_vehicles.empty:
        discrepancies['invalid_type_of_vehicle'] = {
            "count": len(invalid_vehicles),
            "list": invalid_vehicles['type_of_vehicle'].unique().tolist()
            }
    
    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in type of vehicles:\n"
        for issue, details in discrepancies.items():
            if isinstance(details, dict):
                result_message += f"{issue}: {details['count']} found. List: {details['list']}\n"
            else:
                result_message += f"{issue}: {details}\n"
    else:
        result_message = "All type of vehicles are valid and consistent."

    return result_message   


def validate_festival(data):
    """
    Validate that festival is within expected values, complete, and consistent.
    
    Args:
        data (pd.DataFrame): The input DataFrame containing 'festival'.

    Returns:
        dict: A dictionary with issues found related to festival.
    """
    discrepancies = {}
    
    # Check if the required column exists
    if 'festival' not in data.columns:
        raise ValueError("The DataFrame must contain 'festival' column.")
    
    # Define expected festivals
    expected_festivals = {'No', 'Yes'}  
    
    # Check for missing values
    missing_festivals = data[data['festival'].isnull()]
    if not missing_festivals.empty:
        discrepancies['missing_festivals'] = f"Missing festivals found: {len(missing_festivals)}"   
    
    # Check for valid festivals
    invalid_festivals = data[~data['festival'].isin(expected_festivals)]
    if not invalid_festivals.empty:
        discrepancies['invalid_festivals'] = {
            "count": len(invalid_festivals),
            "list": invalid_festivals['festival'].unique().tolist()
        }   
    
    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in festivals:\n"
        for issue, details in discrepancies.items():
            if isinstance(details, dict):
                result_message += f"{issue}: {details['count']} found. List: {details['list']}\n"   
            else:
                result_message += f"{issue}: {details}\n"
    else:
        result_message = "All festivals are valid and consistent."

    return result_message  

def validate_city(data):
    """
    Validate that city is within expected values, complete, and consistent.
    
    Args:
        data (pd.DataFrame): The input DataFrame containing 'city'.

    Returns:
        dict: A dictionary with issues found related to city.
    """
    discrepancies = {}
    
    # Check if the required column exists
    if 'city' not in data.columns:
        raise ValueError("The DataFrame must contain 'city' column.")
    
    # Define expected cities
    expected_cities = {'Metropolitian', 'Urban', 'Semi-Urban'}  
    
    # Check for missing values
    missing_cities = data[data['city'].isnull()]
    if not missing_cities.empty:
        discrepancies['missing_cities'] = f"Missing cities found: {len(missing_cities)}"
    
    # Check for valid cities
    invalid_cities = data[~data['city'].isin(expected_cities)]
    if not invalid_cities.empty:
        discrepancies['invalid_cities'] = {
            "count": len(invalid_cities),
            "list": invalid_cities['city'].unique().tolist()
        }
    
    # Prepare the output message
    if discrepancies:
        result_message = "Discrepancies found in cities:\n"
        for issue, details in discrepancies.items():
            if isinstance(details, dict):
                result_message += f"{issue}: {details['count']} found. List: {details['list']}\n"
            else:
                result_message += f"{issue}: {details}\n"
    else:
        result_message = "All cities are valid and consistent."

    return result_message

# need to write the rule for multiple_deliveries because of this feature is just only indicator